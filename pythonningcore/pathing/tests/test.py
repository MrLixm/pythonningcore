"""

"""
import filecmp
import logging
import os.path
import unittest
import uuid

import pythonningcore
import pythonningcore.pathing
import pythonningcore.loggering

logger = logging.getLogger("{}.tests.test".format(pythonningcore.pathing.c.abr))
pythonningcore.loggering.setupLoggingFor(
    loggers=[pythonningcore.c.abr], level=logging.DEBUG
)

DIR_DATA = os.path.abspath("./data")
SRC_DIR = os.path.join(DIR_DATA, "src")
SRC_ALPHA = os.path.join(SRC_DIR, "alpha")
SRC_BETA = os.path.join(SRC_DIR, "beta")


def initTestDir(src, target):
    # type: (str, str) -> None
    if os.path.exists(target):
        pythonningcore.pathing.clearDir(target)
    os.makedirs(target)
    pythonningcore.pathing.copyDir(src, target)
    logger.info("[initTestDir] Finished. Created {}".format(target))
    return


class B_clearDirTest(unittest.TestCase):
    def setUp(self):
        self.test_dir = os.path.join(DIR_DATA, "test{}".format(uuid.uuid4().hex))

    def tearDown(self):
        self.test_dir = None

    def test_basic(self):

        initTestDir(SRC_ALPHA, target=self.test_dir)

        self.assertTrue(os.path.exists(self.test_dir))
        pythonningcore.pathing.clearDir(self.test_dir)
        self.assertFalse(os.path.exists(self.test_dir))

    def test_not_exists(self):

        self.assertFalse(os.path.exists(self.test_dir))
        pythonningcore.pathing.clearDir(self.test_dir)
        self.assertFalse(os.path.exists(self.test_dir))

    def test_readonly(self):
        initTestDir(SRC_BETA, target=self.test_dir)

        self.assertTrue(os.path.exists(self.test_dir))
        pythonningcore.pathing.clearDir(self.test_dir)
        self.assertFalse(os.path.exists(self.test_dir))

    def test_readonly_fail(self):
        initTestDir(SRC_BETA, target=self.test_dir)

        self.assertTrue(os.path.exists(self.test_dir))
        with self.assertRaises(PermissionError) as excp:
            pythonningcore.pathing.clearDir(self.test_dir, force=False)
        self.assertTrue(os.path.exists(self.test_dir))

        pythonningcore.pathing.clearDir(self.test_dir, force=True)


class A_copyDir(unittest.TestCase):
    def setUp(self):
        self.test_dir = os.path.join(DIR_DATA, "test{}".format(uuid.uuid4().hex))

    def tearDown(self):
        pythonningcore.pathing.clearDir(self.test_dir, force=True)
        self.test_dir = None

    def test_basic(self):

        pythonningcore.pathing.copyDir(SRC_ALPHA, self.test_dir)
        result = filecmp.dircmp(SRC_ALPHA, self.test_dir)
        self.assertFalse(result.left_only)
        self.assertFalse(result.right_only)

    def test_mirror(self):

        pythonningcore.pathing.copyDir(SRC_ALPHA, self.test_dir)
        pythonningcore.pathing.copyDir(SRC_BETA, self.test_dir)
        result = filecmp.dircmp(SRC_ALPHA, self.test_dir)
        self.assertFalse(result.left_only)
        self.assertTrue(result.right_only)

        pythonningcore.pathing.copyDir(SRC_BETA, self.test_dir, mirror=True)
        result = filecmp.dircmp(SRC_BETA, self.test_dir)
        self.assertFalse(result.left_only)
        self.assertFalse(result.right_only)


if __name__ == "__main__":
    unittest.main()
