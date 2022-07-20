import os
import sys


class Plateform:
    """
    Utility class to improve upon ``sys.platform``
    """

    ENV_FAKE = "PLATFORM_FAKE"
    """
    Name of the environment variable that can be used to "fake" the platform currently
    active. Value must be one of ``sys.platform``.
    
    It is recommend to override it in the instance and the package's prefix.
    """

    def __repr__(self):
        return self.name

    @property
    def name(self):
        # type: () -> str
        if self.is_linux:
            return "linux"
        elif self.is_mac:
            return "mac"
        elif self.is_windows:
            return "windows"
        else:
            raise OSError("Unsupported plateform {}".format(sys.platform))

    @property
    def source(self):
        return os.environ.get(self.ENV_FAKE) or sys.platform

    @property
    def is_linux(self):
        # type: () -> bool
        return self.source.startswith("linux")

    @property
    def is_mac(self):
        # type: () -> bool
        return self.source.startswith("darwin")

    @property
    def is_windows(self):
        # type: () -> bool
        return self.source in ("win32", "cygwin")
