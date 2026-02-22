import top_secret

my_dict = {
  "hello": "world",
  "foo": "bar",
  "baz": "qux",
  "hello world": "foo bar baz qux",
  "spam": "eggs"
}
test_dict = top_secret.loads(top_secret.dumps(my_dict))
with open("test.txt", "w") as f:
  top_secret.dump(test_dict, f)
with open("test.txt", "r") as f:
  test_dict = top_secret.load(f)
assert test_dict == my_dict, f"{repr(test_dict)} != {repr(my_dict)}"
