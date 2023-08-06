"""Contains exceptions that are raised when errors occur with the Config class."""
from autoconfiguration.exceptions.base_exception import ConfigBaseError


class ConfigNotInitializedError(ConfigBaseError):
    """Raised if the Config class was not initialized."""

    def __init__(self):
        super().__init__(
            "The Config class was not initialized! Call the init function first."
        )
