# liberyacs

`liberyacs` is a Python library based on `yacs`. It enhances YAML configuration handling by supporting dynamic evaluation of values into Python objects, literals, and more. It provides developers with the freedom to define sophisticated configurations that integrate seamlessly with Python code.

## Key Features

- Dynamic evaluation of YAML values into Python objects and literals.
- Recursive evaluation.
- Self-referencing support for chaining and nesting of configuration values.
- Flexible importing of additional libraries via the `extralibs` field.
- Seamless integration with `yacs` for standard YAML parsing.

## Installation

You can install `liberyacs` via pip from PyPI or directly from the Git repository:

```bash
pip install liberyacs
```

Or, if installing from Git:

```bash
pip install git+https://github.com/tronglh241/liberyacs.git
```

This option is helpful if you want to access the latest development version of `liberyacs` or if a specific feature or bug fix is not yet available in the PyPI release.

## Usage

```python
from liberyacs import CfgNode

# Load configuration with dynamic evaluation
config = CfgNode.load(filepath, evaluate=True)

# Or use as standard yacs, without dynamic evaluation
config = CfgNode.load(filepath, evaluate=False)
```

## Evaluation Principles

### String Evaluation

- **String values are evaluated once.**
  - Example:
    ```yaml
    first_str: "'print'"
    second_str: print
    ```
    - `first_str`'s value will be string literal `'print'`.
    - `second_str`'s value will be the `print` function.

- **If a string evaluates to a non-string, it will be further evaluated.**
  - Example:
    ```yaml
    tuple: (1, 1.2, "'word'")
    ```
    - `tuple`'s value will be `(1, 1.2, 'word')`.

### Dictionary and Object Evaluation

- **Dictionary values are converted to `CfgNode` objects.**
  - Example:
    ```yaml
    video:
      path: some_video.mp4
    ```
    - You can access `path`'s value using either `config.video.path` or `config.video['path']`.

- **When a dictionary contains exactly `module` and `name`:**
  - It will be evaluated into a Python object using the provided arguments in `kwargs`.
  - If `kwargs` is not provided, the object is created using its default constructor, without any arguments.
  - Example:
    ```yaml
    date:
      module: datetime
      name: datetime
      kwargs:
        year: 2024
        month: 12
        day: 24
    ```
    - Equivalent to:
      ```python
      from datetime import datetime

      config.date = datetime(year=2024, month=12, day=24)
      ```
  - **Default Constructor Behavior:**
    ```yaml
    empty_list:
      module: builtins
      name: list
    ```
    - Equivalent to:
      ```python
      config.empty_list = list()
      ```
- **When a dictionary does not contain both `module` and `name`:**
  - It will be treated as an ordinary dictionary and no evaluation into a Python object will occur.

### Lists and Tuples Evaluation

- **Lists and tuples are recursively evaluated.**

### Importing Extra Libraries

- You can specify additional libraries for evaluation using the `extralibs` field.
  - Example:
    ```yaml
    numpy_pi: np.pi
    math_pi: m_pi
    extralibs:
      np: numpy
      m_pi:
        module: math
        name: pi
    ```
    - Equivalent to:
      ```python
      import numpy as np
      from math import pi as m_pi

      config.numpy_pi = np.pi
      config.math_pi = m_pi
      ```

- **Flexible Importing:** The `extralibs` mechanism allows mapping custom module aliases and object references directly in the configuration. This ensures that the configuration can handle complex dependencies effortlessly.

### Self-Referencing Values

- **Self-Referencing:** Values can reference other values in the configuration, provided the referenced value is already defined.
  - Example:
    ```yaml
    base_value: 10
    level_one: base_value * 2
    level_two: level_one + 5
    ```
    - `level_one` will resolve to `20` (10 \* 2), and `level_two` will resolve to `25` (20 + 5).

- **Depth-First Evaluation:** This ensures that dependencies like `base_value` and `level_one` are fully resolved before `level_two` is evaluated, enabling robust and reliable configurations.

## Examples

### Prediction on MNIST Dataset

Using `liberyacs` to configure a basic prediction pipeline on the MNIST dataset with MobileNetV2 from the `torchvision` library. This serves as a straightforward demonstration of how `liberyacs` can be utilized.

#### YAML Configuration

```yaml
model:
  module: torchvision.models
  name: mobilenet_v2

data:
  module: torch.utils.data
  name: DataLoader
  kwargs:
    dataset:
      module: torchvision.datasets
      name: MNIST
      kwargs:
        root: "'data/'"
        train: False
        download: True
        transform: 'transforms.Compose([
          transforms.ToTensor(),
          transforms.Normalize((0.1307,), (0.3081,)),
          transforms.Lambda(lambda x: x.repeat(3, 1, 1)),
        ])'
    shuffle: False
    batch_size: 16

extralibs:
  transforms: torchvision.transforms
```

#### Python Code

```python
import torch
from liberyacs import CfgNode

# Load configuration
config = CfgNode.load('config.yml', evaluate=True)

# Load model and data
model = config.model
mnist_data = config.data

with torch.no_grad():
    # Run predictions
    images, _ = next(iter(mnist_data))
    outputs = model(images)
    predictions = torch.argmax(outputs, dim=1)
    print(predictions)
```

---

With `liberyacs`, you can unlock the full potential of dynamic configuration management in Python. Simplify your workflows, reduce boilerplate, and gain unparalleled flexibility in defining configurations for your projects!

