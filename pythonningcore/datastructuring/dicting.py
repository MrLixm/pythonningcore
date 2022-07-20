"""
"""
from __future__ import annotations

import json
import logging

import pythonningcore.py23.helpers

from . import c

if pythonningcore.py23.helpers.isModuleAvailable("pathlib"):
    from pathlib import Path
if pythonningcore.py23.helpers.isModuleAvailable("typing"):
    from typing import Any

__all__ = ("DiskDict",)

logger = logging.getLogger(f"{c.abr}.dicting")


class DiskDict:
    """
    Looks like a dict but is not one. Data is stored/retrieved from a disk file,
    usually a .json.

    Trying to set a key while the instance is set to ``read_only=True`` will not raise
    error but will not apply any change.

    Args:
        file_path:
            absolute path to the FILE storing the dict. MIGHT not exist yet.
            Expected to be json for now.
        read_only:
            True to prevent writing anything to the file on disk.
    """

    def __init__(self, file_path, read_only=False):
        # type: (str | Path, bool) -> None
        self.path = str(file_path)  # type: str
        self.read_only = read_only  # type: bool
        logger.debug(
            "[{}][__init__] Finished with path={}"
            "".format(self.__class__.__name__, self.path)
        )
        return

    def __getitem__(self, item):
        # type: (str) -> Any
        """
        Args:
            item: key that MUST exists in the dict

        Returns:
            value of the given key
        """
        return self._read()[item]

    def __setitem__(self, key, value):
        # type: (str, Any) -> None
        new = self._read()
        new[key] = value
        self._write(new)
        logger.debug(
            "[{}][set] modified {}={}".format(self.__class__.__name__, key, value)
        )
        return

    def __str__(self):
        # type: () -> str
        return json.dumps(self._read(), indent=4)

    def _read(self):
        # type: () -> dict
        with open(self.path, "r") as file:
            content = json.load(file)
        return content

    def _write(self, content):
        # type: (dict) -> None
        if self.read_only:
            return

        with open(self.path, "w") as file:
            json.dump(content, file, indent=4)
        return

    def debug(self, log=False):
        # type: (bool) -> str
        """
        Return a message that can be used for debugging purposes.
        If log=True also log it with the module logger (at DEBUG level)
        """
        msg = "[{}][debug] {}:\n{}".format(
            self.__class__.__name__,
            self.path,
            json.dumps(self._read(), indent=4),
        )
        if log:
            logger.debug(msg)
        return msg

    def get(self, key, default=None):
        # type: (str, Any | None) -> Any
        try:
            out = self[key]
        except KeyError:
            out = default
        return out

    def set(self, key, value):
        # type: (str, Any) -> None
        self[key] = value
