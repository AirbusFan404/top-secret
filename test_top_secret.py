import top_secret  # Importing the top_secret module for serialization and deserialization
import typing_extensions  # Importing typing_extensions for type hinting support
import unittest  # Importing the unittest module to create and run tests


class TestTopSecret(
    unittest.TestCase
):  # Defining a test case class that inherits from unittest.TestCase

  def test_roundtrip(
      self: typing_extensions.Self
  ) -> None:  # Test method for roundtrip serialization
    data = {
        "foo": "bar",
        "spam": "eggs"
    }  # Sample data to be serialized and deserialized
    # Asserting that the deserialized data matches the original data after serialization
    self.assertEqual(top_secret.loads(top_secret.dumps(data)), data)

  def test_roundtripf(
      self: typing_extensions.Self
  ) -> None:  # Test method for file-based roundtrip serialization
    data = {
        "foo": "bar",
        "spam": "eggs"
    }  # Sample data to be written to a file
    with open("test.txt", "w") as f:  # Opening a file in write mode
      top_secret.dump(data, f)  # Serializing and writing the data to the file
    with open("test.txt", "r") as f:  # Opening the same file in read mode
      # Asserting that the deserialized data from the file matches the original data
      self.assertEqual(top_secret.load(f), data)


if __name__ == "__main__":  # Checking if the script is being run directly
  unittest.main()  # Running the unit tests
