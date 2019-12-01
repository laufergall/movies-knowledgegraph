
import unittest

from spiders.utils import is_positiveinteger, strip_text


class TestUtils(unittest.TestCase):

    def test_is_positiveinteger(self):

        self.assertTrue(is_positiveinteger(1))
        self.assertTrue(is_positiveinteger(23))
        self.assertTrue(is_positiveinteger(1.1))

        self.assertFalse(is_positiveinteger(0))
        self.assertFalse(is_positiveinteger(-0))
        self.assertFalse(is_positiveinteger(-1))
        self.assertFalse(is_positiveinteger(-23.1))

    def test_strip_text(self):

        @strip_text
        def my_function():
            return ['\n                    6,50 EUR ',
                    '\nAndere Preise gelten bei Kurzfilmen                ']

        actual = my_function()
        expected = ['6,50 EUR', 'Andere Preise gelten bei Kurzfilmen']

        self.assertListEqual(actual, expected)
