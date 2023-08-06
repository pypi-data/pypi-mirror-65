"""
distutils command for building local GIT project
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
from distutils.log import INFO
from distutils.cmd import Command
from pykrete.versioning import TagVersion
from pykrete.builder import PythonBuildManager
from pykrete.repo import Git
from pykrete.credentials import CiSshPrivateKey


class BuildGitSshTag(Command):
    """A custom command for building local GIT project where SSH is used for pushing,
     and the version is tag-based
    """
    description = 'Build the current GIT project'
    user_options = []

    def initialize_options(self):
        """Set default values for options"""

    def finalize_options(self):
        """Post-process received options"""

    def run(self):
        """Performs the build"""
        with CiSshPrivateKey() as key:
            repo = Git(credentials=key)
            version = TagVersion(repo=repo)
            manager = PythonBuildManager(version)
            self.announce(str(manager), level=INFO)
            manager.run()
        self.announce('Build succeeded', level=INFO)
