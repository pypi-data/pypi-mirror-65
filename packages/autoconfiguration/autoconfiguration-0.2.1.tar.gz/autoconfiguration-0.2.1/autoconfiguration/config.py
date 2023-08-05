"""Contains the :class:`Config` class that loads the configuration files."""

import logging
from collections import namedtuple
from configparser import ConfigParser
from typing import List, Union

from autoconfiguration.infrastructure.singleton import Singleton


LOG = logging.getLogger(__name__)


def _valid_name(name: str) -> str:
    return name.replace("-", "_")


class Config(metaclass=Singleton):
    """
    Loads the configuration files and will contain all values of these files.
    """

    def __init__(self, config_files: List[str]):
        self._config = ConfigParser()
        self._config.read(config_files)

        self._sections = {
            _valid_name(section): self._create_namedtuple(section)
            for section in self._config.sections()
        }
        LOG.debug("Generated config: %s", self._sections)

    def _create_namedtuple(self, section: str):
        keys = (_valid_name(key) for key in self._config[section].keys())
        values = self._config[section].values()
        return namedtuple(_valid_name(section.title()), keys)(*values)

    def __getattr__(self, name):
        return self._sections[name]
