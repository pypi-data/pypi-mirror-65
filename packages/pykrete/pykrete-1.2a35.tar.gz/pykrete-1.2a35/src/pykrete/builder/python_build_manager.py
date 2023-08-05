"""
Python build manager
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import subprocess
import shutil
import logging
from pykrete.packages import install_python_packages
from pykrete.args import environ
from pykrete.versioning import VersionPyVersion
from pykrete.patterns import write_lines
from .build_manager import BuildManager


class PythonBuildManager(BuildManager):
    """Manages building a python package"""

    _logger = logging.getLogger(__name__)

    def _clean_distribution(self):
        """Removes previous distribution files"""
        self._logger.debug('Deleting previous distribution')
        shutil.rmtree('dist', ignore_errors=True)

    def _upload(self, is_release):
        """Uploads the package

        :param is_release: flag this package as release
        """
        self._logger.debug('Uploading %s', self._project)
        install_python_packages('twine')
        self._make_pypirc()
        self._run_build(
            'Uploading package...',
            'twine', '--project', self._project)
        if is_release:
            self._version.apply()

    def _build(self):
        """Performs the actual build using build.py"""
        self._logger.debug('Building %s', self._project)
        install_python_packages('setuptools', 'wheel')
        self._run_build(
            'Building package...',
            'check', 'sdist', 'bdist_wheel')

    def _set_package_version(self):
        """Sets the package version in the project's version file"""
        VersionPyVersion(self._project, self._version).apply()

    def _run_build(self, message, *args):
        """Runs build.py

        :param message: pre-run debug message
        :param args: build.py argument
        """
        self._logger.debug(message)
        subprocess.check_call(['python', 'build.py'] + list(args))

    def _make_pypirc(self):
        """Generates the pypirc file required for upload, from GitLab environment variables:
        username: PYPI_USER
        password: PYPI_PASSWORD
        """
        self._logger.debug('Prepping pypirc')
        path = environ('pypirc')
        with open(path if path else 'pypirc', 'w') as pypirc:
            write_lines(pypirc, self._make_pypirc_lines())

    @staticmethod
    def _make_pypirc_lines():
        return [
            '[distutils]',
            'index-servers =',
            '    pypi',
            '',
            '[pypi]',
            '    username: ' + environ('PYPI_USER', 'the Pypi repository user name'),
            '    password: ' + environ('PYPI_PASSWORD', 'the Pypi repository password/API-key'),
        ]
