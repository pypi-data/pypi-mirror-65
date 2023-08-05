"""Contains exceptions that are raised when errors occur with the Config class."""


class ConfigNotInitializedError(Exception):
    """Raised if the Config class was not initialized."""

    def __init__(self):
        super().__init__(
            "The Config class was not initialized! Call the init function first."
        )
