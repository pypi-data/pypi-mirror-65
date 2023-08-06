# rac_schemas

JSON schemas and validation helpers.

## Requirements
*   Python 3.4 or higher
*   [jsonschema](https://python-jsonschema.readthedocs.io/en/stable/)
*   [tox](https://tox.readthedocs.io/) (for running tests)
*   [pre-commit](https://pre-commit.com/) (for running linters before committing)
    *   After installing pre-commit, install the git-hook scripts:

    ```
    $ pre-commit install
    ```

## Installation

The recommended way to install this package is using `pip`:

```
pip install rac_schemas
```

## Usage

This library has one main public method, `is_valid()`, which takes a dict as the first argument and a schema filename as the second.

```
from rac_schemas import is_valid

data = {"key": "value" ... }
is_valid(data, "object.json")
```

`rac_schemas` will attempt to add an appropriate extension to schema filenames in cases where it is either missing or incorrect. For example, if either `schema` and `schema.org` as schema filenames, `rac_schemas` will attempt to open `schema.json`.

Invalid data will raise a `jsonschema.exceptions.ValidationError`, and an invalid schema filename will raise a `FileNotFoundError`.

### Available schemas

All schemas are located in the `schemas/` subdirectory of the `rac_schemas/` directory.

#### Tests

`rac_schemas` comes with unit tests as well as linting. The easiest way to make sure all tests pass is to run `tox` from the root of the repository. This will execute all tests, and will also run `autopep8` and `flake8` linters against the codebase.

### License

Code is released under an MIT license. See`LICENSE.md`.
