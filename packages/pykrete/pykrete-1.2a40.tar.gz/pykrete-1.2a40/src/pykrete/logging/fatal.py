"""
Fatal issue handler
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import logging


def fatal(message, exception_class=None):
    """Log and raise a fatal error

    :param message: error message
    :param exception_class: Exception class (optional, use Exception if not supplied)
    :exception: always raises an exception of the specified type with the specified message
    """
    logging.getLogger(__name__).error(message)
    raise (exception_class if exception_class else Exception)(message)
