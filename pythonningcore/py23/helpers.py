"""
Objects helping to maintain python 2 AND 3 compatibility
"""
import sys

typing_available = sys.version_info[0] >= 3 and sys.version_info[1] >= 5
"""
Determine if the typing module can be safely imported. True = safe.
Example::

    >>> if typing_available:
    >>>     from typing import List, Union
"""
