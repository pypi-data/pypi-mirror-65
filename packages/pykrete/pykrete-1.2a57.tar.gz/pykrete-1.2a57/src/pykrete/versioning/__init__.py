"""
Version information managers
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
from .ci_version import CiVersion
from .revision_type import RevisionType
from .version import Version
from .version_py_version import VersionPyVersion, make_python_root_version_file_path
from .tag_version import TagVersion
from .formatting import Formatting

__all__ = ['CiVersion', 'RevisionType', 'Version', 'VersionPyVersion', 'TagVersion', 'Formatting',
           'make_python_root_version_file_path']
