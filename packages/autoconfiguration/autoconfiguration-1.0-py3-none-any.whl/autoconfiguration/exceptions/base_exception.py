"""Contains the base exception of the autoconfiguration package."""


class ConfigBaseError(Exception):
    """The base autoconfiguration exception."""

    def __init__(self, message: str):
        super().__init__(message)
