"""
Pykrete test helpers
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""

import os


def get_full_path(project, is_with_src_root=False):
    """Compose relative paths for tests

    :param project: simulated project
    :param is_with_src_root: should this repo's 'src' root be included
    :return: Composed path
    """
    root = 'pykrete'
    if is_with_src_root:
        root = os.path.join('src', root)
    return os.path.join(root, 'tests', 'src', project)
