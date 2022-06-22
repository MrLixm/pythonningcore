"""
TODO: this should be moved to its own module later
"""
import logging
import subprocess

from pythonningcore.py23.helpers import typing_available
from . import c

if typing_available:
    from typing import Sequence, Optional, AnyStr, List, Any

__all__ = ("formatSubprocessError", "callBasic")

logger = logging.getLogger("{}".format(c.abr))


def formatSubprocessError(code, args, error):
    # type: (int, Sequence[AnyStr], Optional[AnyStr]) -> str
    """
    Args:
        code: exit code from process.poll()
        args: args Popen() was called with
        error: error data from process.communicate()

    Returns:
        human readable string
    """
    return "Subprocess <{}> returned with non-zero exit status {}:\n {}".format(
        " ".join(args).encode("ascii"), code, error
    )


def callBasic(command, error_tip=None, **kwargs):
    # type: (List[str], Optional[str], Any) -> AnyStr
    """
    Basic implementation of subprocess.Popen() that handle errors.

    Args:
        command: command to use for calling Popen.
        error_tip: an additional message to specify after the error.
        kwargs: kwargs are passed to subprocess.Popen

    Returns:
        result of the subprocess call from stdout

    Raises:
        RuntimeError: if process returned non-zero exit code.
    """
    process = subprocess.Popen(command, stdout=subprocess.PIPE, **kwargs)
    stdoutdata, stderrdata = process.communicate()
    if process.returncode != 0:
        msg = formatSubprocessError(process.poll(), process.args, stderrdata)
        if error_tip:
            msg += "\n"
            msg += error_tip
        raise RuntimeError(msg)

    logger.debug(
        "[callBasic] Finished. [{}][result={}]"
        "".format(" ".join(command).encode("ascii"), stdoutdata)
    )
    return stdoutdata
