"""
Build manager base class
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import logging
from abc import abstractmethod
from pykrete.args import environ
from pykrete.versioning import Version, RevisionType


class BuildManager:
    """Manages building a python package"""

    _logger = logging.getLogger(__name__)

    def __init__(self, version: Version):
        """Initializes this instance
        :param version: Build version
        """
        self._version = version
        self._project = environ('CI_TARGET', 'the name of the project under src')

    def run(self):
        """Runs the build process"""
        self._clean_distribution()
        self._set_package_version()
        self._build()
        self._upload(self._version.revision_type == RevisionType.Release)

    @abstractmethod
    def _clean_distribution(self):
        """Removes previous distribution files"""

    @abstractmethod
    def _set_package_version(self):
        """Sets the package version in the project's version file"""

    @abstractmethod
    def _build(self):
        """Performs the actual build using build.py"""

    @abstractmethod
    def _upload(self, is_release):
        """Uploads the package

        :param is_release: flag this package as release
        """

    def __str__(self):
        """Gets a string representation of this object"""
        return f'Builder for version {self._version} of project "{self._project}"'
