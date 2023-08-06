"""
Version information manager
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
from abc import abstractmethod


class Version:
    """Represents a package version
    """

    @property
    def major(self):
        """
        :return: Major part of the version
        """
        return self._major

    @property
    def minor(self):
        """
        :return: Minor part of the version
        """
        return self._minor

    @property
    def revision(self):
        """
        :return: Revision part of the version
        """
        return self._revision

    @property
    def build(self):
        """
        :return: Build part of the version
        """
        return self._build

    @property
    def revision_type(self):
        """
        :return: Revision type of the version
        """
        return self._revision_type

    def __init__(self, *args, **kwargs):
        """Initializes this instance with the specified values

        :param args: one of:
            - a single tuple of (major, minor, revision, build, revision_type)
            - these five values individually
            - a Version object
        :param kwargs: specify values with labels: major, minor, revision, build, revision_type
        """
        (major, minor, revision, build, revision_type) = \
            Version.__get_version_parts_from_args(args) if args \
            else Version.__get_version_parts_from_kwargs(kwargs)
        self._major = major
        self._minor = minor
        self._revision = revision
        self._build = build
        self._revision_type = revision_type

    @abstractmethod
    def apply(self):
        """Apply this version to the relevant environment
        """

    def __str__(self):
        return f'{self.major}.{self.minor}.{self.revision}.{self.build} {self.revision_type.name}'

    def __ge__(self, other):
        return not self.__lt__(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __lt__(self, other):
        for comparison in self.__make_comparisons(other):
            if comparison[0] < comparison[1]:
                return True
            if comparison[0] > comparison[1]:
                return False
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        for comparison in self.__make_comparisons(other):
            if comparison[0] != comparison[1]:
                return False
        return self.revision_type == other.revision_type

    def __make_comparisons(self, other):
        comparisons = [(self.major, other.major), (self.minor, other.minor),
                       (self.revision, other.revision), (self.build, other.build)]
        return comparisons

    @staticmethod
    def __get_version_parts_from_kwargs(kwargs):
        return (kwargs['major'], kwargs['minor'], kwargs['revision'], kwargs['build'],
                kwargs['revision_type'])

    @staticmethod
    def __get_version_parts_from_args(args):
        first_arg = args[0]
        first_arg_type = type(first_arg)
        if first_arg_type == tuple:
            return first_arg
        if issubclass(first_arg_type, Version):
            return (first_arg.major, first_arg.minor, first_arg.revision, first_arg.build,
                    first_arg.revision_type)
        return args
