"""

"""
import pythonningcore.py23.helpers

if pythonningcore.py23.helpers.typing_available:
    from typing import Sequence, Optional, AnyStr


def formatSubprocessError(code, args, error):
    # type: (int, Sequence[AnyStr], Optional[bytes]) -> str
    """
    Args:
        code: exit code from process.poll()
        args: args Popen() was called with
        error: error data from process.communicate()

    Returns:
        human readable string
    """
    return "Subprocess <{}> returned with non-zero exit status {}:\n {}".format(
        " ".join(args), code, error
    )
