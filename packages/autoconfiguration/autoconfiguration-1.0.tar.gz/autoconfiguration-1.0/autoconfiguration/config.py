"""Contains the :class:`Config` class that loads the configuration files."""

import logging
from collections import namedtuple
from configparser import ConfigParser
from typing import Tuple

from autoconfiguration.infrastructure.singleton import Singleton


LOG = logging.getLogger(__name__)


def _valid_name(name: str) -> str:
    return name.replace("-", "_")


class Config(metaclass=Singleton):
    """
    Loads the configuration files and will contain all values of these files.
    """

    def __init__(self, config_files: Tuple[str, ...]):
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

    def __getattr__(self, name: str):
        return self._sections[name]

    def __contains__(self, item: str) -> bool:
        return item in self._sections

    def __getitem__(self, item: str):
        return self._sections[item]

    def get(self, section_name: str, default_value=None):
        """
        Returns the namedtuple of a section if it exists. The default_value is
        returns otherwise. Returns None if the section does not exist and no
        default_value was specified.

        :param section_name: The name of the configuration section
        :param default_value: The value that will be returned if the section does not
            exist
        :return: The namedtuple of the section or the default_value or None
        """
        return (
            self._sections[section_name]
            if section_name in self._sections
            else default_value
        )
