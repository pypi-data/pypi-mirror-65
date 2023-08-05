"""
Contains the initialization for the autoconfiguration package. It searches for the
config files and initializes the instance of :class:`Config`.
"""

import logging
import os
from glob import glob
from typing import List

from autoconfiguration.config import Config
from autoconfiguration.exceptions.config_class_errors import ConfigNotInitializedError
from autoconfiguration.exceptions.config_dir_errors import ConfigDirNotFoundError
from autoconfiguration.exceptions.config_file_errors import NoConfigFilesFoundError

LOG = logging.getLogger(__name__)

CONFIG_EXTENSION = ".ini"


def init(
    config_files: List[str] = None, current_env: str = None, config_dir: str = "config"
) -> Config:
    """
    Initializes the :class:`Config` class.

    Searches for the configuration files automatically inside config_dir if no
    config_files were passed. The order of these files matters because the files can
    depend on each other. The files are sorted alphabetically if they were found by
    the automatic search. Files at a higher index in the list can depend on files
    with lower indices. Values are overwritten by files at a higher index.

    :param config_files: A list of files that should be loaded. They should be inside
        config_dir.
    :param current_env: The config file that should be loaded. All files at a lower
        index in the config_files list than current_env will be loaded as well. The
        current_env file will always be the last file to be loaded.
    :param config_dir: Should be a path that is reachable from the directory where the
        application was executed. Default: config
    :returns: The initialized :class:`Config` instance containing the values of the
        config files
    """
    if Config._initialized:
        LOG.debug("Config was already initialized. Returning existing instance.")
        return Config()

    if not os.path.exists(config_dir):
        raise ConfigDirNotFoundError(config_dir)

    config_files = _validate_config_files(config_files, config_dir)
    LOG.info("The following config files were found: %s", config_files)

    current_env = _get_current_env(current_env, config_files)
    LOG.info("The current environment was set to '%s'", current_env)

    return Config(config_files[: config_files.index(current_env) + 1])


def get():
    """
    Returns the initialized :class:`Config` instance.

    :returns: The initialized :class:`Config` instance
    :raise ConfigNotInitializedError: If the :class:`Config` was not initialized
    """
    if not Config._initialized:
        raise ConfigNotInitializedError()
    return Config()


def _validate_config_files(config_files: List[str], config_dir: str) -> List[str]:
    if config_files is None:
        config_files = glob(os.path.join(config_dir, f"*{CONFIG_EXTENSION}"))
    else:
        not_existing_config_files = [
            config_file
            for config_file in config_files
            if not os.path.exists(
                os.path.join(config_dir, _add_config_extension(config_file))
            )
        ]

        if len(not_existing_config_files) == len(config_files):
            raise NoConfigFilesFoundError()
        if len(not_existing_config_files) > 1:
            LOG.warning(
                "The following config files could not be found: %s",
                not_existing_config_files,
            )

        config_files = [
            os.path.join(config_dir, _add_config_extension(config_file))
            for config_file in config_files
            if config_file not in not_existing_config_files
        ]

    if len(config_files) < 1:
        raise NoConfigFilesFoundError()
    return config_files


def _get_current_env(env: str, config_files: List[str]):
    if env is not None:
        if env.endswith(CONFIG_EXTENSION):
            if env not in config_files and not any(
                config_file.endswith(env + CONFIG_EXTENSION)
                for config_file in config_files
            ):
                env = None
        else:
            env = next(
                (
                    config_file
                    for config_file in config_files
                    if config_file.endswith(env + CONFIG_EXTENSION)
                ),
                None,
            )

    if env is None:
        env = config_files[0]
    return env


def _add_config_extension(filename: str):
    return filename + ("" if filename.endswith(CONFIG_EXTENSION) else CONFIG_EXTENSION)
