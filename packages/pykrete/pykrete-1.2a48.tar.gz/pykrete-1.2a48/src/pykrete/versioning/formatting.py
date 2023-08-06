"""
Feature revision types
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
from . import Version


class Formatting:
    """Version formatter"""
    @property
    def for_python(self):
        """Create python version string for the formatted version

        :return: The version string
        """
        return ''.join(
            [
                str(self._version.major),
                '.',
                str(self._version.minor),
                ['pa', 'a', 'b', 'rc', '.'][self._version.revision_type.value],
                str(self._version.build),
            ])

    def __init__(self, version: Version):
        """Initialize this instance to format the specified version

        :param version: Version to be formatted
        """
        self._version = version
