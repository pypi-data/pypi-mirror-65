"""
Python package installation
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import logging
import subprocess


def install_python_packages(*args):
    """Installs the specified pip packages

    :param args: The packages to install
    """
    packages = list(args)
    logging.getLogger(__name__).debug('Installing packages %s', packages)
    subprocess.check_call(['python', '-m', 'pip', 'install'] + packages)
