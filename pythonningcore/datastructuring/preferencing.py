"""
Define an interface to store & read preferences as commonly used in applications.

The current implementation is based on a flat dict structure with a pair of key:value
(no nested keys).
It is build around DiskDict class API.

The host must implements:
1. a subclass of BaseKey for each key supported
2. a subclass of Preferences that must instance the class created in 1.

Rough graph::

    ┌────────────────────┐
    │PreferencesContainer│
    └─┬────────────────┬─┘
      ├────────────────┤
      │PreferencesFiles│
      ├────────────────┘
      │
      │  ┌───────────┐
      ├─►│Preferences│
      │  ├───────────┘
      │  │
      │  │  ┌───────┐
      └─►└─►│BaseKey│
            └───────┘
"""
from __future__ import annotations

import json
import logging
import os
from abc import ABC, abstractmethod, abstractproperty
from functools import cache

from pythonningcore import py23

from . import c
from . import dicting

if py23.helpers.isModuleAvailable("pathlib"):
    from pathlib import Path
if py23.helpers.isModuleAvailable("typing"):
    from typing import Any, Type

__all__ = (
    "BaseKey",
    "BaseKeyCategories",
    "BasePreferences",
    "BasePreferencesFile",
)

logger = logging.getLogger("{}.preferencing".format(c.abr))


PreferencesContainer = dicting.DiskDict
"""
Base class for directly manipulating data storing preferences on disk.
"""


class BaseKeyCategories(py23.Enum):
    """
    Store the categories from the preferences keys.

    A key can only belongs to a single category. The category is not stored on disk
    and is only assigned in the package when subclass BaseKey.

    Each Enum attribute value correspond to its "pretty name". The string must be
    formatted as per the str.title() method.

    .. You CAN'T set attributes on this class else it can't be subclassed.

    """

    @classmethod
    def __all__(cls):
        return [attr for attr in cls]


class BaseKey(ABC):
    """
    This is use a subclass to define each key that can be found in the preference file.

    Subclassing
    ===========

    A minimal subclass looks like::

        class key_name(PreferenceKey):
            name = "key_name"
            types = (Type, Type, ...)
            default = Any

            def validateValue(self):
                pass

    Where its name MUST not respect PEP8 and just be the same as key's name.

    Args:
        pref_storage: object holding the preferences as key/value pairs.
    """

    # to override in subclass
    name = NotImplemented  # type: str
    category = NotImplemented  # type: BaseKeyCategories
    types = NotImplemented  # type: tuple[Type]
    default = NotImplemented  # type: Any

    def __init__(self, pref_storage):
        # type: (PreferencesContainer) -> None
        self.source = pref_storage  # type: PreferencesContainer

    def __str__(self):
        return "{}={}".format(self.name, self.value)

    @property
    def value(self):
        # type: () -> Any | None
        """
        The key's value in the current preference file.
        """
        return self.source.get(self.name)

    @value.setter
    def value(self, new):
        # type: (Any) -> None
        assert isinstance(new, self.types), (
            "Can't set value, unsupported type passed:\n"
            "  got {}\n   expected one of {}"
            "".format(type(new), self.types)
        )
        self.source.set(self.name, new)

    def validateType(self):
        """
        Raises:
            TypeError: if the current value is not an instance of the expected type(s).
        """
        if isinstance(self.value, self.types):
            return
        raise TypeError(
            "Key <{}> has its value with an unexpected type:\n"
            "   Expected {}\n"
            "    But got {}"
            "".format(self.name, self.types, type(self.value))
        )

    @abstractmethod
    def validateValue(self):
        """
        Must raise if the key in the pref file has an invalid value.
        Recommended to raise a ValueError or an AssertionError
        """
        pass


class BasePreferences(ABC):
    """
    Simple namespace for everything related to peference's keys.

    You can use ``PrefKey.get(keyName)`` to return the class representing the
    given key name.

    subclassing
    ===========

    Only need to implement ``__init__``. You will create a new instance attribute for
    each BaseKey subclass you created.
    """

    @abstractmethod
    def __init__(self, preference_file):
        # type: (BasePreferencesFile) -> None
        pass

    def __repr__(self):
        return json.dumps(self.items(), default=str, indent=4)

    def get(self, key_name):
        # type: (str) -> BaseKey
        """
        Return the class corresponding to the given key name.

        If pref_file is specified, return an instance build with it, else just
        return the class' type. An instance allow you to query the key's value
        and validate it.

        Args:
            key_name: supported key_name

        Returns:
            BaseKey instance
        """
        if key_name not in self.keys():
            raise KeyError("Given key <{}> is not implemented.".format(key_name))
        return self.__getattribute__(key_name)

    @cache
    def values(self):
        # type: () -> list[BaseKey]
        return list(self.__dict__.values())

    @cache
    def keys(self):
        # type: () -> list[str]
        """
        Returns the list of all the key name the pref file must contain.
        """
        return list(self.__dict__.keys())

    @cache
    def items(self):
        # type: () -> list[tuple[str, BaseKey]]
        return list(zip(self.keys(), self.values()))


class BasePreferencesFile(ABC, PreferencesContainer):
    """
    Represents the preferences stored on disk.
    Expose a bunch if methods to save and retrieve those preferences.

    Furthermore, it's possible to use the class attribute syntax to access some keys
    like::
        v = Preferences().ocio_config_default
    └> will return the value of the ``ocio_config_default`` key stored on disk.

    Trying to modify a key while the instance is set to read_only will not raise error
    but will not apply any change.

    subclassing
    ===========

    You just need to implement ``_preference_class`` as a class variable or as a
    property. It must return your subclass of BasePreferences

    Args:
        file_path:
            absolute path to the preference FILE. MIGHT not exist yet. Content must
            be JSON syntax.
        read_only:
            True to prevent writing anything to the file on disk.
    """

    def __init__(self, file_path, read_only=False):
        # type: (str | Path, bool) -> None
        super(BasePreferencesFile, self).__init__(file_path, read_only)
        self.preferences = self._preference_class(self)
        return

    @abstractproperty
    def _preference_class(self):
        # type: () -> Type[BasePreferences]
        pass

    def __getitem__(self, item):
        # type: (str | Type[BaseKey]) -> BaseKey
        """

        Args:
            item: must be a supported preference key name

        Returns:
            PreferenceKey instance of the correspond key
        """
        if isinstance(item, BaseKey):
            item = item.name
        assert (
            item in self.preferences.keys()
        ), "Unsuported key name: got <{}> expected one of <{}>" "".format(
            item, self.preferences.keys()
        )
        return super(BasePreferencesFile, self).__getitem__(item)

    def __setitem__(self, key, value):
        # type: (str | Type[BaseKey], Any) -> None
        if issubclass(key, BaseKey):
            key = key.name
        assert (
            key in self.preferences.keys()
        ), "Unsuported key name: got <{}> expected one of <{}>" "".format(
            key, self.preferences.keys()
        )
        super(BasePreferencesFile, self).__setitem__(key, value)
        return

    def createDefault(self):
        """
        Create the pref file with default values IF it doesn't exist yet.
        """
        if os.path.exists(self.path) or self.read_only:
            return

        # create empty file
        with open(self.path, "w+") as file:
            json.dump({}, file)

        # Now set all defaults values
        self.upgrade(log=False)
        logger.info(
            "[{}][createDefault] Finished. New pref created at {}"
            "".format(self.__class__.__name__, self.path)
        )
        return

    def upgrade(self, log=True):
        """
        Add missing keys if any.
        """

        if self.read_only:
            return

        disk_content = self._read()

        for (
            key_name,
            pref_key,
        ) in self.preferences.items():  # type: str, BaseKey

            # key exists on disk, all good, skip to next one
            if not disk_content.get(key_name, "$$%%") == "$$%%":
                continue

            disk_content[key_name] = pref_key.default
            if log:
                logger.info(
                    "[{}][upgrade] added missing key {}"
                    "".format(self.__class__.__name__, key_name)
                )

        self._write(disk_content)
        return

    def validate(self):
        """
        Raise an error if the file/instance have any issue.

        Raises:
            FileNotFoundError:
            Exception:
        """
        if not os.path.exists(self.path):
            raise FileNotFoundError(
                "The pref file doesn't exists on disk. Expected {}".format(self.path)
            )

        prefs_content = self._read()
        expected = sorted(self.preferences.keys())
        current = sorted(list(prefs_content.keys()))
        assert current == expected, (
            "Preferences are missing a key or have an unsupported key.\n"
            "  Expected {}\n"
            "   But got {}."
            "".format(expected, current)
        )

        # we are sure all the keys are supported
        for pref_key in self.preferences.values():  # type: BaseKey

            pref_key.validateType()
            pref_key.validateValue()

        return
