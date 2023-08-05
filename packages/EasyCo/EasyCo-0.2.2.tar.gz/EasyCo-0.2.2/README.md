# EasyCo
[![Build Status](https://travis-ci.org/spacemanspiff2007/EasyCo.svg?branch=master)](https://travis-ci.org/spacemanspiff2007/EasyCo)
[![Documentation Status](https://readthedocs.org/projects/easyco/badge/?version=latest)](https://easyco.readthedocs.io/en/latest/?badge=latest)

_Easy Configuration with yaml files_

# Goal
The goal of **EasyCo** is to provide an **easy** way of **Co**niguration using yaml files for Python programs.
It can automatically create a default configuration from provided default values and will validate the provided data.

# Documentation
[The documentation can be found at here](https://easyco.readthedocs.io)

# Example

```python
from EasyCo import ConfigFile, ConfigContainer

class MyContainer(ConfigContainer):
    SubValueA: int
    SubValueB: int = 7

class MyConfigFile(ConfigFile):
    ConfValueA: int = 5
    ConfValueB: float = 5.5

    sub_values = MyContainer()
    
cfg = MyConfigFile('test')
cfg.load()
```