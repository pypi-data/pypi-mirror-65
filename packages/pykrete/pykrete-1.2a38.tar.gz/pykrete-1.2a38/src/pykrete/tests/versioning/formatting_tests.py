"""
Pykrete versioning.formatting tests
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""

import unittest
import logging
from pykrete.versioning import Version, Formatting, RevisionType


class PykreteVersioningFormattingTestCase(unittest.TestCase):
    """Unit tests for pykrete's versioning module's Formatting class
    """

    _logger = logging.getLogger(__name__)

    def test_release_version_formatting(self):
        """Verifies formatting release versions"""
        target = Formatting(Version(1, 2, 4, 3, RevisionType.Release))
        self.assertEqual('1.2.3', target.for_python, 'wrong python format')

    def test_rc_version_formatting(self):
        """Verifies formatting rc versions"""
        target = Formatting(Version(11, 22, 3, 44, RevisionType.RC))
        self.assertEqual('11.22rc44', target.for_python, 'wrong python format')

    def test_beta_version_formatting(self):
        """Verifies formatting beta versions"""
        target = Formatting(Version(12, 23, 2, 34, RevisionType.Beta))
        self.assertEqual('12.23b34', target.for_python, 'wrong python format')

    def test_alpha_version_formatting(self):
        """Verifies formatting alpha versions"""
        target = Formatting(Version(21, 32, 1, 43, RevisionType.Alpha))
        self.assertEqual('21.32a43', target.for_python, 'wrong python format')

    def test_pre_alpha_version_formatting(self):
        """Verifies formatting pre-alpha versions"""
        target = Formatting(Version(111, 222, 0, 333, RevisionType.PreAlpha))
        self.assertEqual('111.222pa333', target.for_python, 'wrong python format')


if __name__ == '__main__':
    unittest.main()
