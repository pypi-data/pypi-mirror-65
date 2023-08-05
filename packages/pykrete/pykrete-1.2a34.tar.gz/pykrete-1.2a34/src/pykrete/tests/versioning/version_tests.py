"""
Pykrete versioning.version tests
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import unittest
import logging
from pykrete.versioning import RevisionType, Version
from .versioning import PykreteVersioningTestCase


class PykreteVersioningVersionTestCase(PykreteVersioningTestCase):
    """Unit tests for pykrete's versioning module's Version class
    """

    _logger = logging.getLogger(__name__)

    def test_version_from_tuple(self):
        """Verifies creation of version from tuple"""
        target = Version((1, 2, 3, 4, RevisionType.Alpha))
        self._assert_version(target, (1, 2, 3, 4, RevisionType.Alpha))

    def test_version_from_args(self):
        """Verifies creation of version from arguments"""
        target = Version(12, 23, 34, 45, RevisionType.Beta)
        self._assert_version(target, (12, 23, 34, 45, RevisionType.Beta))

    def test_version_from_version(self):
        """Verifies creation of version from another version object"""
        source = Version(111, 222, 333, 444, RevisionType.RC)
        target = Version(source)
        self._assert_version(target, (111, 222, 333, 444, RevisionType.RC))
        self.assertEqual(source, target, "Version objects aren't equal")

    def test_version_from_kwargs(self):
        """Verifies creation of version from named arguments"""
        target = Version(major=21, minor=32, revision=43, revision_type=RevisionType.Release,
                         build=54)
        self._assert_version(target, (21, 32, 43, 54, RevisionType.Release))

    def test_version_comparison(self):
        """Verifies ordering of version objects"""
        self.assertTrue(
            Version(1, 0, 0, 0, RevisionType.RC) >= Version(0, 99, 99, 99, RevisionType.RC),
            'Major comparison failed')
        self.assertTrue(
            Version(1, 1, 0, 0, RevisionType.RC) >= Version(1, 0, 99, 99, RevisionType.RC),
            'Minor comparison failed')
        self.assertTrue(
            Version(1, 1, 1, 0, RevisionType.RC) >= Version(1, 1, 0, 99, RevisionType.RC),
            'Revision comparison failed')
        self.assertTrue(
            Version(1, 1, 1, 1, RevisionType.Alpha) >= Version(1, 1, 1, 0, RevisionType.RC),
            'Minor comparison failed')

    def test_version_ordering(self):
        """Verifies ordering of version objects"""
        source = [Version(1, 2, 3, 4, RevisionType.Release),
                  Version(1, 2, 3, 1, RevisionType.Release),
                  Version(1, 2, 3, 4, RevisionType.Release),
                  Version(1, 2, 1, 3, RevisionType.Release),
                  Version(1, 0, 2, 3, RevisionType.Release),
                  Version(0, 1, 2, 3, RevisionType.Release),
                  Version(11, 22, 33, 44, RevisionType.Release)]
        target = sorted(source)
        self._logger.debug('\n'.join(str(version) for version in target))
        expected = [Version(0, 1, 2, 3, RevisionType.Release),
                    Version(1, 0, 2, 3, RevisionType.Release),
                    Version(1, 2, 1, 3, RevisionType.Release),
                    Version(1, 2, 3, 1, RevisionType.Release),
                    Version(1, 2, 3, 4, RevisionType.Release),
                    Version(1, 2, 3, 4, RevisionType.Release),
                    Version(11, 22, 33, 44, RevisionType.Release)]
        for comparison in zip(expected, target):
            self.assertEqual(comparison[0], comparison[1], "Wrong ordering")

    def _assert_version(self, target, expected):
        (major, minor, revision, build, revision_type) = expected
        self._assert_version_pattern(target)
        self.assertEqual(major, target.major, "Wrong major version")
        self.assertEqual(minor, target.minor, "Wrong minor version")
        self.assertEqual(revision, target.revision, "Wrong revision")
        self.assertEqual(build, target.build, "Wrong build number")
        self.assertEqual(revision_type, target.revision_type, "Wrong revision type")


if __name__ == '__main__':
    unittest.main()
