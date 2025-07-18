# ConSolar Framework Documentation

## Overview

*ConSolar* is a console framework for building extensible console applications with plugin support.

---

## Getting Started

### Installation

Clone the repository and install dependencies from `requirements.txt` using `pip install -r requirements.txt`.


### Basic Usage

```python
from consolar import user, Framework, Plugin, load_plugin

# Create a user input

user.user_input("Enter your name:")
print(user.user_value)
```

---

## API Reference

### class user

- `user_input(question: str) -> None`: Prompts the user for input. Result is stored in `user_value`.
- `multi_choice(question: str, options: list) -> None`: Prompts the user to select from options. Result is stored in `user_value`.
- `user_value`: Stores the last answer from user input or choice.

### class Framework

- `register_plugin(plugin: Plugin)`: Registers a plugin instance.
- `plugins`: List of registered plugins.

### class Plugin

- `run()`: Method to be implemented by plugins.

### function load_plugin(module_name: str, class_name: str) -> Plugin

Dynamically loads a plugin class from a module.

---

## Writing Plugins

1. Inherit from `Plugin`:

```python
from consolar import Plugin
class MyPlugin(Plugin):
    def run(self):
        print("MyPlugin is running!")
```

2. Register with the framework:

```python
from consolar import Framework
fw = Framework()
fw.register_plugin(MyPlugin())
```

---

## Error Handling

- Plugin registration errors are printed to the console.

---

## Contribution

- Fork the repo, add features, and submit pull requests.

---

## License

MIT

Copyright (c) 2025 Samyar Sharafi

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

- The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
