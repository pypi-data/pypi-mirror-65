"""
Visitor pattern base class
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
from abc import ABCMeta, abstractmethod


class Visitor(metaclass=ABCMeta):
    """Visitor pattern base class"""

    @abstractmethod
    def visit(self, target):
        """Visit this instance

        :param target: visited target
        """
