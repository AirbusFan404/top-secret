import os  # Importing the os module to interact with the operating system
import random  # Importing the random module to generate random numbers
import string  # Importing the string module for string constants
import typing_extensions  # Importing typing_extensions for type hinting

# Asserting that the module is not run directly
assert __name__ != "__main__", "This module is not meant to be run directly."

# Defining a character set for encoding/decoding
charset: str = string.ascii_letters + string.digits + string.punctuation


# Custom exception for seed errors
class SeedError(Exception):
  pass


# Function to retrieve a seed value
def _getseed() -> int:
  try:
    # Check if a seed is provided in the environment variable
    if "SECRETSEED" in os.environ:
      seed = int(os.environ["SECRETSEED"].strip(), 16)  # Convert hex to int
    # Check if a seed is provided in a file
    elif "SECRETFILE" in os.environ:
      with open(os.environ["SECRETFILE"], "r") as f:
        seed = int(f.read().strip(), 16)  # Convert hex to int
    # Check if a default seed file exists
    elif os.path.isfile(os.path.join(os.path.expanduser("~"), ".secretseed")):
      with open(os.path.join(os.path.expanduser("~"), ".secretseed"),
                "r") as f:
        seed = int(f.read().strip(), 16)  # Convert hex to int
    else:
      # Generate a random seed if none is found
      seed = random.randint(0, 2**31 - 1)
      with open(os.path.join(os.path.expanduser("~"), ".secretseed"),
                "w") as f:
        f.write(f"{seed:x}")  # Write the seed to the file in hex format
    return seed  # Return the seed value
  except Exception as e:
    # Raise a SeedError with the exception details
    raise SeedError(f"{type(e).__name__} {repr(str(e))}") from None


# Function to perform a calculation based on a number
def _calc(num: int) -> int:
  rng = random.Random(
      _getseed())  # Create a random number generator with the seed
  addby = rng.randint(-50, 50)  # Generate a random number to add
  multby = rng.randint(1, 20)  # Generate a random multiplier
  return num * multby + addby  # Return the calculated value


# Function to reverse the calculation
def _decalc(num: int) -> int:
  rng = random.Random(
      _getseed())  # Create a random number generator with the seed
  addby = rng.randint(-50, 50)  # Generate a random number to add
  multby = rng.randint(1, 20)  # Generate a random multiplier
  return (num - addby) // multby  # Return the reversed calculation


# Function to cipher a given text
def _cipher(text: str) -> str:
  rng = random.Random(
      _getseed())  # Create a random number generator with the seed
  cipher = dict(zip(string.hexdigits,
                    rng.sample(charset, 16)))  # Create a cipher mapping
  result = ""  # Initialize the result string
  for i in text:  # Iterate through each character in the text
    if i in cipher:  # Check if the character is in the cipher
      result += cipher[i]  # Append the ciphered character
    else:
      result += i  # Append the original character if not ciphered
  return result  # Return the ciphered text


# Function to decipher a given text
def _decipher(text: str) -> str:
  rng = random.Random(
      _getseed())  # Create a random number generator with the seed
  decipher = dict(zip(rng.sample(charset, 16),
                      string.hexdigits))  # Create a decipher mapping
  result = ""  # Initialize the result string
  for i in text:  # Iterate through each character in the text
    if i in decipher:  # Check if the character is in the decipher
      result += decipher[i]  # Append the deciphered character
    else:
      result += i  # Append the original character if not deciphered
  return result  # Return the deciphered text


# Custom exception for encoding errors
class TopSecretEncodeError(Exception):
  pass


# Function to serialize an object into a string format
def dumps(obj: typing_extensions.Dict[str, str]) -> str:
  try:
    result = []  # Initialize a list to hold the serialized key-value pairs
    for k, v in obj.items(
    ):  # Iterate through each key-value pair in the dictionary
      key = " ".join([_cipher(f"{_calc(ord(i)):x}")
                      for i in k])  # Cipher the key
      value = " ".join([_cipher(f"{_calc(ord(i)):x}")
                        for i in v])  # Cipher the value
      result.append(key + ": " +
                    value)  # Append the key-value pair to the result
    return "\n".join(result)  # Return the serialized string
  except Exception as e:
    # Raise a TopSecretEncodeError with the exception details
    raise TopSecretEncodeError(f"{type(e).__name__} {repr(str(e))}") from None


# Function to write serialized data to a file
def dump(obj: typing_extensions.Dict[str, str],
         fp: typing_extensions.TextIO) -> int:
  try:
    return fp.write(dumps(obj))  # Write the serialized data to the file
  except Exception as e:
    # Raise a TopSecretEncodeError with the exception details
    raise TopSecretEncodeError(f"{type(e).__name__} {repr(str(e))}") from None


# Custom exception for decoding errors
class TopSecretDecodeError(Exception):
  pass


# Function to deserialize a string back into a dictionary
def loads(s: str) -> typing_extensions.Dict[str, str]:
  try:
    result = {}  # Initialize an empty dictionary to hold the deserialized data
    for line in s.split("\n"):  # Split the string into lines
      if not line:  # Skip empty lines
        continue
      k, v = line.split(": ")  # Split the line into key and value
      key = "".join([
          chr(_decalc(int(_decipher(i), 16))) for i in k.split(" ")
      ])  # Decipher the key
      value = "".join([
          chr(_decalc(int(_decipher(i), 16))) for i in v.split(" ")
      ])  # Decipher the value
      result[key] = value  # Add the key-value pair to the result dictionary
    return result  # Return the deserialized dictionary
  except Exception as e:
    # Raise a TopSecretDecodeError with the exception details
    raise TopSecretDecodeError(f"{type(e).__name__} {repr(str(e))}") from None


# Function to load data from a file and deserialize it
def load(fp: typing_extensions.TextIO) -> typing_extensions.Dict[str, str]:
  try:
    return loads(fp.read())  # Read the file and return the deserialized data
  except Exception as e:
    # Raise a TopSecretDecodeError with the exception details
    raise TopSecretDecodeError(f"{type(e).__name__} {repr(str(e))}") from None
