"""Contains exceptions that are raised when errors occur with config files."""
from autoconfiguration.exceptions.base_exception import ConfigBaseError


class NoConfigFilesFoundError(ConfigBaseError):
    """Raised if none of the configuration files exist."""

    def __init__(self):
        super().__init__("No configuration files could be found!")
