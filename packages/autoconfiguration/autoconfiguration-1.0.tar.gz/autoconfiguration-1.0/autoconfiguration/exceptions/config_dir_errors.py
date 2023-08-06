"""Contains exceptions that are raised when errors occur with config directories."""
from autoconfiguration.exceptions.base_exception import ConfigBaseError


class ConfigDirNotFoundError(ConfigBaseError):
    """Raised if the configuration directory does not exist."""

    def __init__(self, config_dir: str):
        super().__init__(
            f"The configuration directory '{config_dir}' could not be found!"
        )
