"""
Feature revision types
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
from enum import Enum


class RevisionType(Enum):
    """Revision type enumeration"""
    PreAlpha = 0
    """Feature still in bring-up phase, mostly not testable"""

    Alpha = 1
    """Feature implementation in progress, testing enabled"""

    Beta = 2
    """Feature complete, fully testable"""

    RC = 3
    """Feature finalized, integration candidate"""

    Release = 4
    """Feature ready for production"""
