import unittest
from datetime import datetime, timedelta
from component.parts import *


class PartsSimpleTestCase(unittest.TestCase):
    def setUp(self):
        self.strings = 'flower'
        self.floats = 2.50
        self.ints = 5
        self.dicts = {'name': 'flower'}
        self.lists = ['flower', 2.5, 5]
        self.token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MiwidXNlcm5hbWUiOiJnYW5uaWN1cyIsImV4cCI6MTU1MDMyMzY3MX0.LeVaHFMM7Z3GPRtzvzQ3tUr2HTuiDnLs4AHC76voxBc'

    def test_str_to_hash(self):
        # Testing function with the right parameters
        val = str_to_hash(self.strings)
        self.assertIsNotNone(val)

        # Testing function with the incorrect parameters
        with self.assertRaises(ValueError):
            str_to_hash(self.ints)
        with self.assertRaises(ValueError):
            str_to_hash(self.lists)

    def test_random_characters(self):
        # Testing function with the right parameters
        val = random_characters(90, 100, self.ints)
        self.assertEqual(self.ints, len(val))

        # Testing function with the incorrect parameters
        with self.assertRaises(TypeError):
            random_characters(97, 100, self.strings)
        with self.assertRaises(TypeError):
            random_characters(self.strings, 122, 6)
        with self.assertRaises(ValueError):
            random_characters(97, 100, 6)

    @unittest.skip('Please prepare new token before testing')
    def test_get_username(self):
        # Testing function with the right parameters
        val = get_username(self.token)
        self.assertIsNotNone(val)

        # Testing function with the incorrect parameters
        val1 = get_username(self.strings)
        self.assertIsNone(val1)

    def test_timedelta_format(self):
        # Testing function with the right parameters
        val = timedelta_format(timedelta(seconds=self.ints))
        self.assertIsInstance(val, str)

        # Testing function with the incorrect parameters
        with self.assertRaises(TypeError):
            timedelta_format(self.ints)

    def test_prep(self):
        # Testing function with the incorrect parameters
        with self.assertRaises(TypeError):
            prep(self.ints, self.strings)

        with self.assertRaises(AttributeError):
            prep(self.dicts, DEFAULT_OFFSET)


if __name__ == '__main__':
    unittest.main()
