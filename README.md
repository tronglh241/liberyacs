# Liberyacs

Liberyacs is a Python library based on `yacs`, designed to enhance YAML configuration handling by supporting dynamic evaluation of values into Python objects, literals, and more. It provides developers with the freedom to define sophisticated configurations that integrate seamlessly with Python code.

## Installation

You can install Liberyacs via pip from PyPI or directly from the Git repository:

```bash
pip install liberyacs
```

Or, if installing from Git:

```bash
pip install git+https://github.com/yourusername/liberyacs.git
```

## Usage

```python
from liberyacs import CfgNode

# Load configuration with dynamic evaluation
config = CfgNode.load(filepath, evaluate=True)

# Or use as standard yacs, without dynamic evaluation
config = CfgNode.load(filepath, evaluate=False)
```

## Evaluation Principles

### General Rules
- **String values are evaluated once.**
  - Example:
    ```yaml
    first_str: "'print'"
    second_str: print
    ```
    - `first_str`'s value will be the string literal `'print'`.
    - `second_str`'s value will be the `print` function.

- **If a string evaluates to a non-string, it will be further evaluated.**
  - Example:
    ```yaml
    tuple: (1, 1.2, "'word'")
    ```
    - `tuple`'s value will be `(1, 1.2, 'word')`.

- **Dictionary values are converted to `CfgNode` objects.**
  - Example:
    ```yaml
    video:
        path: some_video.mp4
    ```
    - You can access `path`'s value using either `config.video.path` or `config.video['path']`.

- **Lists and tuples are recursively evaluated.**

### Python Object Evaluation

- If a dictionary contains both `_module_` and `_name_`, it will be evaluated into a Python object using the provided arguments in `_kwargs_`.
  - Example:
    ```yaml
    date:
        _module_: datetime
        _name_: datetime
        _kwargs_:
            year: 2024
            month: 12
            day: 24
    ```
    - Equivalent to:
      ```python
      from datetime import datetime

      config.date = datetime(year=2024, month=12, day=24)
      ```
  - **Default Constructor Behavior:** If `_kwargs_` is not provided, no arguments will be passed to the initialization, and the object will be created using its default constructor. For instance:
    ```yaml
    empty_list:
        _module_: builtins
        _name_: list
    ```
    - Equivalent to:
      ```python
      config.empty_list = list()
      ```
  - **No Arguments Example:** This demonstrates the behavior when `_kwargs_` is omitted. It allows creating objects with their default settings effortlessly.

- **Extra Fields Are Discarded:** Only the keys `_module_`, `_name_`, and `_kwargs_` are processed during evaluation. Any additional fields in the dictionary will be ignored.
  - Example:
    ```yaml
    date:
        _module_: datetime
        _name_: datetime
        _kwargs_:
            year: 2024
            month: 12
            day: 24
        random_field: 0
    ```
    - Here, `random_field` will be discarded and not included in the configuration.

### Importing Extra Libraries

- You can specify additional libraries for evaluation using the `_extralibs_` field.
  - Example:
    ```yaml
    numpy_pi: np.pi
    math_pi: m_pi
    _extralibs_:
        np: numpy
        m_pi:
            _module_: math
            _name_: pi
    ```
    - Equivalent to:
      ```python
      import numpy as np
      from math import pi as m_pi

      config.numpy_pi = np.pi
      config.math_pi = m_pi
      ```

- **Flexible Importing:** The `_extralibs_` mechanism allows mapping custom module aliases and object references directly in the configuration. This ensures that the configuration can handle complex dependencies effortlessly.

### Self-Referencing Values

- Values can reference other values in the configuration, provided the referenced value is already defined. The evaluation process is conducted in a depth-first manner to resolve dependencies accurately.
  - Example:
    ```yaml
    a_list: [1, 2, 3, 4]
    list_length: len(a_list)
    ```
    - `list_length` will be `4`.
  - **Depth-First Evaluation:** This ensures that any referenced values are fully resolved before being used, enabling robust and reliable configurations.

---

With Liberyacs, you can unlock the full potential of dynamic configuration management in Python. Simplify your workflows, reduce boilerplate, and gain unparalleled flexibility in defining configurations for your projects!

