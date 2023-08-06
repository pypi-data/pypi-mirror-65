"""
Pykrete versioning.ci_version tests
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""

import unittest
import logging
from pykrete.args import CiIo
from pykrete.versioning import CiVersion, RevisionType
from .versioning import PykreteVersioningTestCase


class PykreteVersioningCiVersionTestCase(PykreteVersioningTestCase):
    """Unit tests for pykrete's versioning module's CiVersion class
    """

    _logger = logging.getLogger(__name__)
    _local_release = {
        'major version': '1',
        'minor version': '2',
        'build version': '3',
        'branch name': 'master',
        'merge request title': 'None',
        'job name': 'some_job'}
    _local_rc_master_rc_job = {
        'major version': '11',
        'minor version': '22',
        'build version': '33',
        'branch name': 'master',
        'merge request title': 'None',
        'job name': 'some_rc_job'}
    _local_rc_merge_request = {
        'major version': '12',
        'minor version': '23',
        'build version': '34',
        'branch name': 'custom',
        'merge request title': 'title'}
    _local_beta = {
        'major version': '111',
        'minor version': '222',
        'build version': '333',
        'branch name': 'custom',
        'merge request title': 'WIP: title'}
    _local_alpha = {
        'major version': '123',
        'minor version': '456',
        'build version': '789',
        'branch name': 'custom',
        'merge request title': 'None'}

    def test_ci_version_local_release(self):
        """Verifies handling of simulated CI-environment's release version"""
        self._assert_ci_version_local(
            spec=self._local_release,
            expected_revision_type=RevisionType.Release,
            expected_revision=4)

    def test_ci_version_local_rc_master_rc_job(self):
        """Verifies handling of simulated CI-environment's release-candidate version"""
        self._assert_ci_version_local(
            spec=self._local_rc_master_rc_job,
            expected_revision_type=RevisionType.RC,
            expected_revision=3)

    def test_ci_version_local_rc_merge_request(self):
        """Verifies handling of simulated CI-environment's release-candidate version"""
        self._assert_ci_version_local(
            spec=self._local_rc_merge_request,
            expected_revision_type=RevisionType.RC,
            expected_revision=3)

    def test_ci_version_local_beta(self):
        """Verifies handling of simulated CI-environment's beta version"""
        self._assert_ci_version_local(
            spec=self._local_beta,
            expected_revision_type=RevisionType.Beta,
            expected_revision=2)

    def test_ci_version_local_alpha(self):
        """Verifies handling of simulated CI-environment's alpha version"""
        self._assert_ci_version_local(
            spec=self._local_alpha,
            expected_revision_type=RevisionType.Alpha,
            expected_revision=1)

    def _assert_ci_version_local(self, spec, expected_revision_type, expected_revision):
        target = CiVersion(CiIo(self._echo, spec))
        self._assert_version_pattern(target)
        self._assert_spec(spec, target)
        self.assertEqual(expected_revision_type, target.revision_type, "Wrong revision type")
        self.assertEqual(expected_revision, target.revision, "Wrong revision")

    def _assert_spec(self, spec, target):
        parts = {'major': target.major, 'minor': target.minor, 'build': target.build}
        for key, value in parts.items():
            self.assertTrue(isinstance(value, int), f'{key} is not int')
            self.assertEqual(int(spec[f'{key} version']), value, f'Wrong {key} version')


if __name__ == '__main__':
    unittest.main()
