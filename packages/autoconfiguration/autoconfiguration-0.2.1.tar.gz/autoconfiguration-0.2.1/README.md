# python-autoconfiguration

Load configuration files (.ini) automatically.


## Usage

### Auto completion of the Config instance in IDEs

If you want auto completion in IDEs, you have to add stubs to your project. First add
 a package `autoconfiguration` to your project. You need to create two files in that
 package:

File `autoconfiguration.pyi`:
```
from typing import List

from autoconfiguration.config import Config


def init(
    config_files: List[str] = None, current_env: str = None, config_dir: str = "config"
) -> Config: ...
```

---

File `config.pyi`:
```
from collections import namedtuple

class Config:
    # TODO: add your sections to this class with a namedtuple annotation containing your keys
    # Example:
    credentials: namedtuple("Credentials", ("username", "password"))
```


## Build & deploy

`invoke deploy`
