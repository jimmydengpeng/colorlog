# ColorLog

![GitHub](https://img.shields.io/github/license/jimmydengpeng/colorlog)

**ColorLog** is a lightweight logger that makes logging to the terminal easy and pretty for python.

This is self-made & self-used module for coloring logging infomation. Welcome any contributions if you would like!

## TODO
- [x] Auto-inline
- [ ] Add requirements
- [ ] Upload to PyPI

## Installation

### Font
The recommended font is `MesloLGS NF`.

### Install from PyPI
TODO
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

For other detailed APIs please check the code!

