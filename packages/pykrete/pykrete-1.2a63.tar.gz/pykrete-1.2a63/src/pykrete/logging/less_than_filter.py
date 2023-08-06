"""
StdOut and StdErr log maker
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import logging


class LessThanFilter(logging.Filter):
    """Logging filter for messages below a certain level
    """

    def __init__(self, exclusive_maximum, name=""):
        """Initialize this instance to filter messages below the maximum

        :param exclusive_maximum: Exclusive maximum log level
        :param name: filter name (optional)
        """
        super().__init__(name)
        self.max_level = exclusive_maximum

    def filter(self, record):
        """Filter log records

        :param record: log record
        :return: 1 if record is to be shown, 0 otherwise
        """
        return 1 if record.levelno < self.max_level else 0

    def __str__(self):
        return "LessThan " + self.max_level
