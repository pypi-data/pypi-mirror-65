"""
Contains the initialization for the autoconfiguration package. It searches for the
config files and initializes the instance of :class:`Config`.
"""

import logging
import os
from typing import Tuple

from autoconfiguration.config import Config
from autoconfiguration.exceptions.config_class_errors import ConfigNotInitializedError
from autoconfiguration.exceptions.config_dir_errors import ConfigDirNotFoundError
from autoconfiguration.exceptions.config_file_errors import NoConfigFilesFoundError

LOG = logging.getLogger(__name__)

CONFIG_EXTENSION = ".ini"
CONFIG_PREFIX = "config-"
GLOBAL_CONFIG = f"config{CONFIG_EXTENSION}"


def init(*args: str, config_dir: str = "config") -> Config:
    """
    Initializes the :class:`Config` class.

    Searches for the passed configuration files (args) automatically inside
    config_dir. The global config (config.ini) is always loaded by default. The order
    of the passed files matters because the files can depend on each other. Files at
    a higher index in the list can depend on files with lower indices. Values are
    overwritten by files at a higher index.

    :param args: Environments that should be loaded. They should be inside config_dir.
    :param config_dir: Should be a path that is reachable from the directory where the
        application was executed. Default: config
    :returns: The initialized :class:`Config` instance containing the values of the
        config files
    """
    if Config._instance:
        LOG.debug("Config was already initialized. Returning existing instance.")
        return Config()

    if not os.path.exists(config_dir):
        raise ConfigDirNotFoundError(config_dir)
    if not os.path.exists(os.path.join(config_dir, GLOBAL_CONFIG)):
        raise NoConfigFilesFoundError()

    config_files = _validate_config_files(*args, config_dir=config_dir)
    LOG.info("The following config files were found: %s", config_files)

    return Config(config_files)


def get():
    """
    Returns the initialized :class:`Config` instance.

    :returns: The initialized :class:`Config` instance
    :raise ConfigNotInitializedError: If the :class:`Config` was not initialized
    """
    if not Config._instance:
        raise ConfigNotInitializedError()
    return Config()


def _validate_config_files(*args: str, config_dir: str) -> Tuple[str, ...]:
    if not args:
        return (os.path.join(config_dir, GLOBAL_CONFIG),)

    not_existing_config_files = [
        config_file
        for config_file in args
        if not os.path.exists(
            os.path.join(config_dir, _get_correct_config_filename(config_file))
        )
    ]

    if len(not_existing_config_files) > 1:
        LOG.warning(
            "The following config files could not be found: %s",
            not_existing_config_files,
        )

    return (
        os.path.join(config_dir, GLOBAL_CONFIG),
        *(
            os.path.join(config_dir, _get_correct_config_filename(config_file))
            for config_file in args
            if config_file not in not_existing_config_files
        ),
    )


def _get_correct_config_filename(filename: str):
    return (
        ("" if filename.startswith(CONFIG_PREFIX) else CONFIG_PREFIX)
        + filename
        + ("" if filename.endswith(CONFIG_EXTENSION) else CONFIG_EXTENSION)
    )


def _reset():
    Config._instance = None
