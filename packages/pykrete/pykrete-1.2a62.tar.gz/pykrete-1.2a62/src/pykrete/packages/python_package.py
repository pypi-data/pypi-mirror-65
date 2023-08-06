"""
Python package
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import logging
from pykrete.versioning import Formatting, TagVersion, VersionPyVersion


class PythonPackage:
    """Python package"""

    @property
    def project(self):
        """
        :return: (string) name of project package under 'src'.
        """
        return self._project

    @property
    def version(self):
        """
        :return: (string) The project's version
        """
        return self._version

    def __init__(self, project):
        """Initializes this instance to analyze the specified project

        :param project: name of project package under 'src'
        """
        self._logger = logging.getLogger(__name__)
        self._project = project
        version_makers = self._collect_version_makers()
        self._version = self._get_version(version_makers)

    @property
    def long_description(self):
        """Gets the contents of the README.md file

        :return: Long description
        """
        with open('README.md', 'r') as readme:
            return readme.read()

    def _collect_version_makers(self):
        return [self._get_version_from_tag, self._get_version_from_version_py]

    @staticmethod
    def _get_version(version_makers):
        """Gets the package version

        :return: The version
        :exception IOError: Version read failed
        """
        version = None
        for maker in version_makers:
            version = maker()
            if version:
                break
        if not version:
            raise IOError('Unable to get version')

        return Formatting(version).for_python

    def _get_version_from_tag(self):
        try:
            version = TagVersion()
            self._logger.debug('Got version from tag: %s', version)
            return version
        except IOError as exc:
            self._logger.debug('Unable to get version from tag [%s]', exc)
            return None

    def _get_version_from_version_py(self):
        try:
            version = VersionPyVersion(self._project)
            self._logger.debug('Got version from version.py: %s', version)
            return version
        except IOError as exc:
            self._logger.debug('Unable to get version from version.py of %s [%s]',
                               self._project, exc)
            return None

    def __str__(self):
        return f'{self._project} v{self._version}'
