import logging
import unittest

from pythonningcore import stringing

logger = logging.getLogger(__name__)


class TeststringToXmlString(unittest.TestCase):
    def _log(self, *args):
        msg = "[{}] ".format(self.id().split(".", 1)[-1])
        args = map(str, args)
        msg += " ".join(args)
        print(msg)
        return

    def test_a(self):

        source = 'Hello <there> ! Test & bits there. Double "&&"'
        comparison = "&apos;Hello &lt;there&gt; ! Test &amp; bits there. Double &quot;&amp;&amp;&quot;&apos;"
        result = stringing.stringToXmlString(source=source)

        self._log("\nsource={}\nresult={}".format(source, result))
        self.assertEqual(comparison, result)


class TestgenerateAbreviationFromName(unittest.TestCase):
    def test_a(self):

        testDict = {
            "make_soup": "msp",
            "video_encoding_test": "vett",
            "makeSoup": "msp",
            "videoEncondingTest": "vett",
            "makesoup": "mksp",
            "make soup": "mk sp",
            "Make soup": "msp",
        }

        for source, comparison in testDict.items():

            with self.subTest("source<{}> == <{}>".format(source, comparison)):

                result = stringing.generateAbreviationFromName(name=source)
                self.assertEqual(comparison, result)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(levelname)-7s] %(asctime)s [%(name)s]%(message)s",
    )
    unittest.main()
