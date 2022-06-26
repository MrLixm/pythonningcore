"""
Objects helping to maintain python 2 AND 3 compatibility
"""
import pkgutil

__all__ = ("isModuleAvailable",)


def isModuleAvailable(module_name):
    # type: (str) -> bool
    """
    Check if the given module name might be imported in the current context
    without raising error. This might still raise error.

    Args:
        module_name: individual module name (no dot)

    Returns:
        True if the module can be imported in the current context.
    """

    available = False
    if pkgutil.find_loader(module_name):
        available = True

    return available
