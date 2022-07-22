import logging
import os
from pathlib import Path  # TODO convert to py2
import unittest

from pythonningcore.datastructuring import preferencing


logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent / "data"
PREF1 = DATA_DIR / "pref-test-1.json"
PREF_TARGET_A = DATA_DIR / "target-A.json"


class key_alpha(preferencing.BaseKey):
    name = "key_alpha"
    types = (bool,)
    default = True

    def validateValue(self):
        pass


class key_beta(preferencing.BaseKey):
    name = "key_beta"
    types = (str, type(None))
    default = ""

    def validateValue(self):
        v = self.value
        if not v:
            return
        assert os.path.exists(v), "Config doesn't exists on disk: {}".format(v)
        assert v.endswith(".py"), "Path is not a .ocio file: {}".format(v)


class Preferences(preferencing.BasePreferences):
    def __init__(self, preference_file):
        self.key_alpha = key_alpha(preference_file)
        self.key_beta = key_beta(preference_file)


class PreferencesFile(preferencing.BasePreferencesFile):
    _preference_class = Preferences


class PreferencesFileTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        PREF_TARGET_A.unlink(missing_ok=True)

    def _log(self, *args):
        msg = "[{}] ".format(self.id().split(".", 1)[-1])
        args = map(str, args)
        msg += " ".join(args)
        logger.info(msg)
        return

    def test_init(self):
        pref = PreferencesFile(PREF1)
        self.assertEqual(pref.path, str(PREF1))
        self.assertFalse(pref.read_only)

    def test_init_not_exists(self):
        pref = PreferencesFile(PREF_TARGET_A)
        self.assertEqual(pref.path, str(PREF_TARGET_A))
        self.assertFalse(pref.read_only)
        self.assertFalse(PREF_TARGET_A.exists())
        pref.createDefault()
        self.assertTrue(PREF_TARGET_A.exists())
        pref.validate()


class BaseKeyCategoriesTest(unittest.TestCase):
    class KeyCategoriesA(preferencing.BaseKeyCategories):
        general = "General"

    class KeyCategoriesB(preferencing.BaseKeyCategories):
        account = "Account"
        version_control = "Version Control"

    def setUp(self):
        pass

    def tearDown(self):
        PREF_TARGET_A.unlink(missing_ok=True)

    def _log(self, *args):
        msg = "[{}] ".format(self.id().split(".", 1)[-1])
        args = map(str, args)
        msg += " ".join(args)
        logger.info(msg)
        return

    def test_init(self):

        cat_1 = self.KeyCategoriesA.general
        cat_2 = self.KeyCategoriesA.general
        self.assertEqual(cat_1, cat_2)

        self.assertIn(cat_1, self.KeyCategoriesA.__all__())
        self.assertNotIn(cat_1, self.KeyCategoriesB.__all__())


if __name__ == "__main__":
    unittest.main()
