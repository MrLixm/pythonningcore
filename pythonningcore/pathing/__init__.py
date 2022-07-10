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

__all__ = (
    "clearDir",
    "copyDir",
    "createSymLink",
)

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


def copyDir(source, target, mirror=False):
    # type: (str|Path, str|Path, bool) -> None
    """

    Args:
        source:
        target:
        mirror:
            (destructive) if True overwrite ALL the target dir content with source's one.

    Returns:

    """
    if platform.system() != "Windows":
        raise NotImplementedError(
            "Current OS {} used is not supported.".format(platform.system())
        )

    args = [
        "robocopy",
        str(source),
        str(target),
        # copy option
        "/E",
        "/MIR" if mirror else "",  # overwrite the target dir with source content
        # logging options
        "/nfl",  # no file names are not to be logged.
        "/ndl",  # no directory names logged.
        "/np",  # no progress of the copying operation
        "/njh",  # no job header.
        # "/njs",  # no job summary.
    ]
    logger.info("[copyDir] copying <{}> to <{}> ...".format(source, target))
    subprocess.call(args)
    logger.info("[copyDir] Finished.")
    return


def createSymLink(source_path, target_path, hard=False):
    # type: (str | Path, str | Path, bool) -> str
    """
    Create and make the target_path a virtual copy (link) of source_path.

    A hard link makes it appear as though the file or folder actually exists at
    the location of the symbolic link while soft just redirects.

    Args:
        source_path: file or directory path, MUST exist
        target_path: file or directory path, MUST not exist
        hard: True to create a hard link instead of a soft link.

    Returns:
        path to the created symlink (target_path)

    Raises:
        AssertionError: if the symlink was not created
        NotImplementedError: if the current OS is not supported
    """
    if platform.system() != "Windows":
        raise NotImplementedError(
            "Current OS {} used is not supported.".format(platform.system())
        )

    source_path = str(source_path)
    target_path = str(target_path)

    if os.path.isdir(source_path):
        command_option = "/J" if hard else "/D"
    else:
        command_option = "/H" if hard else ""

    assert not os.path.exists(
        target_path
    ), "[createSymLink] target symlink already exists: {}".format(target_path)

    command = ["mklink", command_option, target_path, source_path]
    subprocess.call(command)

    assert os.path.exists(target_path), "Symlink not created for {} --> {}".format(
        source_path, target_path
    )

    logger.info("[createSymLink] Finished. Created at {}".format(target_path))
    return target_path
