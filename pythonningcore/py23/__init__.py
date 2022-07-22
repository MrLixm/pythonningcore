import sys

__all__ = (
    "helpers",
    "Enum",
    "IntEnum",
)

from . import helpers

# enum was introduced in python 3.4
if sys.version_info[0] == 2 or sys.version_info[0] == 3 and sys.version_info[1] <= 3:
    from .enum import Enum, IntEnum
else:
    from enum import Enum, IntEnum
