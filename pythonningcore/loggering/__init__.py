"""
TODO: this should be moved to its own module later
"""
import logging
import sys

import pythonningcore.py23.helpers

if pythonningcore.py23.helpers.isModuleAvailable("typing"):
    from typing import List, Tuple, Sequence

__all__ = ("setupLogger", "setupLoggingFor")


def setupLogger(logger_name, level):
    # type: (str, int) -> logging.Logger
    """

    Args:
        logger_name: name of the logger to set up via getLogger()
        level: minimum level of message this logger should catch

    Returns:
        logger that has been set up
    """

    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    if not logger.handlers:
        # create a file handler
        handler = logging.StreamHandler(stream=sys.stdout)
        handler.setLevel(logging.DEBUG)
        # create a logging format
        formatter = logging.Formatter(
            "%(asctime)s - [%(levelname)7s][%(name)30s]%(message)s",
            datefmt="%H:%M:%S",
        )
        handler.setFormatter(formatter)
        # add the file handler to the logger
        logger.addHandler(handler)

    return logger


def setupLoggingFor(loggers, level=logging.DEBUG):
    # type: (Sequence[str | Tuple[str, int]], int) -> None
    """

    Args:
        loggers: list of logger names to setup with an optional level
        level: optional if level is specified per logger in the logegrs arg
    """

    for loggerdata in loggers:

        if isinstance(loggerdata, tuple):
            setupLogger(logger_name=loggerdata[0], level=loggerdata[1])
        else:
            setupLogger(logger_name=loggerdata, level=level)

    return
