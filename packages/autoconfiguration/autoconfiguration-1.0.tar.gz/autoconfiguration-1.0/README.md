# python-autoconfiguration

Load configuration files (.ini) automatically.


## Usage

The `init` function of the `autoconfiguration` package has to be called first to initialize the configuration. Pass an arbitrary amount of configuration files to this function. All passed files will be loaded. Additionally the global configuration file (`config.ini`) will always be loaded by default. The name of the global configuration file has to be `config.ini`. All other files must start with `config-` and end with `.ini`. You don't have to use the full file names for the `init` function. You can just use the name between `config-` and `.ini`.

**Example**

config files: `config.ini`, `config-dev.ini` and `config-prod.ini` (See example/config)

Initialize autoconfiguration:
```python
from autoconfiguration import autoconfiguration

config = autoconfiguration.init("dev")
```

After the autoconfiguration was initialized you can get the configuration from anywhere in your code by calling the `get` function:
```python
from autoconfiguration import autoconfiguration

config = autoconfiguration.get()
```

### Auto completion of the Config instance in IDEs

---
**NOTE**

This is optional. Use this only if you want auto completion of the sections and keys
 of your config in IDEs.

---

If you want auto completion in IDEs, you have to add stubs to your project. First add
 a package `autoconfiguration` to your project. Make sure that the file extension of
 the `__init__` file is `.pyi` (`__init__.pyi`)! You need to create two files in that
 package:

File `autoconfiguration.pyi`:
```python
from autoconfiguration.config import Config

def init(*args: str, config_dir: str = "config") -> Config: ...
def get() -> Config: ...
```

---

File `config.pyi`:
```python
from collections import namedtuple


class Config:
    # TODO: add your sections to this class with a namedtuple annotation containing your keys
    # Example:
    credentials: namedtuple("Credentials", ("username", "password"))
```
