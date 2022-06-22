import errno
import os
import shutil
import stat

import pythonningcore.py23.helpers

if pythonningcore.py23.helpers.typing_available:
    import typing

__all__ = ("clearDir",)


def clearDir(path, force=True):
    # type: (str, bool) -> None
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
