# ColorLog

![GitHub](https://img.shields.io/github/license/jimmydengpeng/colorlog)

**ColorLog** is a lightweight logger that makes logging to the terminal easy and pretty for python.

This is self-made & self-used module for coloring logging infomation. Welcome any contributions if you would like!

## TODO
- [x] Auto-inline
- [x] Add requirements
- [x] Upload to PyPI
- [ ] Mutable number of API inputs, i.e., optional prompt or args
- [ ] log which file path the line of code in

## Installation

### Font
The recommended font is `MesloLGS NF`.

### Install from PyPI
```shell
pip install colorlog-python
```

## Usage
To use **colorlog**, just import the pre-instantiated `logger` into your code.

```python
from colorlog import logger

logger.debug("prompt:", your_args)
logger.info("prompt:", your_args)
logger.warning("prompt:", your_args)
logger.success("prompt:", your_args)
logger.error("prompt:", your_args)
```

The output in the Terminal will look like this:
![](docs/images/terminal_output.png)


For other detailed APIs please check the code!
