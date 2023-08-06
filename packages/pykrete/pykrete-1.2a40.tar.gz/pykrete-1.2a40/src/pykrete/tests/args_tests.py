"""
Pykrete Args tests
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import logging
import unittest
import argparse
from pykrete.args import build_version, exiting_file, yes_or_no, environ, CiIo


class PykreteArgsTestCase(unittest.TestCase):
    """Unit tests for pykrete's args module
    """

    _logger = logging.getLogger(__name__)

    def test_build_version_good(self):
        """Verifies correct parsing of a legal version
        """
        source = '1.2.3.4'
        version = build_version(source)
        self.assertEqual(version.string, source, 'read version differs from source')
        self._logger.debug(':'.join(version.groups()[1:4]))

    def test_build_version_short(self):
        """Verifies rejection of a short version
        """
        with self.assertRaises(argparse.ArgumentTypeError):
            self._logger.debug(build_version('1.2.3'))

    def test_build_version_bad(self):
        """Verifies rejection of a non-version
        """
        with self.assertRaises(argparse.ArgumentTypeError):
            self._logger.debug(build_version('Blue. No, yellOOOOOOOW!!'))

    def test_existing_file_good(self):
        """Verifies acceptance of an existing file
        """
        source = 'README.md'
        self.assertEqual(exiting_file(source), source, 'read file name differs from source')

    def test_existing_file_bad(self):
        """Verifies rejection of a non-existing file
        """
        with self.assertRaises(argparse.ArgumentTypeError):
            self._logger.debug(exiting_file('no_such_file.txt'))

    def test_yes_no_good(self):
        """Verifies correct parsing of yes/no answers
        """
        cases = {True: ['yes', 'Yes', 'YES'], False: ['no', 'No', 'NO']}
        for key, sources in cases.items():
            for source in sources:
                self.assertEqual(key, yes_or_no(source), f'{source} not {key}')

    def test_yes_no_bad(self):
        """Verifies rejection of a non-yes/no answer
        """
        with self.assertRaises(argparse.ArgumentTypeError):
            self._logger.debug(yes_or_no('Huh? I don\'t know that! EEEEEEAAAARRGH!!!'))

    def test_environ_existing(self):
        """Verifies reading existing environment variable
        """
        self._logger.debug('Read path: %s', environ('PATH', 'search path'))

    def test_environ_non_existing_without_role(self):
        """Verifies reading allowed non-existing environment variable
        """
        self._logger.debug('Read non-existing: %s', environ('NO_IM_NOT'))

    def test_environ_non_existing(self):
        """Verifies attempting to read not-allowed non-existing environment variable raises an error
        """
        with self.assertRaises(IOError):
            self._logger.debug('Read non-existing: %s',
                               environ('ITS_JUST_A_FLESH_WOUND',
                                       'Look, you stupid b***ard, you''ve got no arms left!'))

    def test_ciio_existing(self):
        """Verifies reading existing environment variable
        """
        part = 'part1'
        target = CiIo(ci_spec={part: 'PATH'})
        self._logger.debug('Read path: %s', target.read_env(part))

    def test_ciio_non_existing_with_non_false_default(self):
        """Verifies reading default non-False non-existing environment variable
        """
        part = 'part2'
        target = CiIo(ci_spec={part: 'OH_YES_IT_IS'})
        self._logger.debug('Read non-existing: %s', target.read_env(part, 'Oh no it isn''t'))

    def test_ciio_non_existing_with_false_default(self):
        """Verifies reading default False non-existing environment variable
        """
        part = 'part3'
        target = CiIo(ci_spec={part: 'OH_YES_IT_IS'})
        self._logger.debug('Read non-existing: %s', target.read_env(part, False))

    def test_ciio_non_existing_without_default(self):
        """Verifies attempting to read no-default non-existing environment variable raises an error
        """
        part = 'part4'
        target = CiIo(ci_spec={part: 'OH_YES_IT_IS'})
        with self.assertRaises(IOError):
            self._logger.debug('Read non-existing: %s', target.read_env(part))


if __name__ == '__main__':
    unittest.main()
