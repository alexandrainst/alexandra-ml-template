# {{ cookiecutter.project_name | replace("_", " ") | title }}

{{ cookiecutter.project_description }}

## Python Conventions

### Development Workflow

- Use `uv run` for all script and command execution
- Use `pyproject.toml`, not `requirements.txt` for dependency management
- Do not read entire files, find the relevant line(s) with command-line tools, and only
  read those lines

### Code Organisation

- Keep modules focused and cohesive
- Prefer many small modules over few large ones
- All code modules are in the `src/<project_name>` directory. These are not executed but
  are imported by the scripts
- All scripts are in the `src/scripts` directory. These are executed with `uv run`
- All tests are in the `tests/` directory
- Configs are sometimes available and if so, they are in the `config/` directory
- There will always be a `pyproject.toml` file in the root directory
- Use `uv add <package>` to add packages to the project, do not just add them manually
  to `pyproject.toml`. Add development dependencies with `uv add --group=dev <package>`
- Use the `make tree` command to see the directory structure

### Code Quality

#### Quality Checkers

- Run `make check` to run formatters, linters and type checkers.
- Run tests with `make test`.

#### General Code Conventions

- Code should always fit within 88 characters
- All imports should happen at the top of each file. The only excuse for not doing this
  is if the import would cause a circular import, in which case this should be stated in
  a comment next to the import statement
- Never use the old %-style string formatting. Use f-strings instead
- Never use `print` statements - use a logger instead
- Functions and classes in a module or script should be ordered from the most high-level
  to the most low-level. For example, if a function is a helper function that is only
  used by another function, then the helper function should come after the function that
  uses it. If there is a `main` function, then it should always be first
- When we import things in modules from other modules in the package, we always do it
  using relative imports:

  ```python title="src/mypackage/module.py"
  from .another_module import some_function
  ```

- When we import things in scripts from other modules or other scripts, we always do it
  using absolute imports:

  ```python title="src/scripts/script.py"
  from mypackage.module import some_function
  from another_script import some_other_function
  ```

  This also holds when we're importing things from modules in our tests.

#### Type Hints

- Fully type-annotate all functions, methods, and variables
- Target Python 3.12+ syntax:
  - Use `list[T]`, `dict[K, V]`, `set[T]` (not `List`, `Dict`, `Set` from typing)
  - Use `X | Y` for unions (not `Union[X, Y]`)
  - Use `X | None` for optional types (not `Optional[X]`)
- Always use `import typing as t` and use the `t.` prefix for types from the typing
  module, such as `t.Literal`, `t.TypeAlias` or `t.TYPE_CHECKING`
- For `Iterable`, `Generator` and `Callable`, use these from the `collections.abc`
  module, not from `typing`. Import this as `import collections.abc as c` and refer to
  the types as `c.Iterable`, `c.Generator` and `c.Callable`, etc.
- Try not to use the `Any` type. You can often use`t.TypeVar` instead, but always give
  such type variables meaningful names, and not just single letter names like `T`. The
  main place where `Any` types can be acceptable is as the return type of a dictionary
  with mixed outputs, e.g., `dict[str, t.Any]`, since otherwise you would encounter
  issues with the type checker. Note that `list[t.Any]` is not okay.
- Use the `None` return type for functions that do not return anything. Never use the
  `NoReturn` type.

#### Functions

- Use a single leading underscore (`_`) for protected functions which should not be
  imported from outside the module, or for protected methods which should not be used
  outside the class they are defined in
- Always use keyword arguments when calling functions, never positional arguments
- Example:

  ```python
  def process_items(items: list[Item]) -> list[Result]:
      ...

  process_items(items=items)
  ```

### Documentation

- Avoid tutorial-style `#` comments that explain what code does.
- Comments should explain **why**, not **what** (the code itself should be
  self-explanatory)
- Use Google-style docstrings for all public functions, classes, and modules.
- Always include a newline after the name of each argument and exception in the
  docstring.
- Always prefer ascii characters over unicode (e.g., arrows as -> over →)
- Example:

  ```python
  def process_items(items: list[Item], log: bool) -> list[Result]:
      """Process items and return results.

      Args:
          items:
            List of items to process.
          log:
            Whether to log progress.

      Returns:
          List of processed results.

      Raises:
          ValueError:
            If items list is empty.
      """
      if log:
          logger.info("Processing items")
      return batch_process(items=items)
  ```
