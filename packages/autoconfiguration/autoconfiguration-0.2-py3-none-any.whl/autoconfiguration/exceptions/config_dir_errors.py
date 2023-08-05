"""Contains exceptions that are raised when errors occur with config directories."""


class ConfigDirNotFoundError(Exception):
    """Raised if the configuration directory does not exist."""

    def __init__(self, config_dir: str):
        super().__init__(
            f"The configuration directory '{config_dir}' could not be found!"
        )
