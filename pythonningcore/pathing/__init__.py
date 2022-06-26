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

    logger.info("[clearDir] Finished for {}".format(path))
    return


def createSymLink(source_dir, target_dir, hard=False):
    # type: (str | Path, str | Path, bool) -> str
    """
    Create and make the target_dir a virtual copy (link) of source_dir.

    A hard link makes it appear as though the file or folder actually exists at
    the location of the symbolic link while soft just redirects.

    Args:
        source_dir: directory path, MUST exist
        target_dir: directory path, MUST not exist
        hard: True to create a hard link instead of a soft link.

    Returns:
        path to the created symlink (target_dir)

    Raises:
        AssertionError: if the symlink was not created
        NotImplementedError: if the current OS is not supported
    """
    if platform.system() != "Windows":
        raise NotImplementedError(
            "Current OS {} used is not supported.".format(platform.system())
        )

    source_dir = str(source_dir)
    target_dir = str(target_dir)

    assert not os.path.exists(
        target_dir
    ), "[createSymLink] target symlink dir already exists: {}".format(target_dir)

    command_option = "/J" if hard else "/D"
    command = ["mklink", command_option, target_dir, source_dir]
    subprocess.call(command)

    assert os.path.exists(target_dir), "Symlink not created for {} --> {}".format(
        source_dir, target_dir
    )

    logger.info("[createSymLink] Finished. Created at {}".format(target_dir))
    return target_dir
