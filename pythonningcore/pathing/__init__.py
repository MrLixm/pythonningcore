"""
TODO: this should be moved to its own module later
"""

import errno
import logging
import os
import platform
import shutil
import stat
import subprocess

import pythonningcore.py23.helpers

from . import c

if pythonningcore.py23.helpers.isModuleAvailable("typing"):
    from typing import Optional
if pythonningcore.py23.helpers.isModuleAvailable("pathlib"):
    from pathlib import Path

__all__ = ("clearDir",)

logger = logging.getLogger("{}".format(c.abr))


def clearDir(path, force=True):
    # type: (str | Path, bool) -> None
    """
    Completely delete the given directory and its content.

    SRC: https://stackoverflow.com/q/39566812/13806195

    Args:
        force: if True delete also the read only file that would fail otherwise.
        path: string or any object that once converted to string represents
            a directory path. The path MIGHT not exist.
    """
    path = str(path)
    if not os.path.exists(path):
        return

    def handleRemoveReadonly(func, _path, exc):
        """
        SRC: https://stackoverflow.com/a/1214935/13806195
        """
        excvalue = exc[1]
        if func in (os.rmdir, os.remove, os.unlink) and excvalue.errno == errno.EACCES:
            os.chmod(_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
            func(_path)
        else:
            raise

    if force:
        shutil.rmtree(path, ignore_errors=False, onerror=handleRemoveReadonly)
    else:
        shutil.rmtree(path, ignore_errors=False)

    return


def createSymLink(source, target):
    # type: (str | Path, str | Path) -> Optional[str]
    """
    Create the symlink of the active developed version in the /publish directory.
    Only supported on Windows for now.

    Args:
        source:
        target:

    Returns:
        path to the created symlink

    Raises:
        AssertionError: if the symlink was not created
        NotImplementedError: if the current OS is not supported
    """
    if platform.system() != "Windows":
        raise NotImplementedError(
            "Current OS {} used is not supported.".format(platform.system())
        )

    source = str(source)
    target = str(target)

    if os.path.exists(target):
        logger.warning(
            "[createSymLink] target symlink dir already exists: {}".format(target)
        )
        return

    subprocess.call("mklink /D {} {}".format(target, source))
    assert os.path.exists(
        target
    ), "Symlink not created ! Source[{}] to target[{}]".format(source, target)
    logger.info("[createSymLink] Finished. Created at {}".format(target))
    return target
