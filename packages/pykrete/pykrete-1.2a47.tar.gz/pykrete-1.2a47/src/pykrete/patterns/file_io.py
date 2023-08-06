"""
Pattern and common classes
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""


def write_lines(file, lines):
    """Write lines to file

    :param file: target file
    :param lines: lines to write
    """
    file.writelines('\n'.join(lines) + '\n')
