"""

"""
from __future__ import annotations
import base64
import os
from pythonningcore import py23

if py23.helpers.isModuleAvailable("typing"):
    from typing import Callable

__all__ = (
    "IdentifierTypes",
    "generateIdentifier",
)


def byteToStr(byte_obj):
    # type: (bytes) -> str
    return byte_obj.decode("utf-8")


def processSizeMultipleOf(default, multiple_of):
    # type: (int, int) -> Callable[[Callable], Callable]
    """
    To use as a decorator.
    Expect a certain type of function that only have a ``size`` parameter of type int.

    Args:
        multiple_of:
        default: default value if size parameter passed is None
    """

    def decorator(func):
        def inner(*args, **kwargs):
            size = args[0] if args else kwargs.get("size")
            if size is None:
                size = default

            assert (
                size % multiple_of == 0
            ), "[{}] Given size <{}> must be a multiple of {}" "".format(
                func, size, multiple_of
            )

            return func(size=size)

        return inner

    return decorator


class IdentifierTypes(py23.Enum):

    caps = 0
    """
    Will generate an identifier with a size being a multiple of 5,
    made only of upper letter and numbers.
    
    ex: 7NIWZ7DN, 4X73WFFW5VTYT3AL, UICCHYRES3UWCPKNVCNA6AKS
    """

    random = 1
    """
    Will generate an identifier with a size being a multiple of 3,
    made of any character including special ones.

    ex: qZJoy+JW, /Gfu1qQ4/w+N, 2/Rs
    """

    urlsafe = 2
    """
    Will generate an identifier with a size being a multiple of 3,
    made of any character that can be found in an url.

    ex: ka60u1Ku4-iK, YvfL_ndeSfXe, M_rr
    """


@processSizeMultipleOf(6, multiple_of=3)
def generateRandomId(size=None):
    # type: (int | None) -> str
    """
    SRC: https://stackoverflow.com/a/6763520/13806195
    """
    key = base64.b64encode(os.urandom(size))
    return byteToStr(key)


@processSizeMultipleOf(6, multiple_of=3)
def generateUrlSafeId(size=None):
    # type: (int | None) -> str
    key = base64.urlsafe_b64encode(os.urandom(size))
    return byteToStr(key)


@processSizeMultipleOf(5, multiple_of=5)
def generateCapsId(size=None):
    # type: (int | None) -> str
    """
    SRC: https://stackoverflow.com/a/6763520/13806195
    """
    key = base64.b32encode(os.urandom(size))
    return byteToStr(key)


def generateIdentifier(id_type, size=None):
    # type: (IdentifierTypes, int) -> str

    if id_type == IdentifierTypes.caps:
        identifier = generateCapsId(size)
    elif id_type == IdentifierTypes.random:
        identifier = generateRandomId(size)
    elif id_type == IdentifierTypes.urlsafe:
        identifier = generateUrlSafeId(size)
    else:
        raise ValueError("Unsupported IdentifierType {}".format(id_type))

    return identifier


if __name__ == "__main__":

    for i in range(25):
        print(generateIdentifier(IdentifierTypes.caps, size=5))
