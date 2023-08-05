"""
Visitor pattern base class
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""


class Target:
    """Visitor target base class"""

    def accept(self, visitor):
        """Accept a visitor

        :param visitor: visitor
        """
        return visitor.visit(self)
