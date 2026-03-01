# Iterate over a sorted list of file names with their respective extensions
for i in sorted([
  "list_files.py python",  # Python script for listing files
  "test_top_secret.py python",  # Python script for testing top secret functionality
  "top_secret.py python",  # Main Python script for top secret operations
  "pyproject.toml toml",  # Configuration file for Python project
  "LICENSE.txt plaintext",  # Text file containing the license information
  "README.md markdown"  # Markdown file providing project documentation
]):
  # Split the string into file name and its extension
  fi, li = i.split(" ")

  # Print the file name
  print(fi)

  # Print the file extension in a code block format
  print("``` " + li)

  # Open the file in read mode
  with open(fi, "r") as f:
    # Read the file content and replace any ending code block syntax
    print(f.read().replace("\n```", "\n'''"))

  # Print the closing code block syntax
  print("```")

  # Print two new lines for better readability
  print()
  print()
