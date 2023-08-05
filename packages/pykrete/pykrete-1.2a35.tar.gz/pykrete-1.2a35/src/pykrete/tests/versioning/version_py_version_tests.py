"""
Pykrete versioning.version_py_version tests
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""

import unittest
import os
import logging
from pykrete.versioning import VersionPyVersion
from .versioning import PykreteVersioningTestCase


def _get_full_path(project):
    return os.path.join('pykrete', 'tests', 'src', project)


class PykreteVersioningVersionPyVersionTestCase(PykreteVersioningTestCase):
    """Unit tests for pykrete's versioning module's VersionPyVersion class
    """

    _logger = logging.getLogger(__name__)

    def test_version_py_release_version_good(self):
        """Verifies reading of a release package's version
        """
        self._assert_good_package('african_swallow', '12.34.4.56 Release')

    def test_version_py_rc_version_good(self):
        """Verifies reading of a release-candidate package's version
        """
        self._assert_good_package('european_swallow', '12.34.3.56 RC')

    def test_version_py_missing_version_in_file(self):
        """Verifies handling of a bad version file
        """
        with self.assertRaises(IOError):
            self._logger.debug(str(VersionPyVersion(_get_full_path('a_duck'))))

    def test_version_py_missing_version_file(self):
        """Verifies handling of a missing version file
        """
        with self.assertRaises(FileNotFoundError):
            self._logger.debug(str(VersionPyVersion(_get_full_path('a_witch'))))

    def _assert_good_package(self, project, expected_version):
        """Assert version as expected"""
        target = VersionPyVersion(_get_full_path(project))
        self._assert_version_pattern(target)
        self.assertEqual(expected_version, str(target), 'Wrong version read')


if __name__ == '__main__':
    unittest.main()
