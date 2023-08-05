"""
Environment argument handling
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import os


def environ(var_name, role=None):
    """Gets an environment variable's value

    :param var_name: The variable's name
    :param role: The variable's role (optional)
    :return: The variable's value
    :exception IOError: The variable is not defined in the environment and role is specified
    """
    try:
        return os.environ[var_name]
    except KeyError:
        if role:
            raise IOError(f'Build requires that the "{var_name}"'
                          f' environment variable is set to {role}')
        return None
