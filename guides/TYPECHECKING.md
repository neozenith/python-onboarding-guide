# Typechecking

<!--TOC-->

- [Typechecking](#typechecking)
  - [Level 1 - Opting In](#level-1---opting-in)
    - [😎 This works](#-this-works)
    - [😰 This does not work](#-this-does-not-work)
  - [Level 2 - Minimal Enforcement](#level-2---minimal-enforcement)
    - [😎 This works](#-this-works-1)
    - [😰 This does not work](#-this-does-not-work-1)
  - [Level 3 - Strict](#level-3---strict)
  - [Further Reading](#further-reading)
- [Typechecking Boto3](#typechecking-boto3)

<!--TOC-->

As a Data / ML Engineer, a lot of my work is enforcing schemas and making sure data is correct. That is why typechecking is an invaluable tool for Data / ML Engineers as well as runtime checking tools like [`pydantic`](https://pydantic-docs.helpmanual.io/)

To incrementally adopt typehints in a project here are the three levels and the associated `pyproject.toml` configuration for [`mypy`](https://mypy.readthedocs.io/en/stable/).

The idea is that _in conversation with your team_, you add each level when the team is ready to adopt the increasing costs and strictness. An example timeline could be 3 months at each level.

1. The first level allows some typechecking for early adopters that start adding it to the code base but it is not enforced.
2. The second level does require some work, but should be a manageable amount to adopt by focusing on only functions and method signatures.
3. The last level is more detailed and requires more work, but the bulk of the work is covered in level 2.

## Level 1 - Opting In

The first level allows some typechecking for early adopters that start adding it to the code base but it is not enforced.

With the following settings:

```toml
[tool.mypy]
exclude = ["tests/", "tasks\\.py"]
pretty = true
show_error_codes = true
show_column_numbers = true
show_error_context = true
ignore_missing_imports = true
follow_imports = "silent"

# Level 1
disallow_incomplete_defs = true

# Level 2
disallow_untyped_defs = false

# Level 3
strict = false
```

### 😎 This works

Existing code with no typehints stays fine 👍

```python
def forecast(x, m = 1, b = 0):
  """Forecast using linear regression."""
  return m * x + b
```

Fully typed code works too 👍

```python
def forecast(x: float, m: float = 1, b: float = 0) -> float:
  """Forecast using linear regression."""
  return m * x + b
```

### 😰 This does not work

Partially typed code will not work

```python
def forecast(x: float, m = 1, b = 0) -> float: # Some arguments are not typed
  """Forecast using linear regression."""
  return m * x + b
```

```python
def forecast(x: float, m: float = 1, b: float = 0): # Missing Return type
  """Forecast using linear regression."""
  return m * x + b
```

## Level 2 - Minimal Enforcement

The second level does require some work, but should be a manageable amount to adopt by focusing on only functions and method signatures.

With the following settings:

```toml
[tool.mypy]
exclude = ["tests/", "tasks\\.py"]
pretty = true
show_error_codes = true
show_column_numbers = true
show_error_context = true
ignore_missing_imports = true
follow_imports = "silent"

# Level 1
disallow_incomplete_defs = true

# Level 2
disallow_untyped_defs = true

# Level 3
strict = false
```

### 😎 This works

Only fully typed functions and methods works  👍

```python
def forecast(x: float, m: float = 1, b: float = 0) -> float:
  """Forecast using linear regression."""
  return m * x + b
```

### 😰 This does not work

Untyped and partially typed code will not work

```python
def forecast(x, m = 1, b = 0):
  """Forecast using linear regression."""
  return m * x + b
```

```python
def forecast(x: float, m = 1, b = 0) -> float: # Some arguments are not typed
  """Forecast using linear regression."""
  return m * x + b
```

```python
def forecast(x: float, m: float = 1, b: float = 0): # Missing Return type
  """Forecast using linear regression."""
  return m * x + b
```

## Level 3 - Strict

The last level is more detailed and requires more work, but the bulk of the work is covered in level 2.

With the following settings:

```toml
[tool.mypy]
exclude = ["tests/", "tasks\\.py"]
pretty = true
show_error_codes = true
show_column_numbers = true
show_error_context = true
ignore_missing_imports = true
follow_imports = "silent"

# Level 1
disallow_incomplete_defs = true

# Level 2
disallow_untyped_defs = true

# Level 3
strict = true
```

For the full specific of `strict` then [MyPy Strict Options](https://mypy.readthedocs.io/en/stable/existing_code.html#introduce-stricter-options).

This pretty much disallows the use of `Any` amongst some other corner cases, but disallowing `Any` is a big one on the way to becoming a fully typed codebase.

## Further Reading

Checkout the [MyPy Existing Code Guide](https://mypy.readthedocs.io/en/stable/existing_code.html) for more details.

# Typechecking Boto3

https://youtype.github.io/boto3_stubs_docs/

```sh
# install type annotations only for boto3
python -m pip install boto3-stubs

# install boto3 type annotations
# for ec2, s3, rds, lambda, sqs, dynamo and cloudformation
python -m pip install 'boto3-stubs[essential]'

# or install annotations for services you use
python -m pip install 'boto3-stubs[s3,dynamodb,lambda]'

# or install annotations in sync with boto3 version
python -m pip install 'boto3-stubs[boto3]'
```