"""
Credentials state
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
from enum import Enum


class State(Enum):
    """Credentials state"""

    NotInitialized = 0
    """Credentials not initialized"""

    Enabled = 1
    """Credentials enabled"""

    Disabled = 2
    """Credentials disabled"""
