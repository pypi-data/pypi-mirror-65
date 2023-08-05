"""
Repository change aggregation
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""


class Change:
    """Used for collecting and reviewing repository changes"""
    @property
    def log(self):
        """
        :return: change log (titles)
        """
        return self.__join_str_list(self._log)

    @property
    def details(self):
        """
        :return: change details (descriptive messages)
        """
        return self.__join_str_list(self._details)

    def __init__(self):
        """Initializes this instance to an empty change"""
        self._log = []
        self._details = []

    def append_log(self, log):
        """Appends to the change log

        :param log: log to append (can be a string, list or tuple of strings)
        """
        self.__flatten_convert_and_append_to_list(self._log, log, str)

    def append_details(self, details):
        """Appends to the change details

        :param details: log to append (can be a string, list or tuple of strings)
        """
        self.__flatten_convert_and_append_to_list(self._details, details, str)

    def __str__(self):
        """returns a string representation of this change"""
        return '\n====\n'.join([
            f'Log:\n{self.log}',
            f'Details:\n{self.details}',
        ])

    @staticmethod
    def __join_str_list(str_list):
        return '\n'.join(str_list)

    @staticmethod
    def __flatten_convert_and_append_to_list(a_list, item, converter):
        items = item if isinstance(item, (list, tuple)) else [item]
        a_list.extend([converter(part) for part in items])
