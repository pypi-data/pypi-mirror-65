"""
Pykrete CI features tests base
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import logging
import unittest


class PykreteCiEchoTestCase(unittest.TestCase):
    """Unit tests base for pykrete's CI dependent features
    """

    _logger = logging.getLogger(__name__)

    def _echo(self, what, who):
        self._logger.debug('CiVersion is reading \'%s\' and will get \'%s\'', who, what)
        return None if what == 'None' else what
