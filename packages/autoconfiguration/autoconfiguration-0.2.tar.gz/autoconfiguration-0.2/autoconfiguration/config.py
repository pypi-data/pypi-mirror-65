"""Contains the Config class that loads the configuration files."""

import logging
from collections import namedtuple
from configparser import ConfigParser
from typing import List

from autoconfiguration.infrastructure.singleton import Singleton


LOG = logging.getLogger(__name__)


class Config(metaclass=Singleton):
    """
    Loads the configuration files and will contain all values of these files.
    """

    def __init__(self, config_files: List[str]):
        self._config = ConfigParser()
        self._config.read(config_files)

        self._sections = {
            section: namedtuple(section.title(), self._config[section].keys())(
                *self._config[section].values()
            )
            for section in self._config.sections()
        }
        LOG.debug("Generated config: %s", self._sections)

    def __getattr__(self, name):
        return self._sections[name]
