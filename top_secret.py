import os
import random
from typing import TextIO

if "SECRETSEED" in os.environ:
  secret_seed = int(os.environ["SECRETSEED"], 16)
elif os.path.isfile(os.environ["HOME"] + "/secretseed.txt"):
  with open(os.environ["HOME"] + "/secretseed.txt", "r") as f:
    secret_seed = int(f.read(), 16)
else:
  secret_seed = random.randint(0, 2**32-1)
  with open(os.environ["HOME"] + "/secretseed.txt", "w") as f:
    f.write(hex(secret_seed)[2:])
random.seed(secret_seed)
addby = random.randint(1, 255)
multby = random.randint(2, 31)
digits = [*"0123456789abcdef"]
cipher_digits = [*random.sample("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", 16)]
cipher_dict = {}
decipher_dict = {}
for k, v in zip(digits, cipher_digits):
  cipher_dict[k] = v
  decipher_dict[v] = k

def cipher(s: str) -> str:
  r = ""
  for i in s:
    r += cipher_dict[i]
  return r

def decipher(s: str) -> str:
  r = ""
  for i in s:
    r += decipher_dict[i]
  return r

def calc(x: int) -> int:
  return x * multby + addby

def decalc(x: int) -> int:
  return (x - addby) // multby

def dumps(data: dict[str, str]) -> str:
  result = []
  for k, v in data.items():
    K = []
    for i in k:
      K.append(cipher(hex(calc(ord(i)))[2:]))
    V = []
    for i in v:
      V.append(cipher(hex(calc(ord(i)))[2:]))
    result.append(" ".join(K) + ": " + " ".join(V))
  return "\n".join(result)

def dump(data: dict[str, str], file: TextIO) -> int:
  return file.write(dumps(data))

def loads(data: str) -> dict[str, str]:
  result = {}
  for line in data.split("\n"):
    k, v = line.split(": ")
    K = ""
    for i in k.split(" "):
      K += chr(decalc(int(decipher(i), 16)))
    V = ""
    for i in v.split(" "):
      V += chr(decalc(int(decipher(i), 16)))
    result[K] = V
  return result

def load(file: TextIO) -> dict[str, str]:
  return loads(file.read())
