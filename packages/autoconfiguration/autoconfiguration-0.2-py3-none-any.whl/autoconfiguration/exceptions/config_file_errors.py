"""Contains exceptions that are raised when errors occur with config files."""


class NoConfigFilesFoundError(Exception):
    """Raised if none of the configuration files exist."""

    def __init__(self):
        super().__init__("No configuration files could be found!")
