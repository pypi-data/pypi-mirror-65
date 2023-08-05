import logging
import os
from glob import glob
from typing import List

from autoconfiguration.config import Config
from autoconfiguration.exceptions.config_dir_errors import ConfigDirNotFoundError
from autoconfiguration.exceptions.config_file_errors import NoConfigFilesFoundError

LOG = logging.getLogger(__name__)

CONFIG_EXTENSION = ".ini"


def init(
    config_files: List[str] = None, current_env: str = None, config_dir: str = "config"
):
    if not os.path.exists(config_dir):
        raise ConfigDirNotFoundError(config_dir)

    config_files = _validate_config_files(config_files, config_dir)
    LOG.info("The following config files were found: %s", config_files)

    if current_env is None or current_env not in config_files:
        current_env = config_files[0]
        LOG.info("The current environment was set to '%s'", current_env)

    return Config(config_files[: config_files.index(current_env) + 1])


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
        elif len(not_existing_config_files) > 1:
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


def _add_config_extension(filename: str):
    return filename + ("" if filename.endswith(CONFIG_EXTENSION) else CONFIG_EXTENSION)
