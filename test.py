import unittest
from pytsk3_test import parse_mft


class CustomTests(unittest.TestCase):

    def test_skip_padding(self):
        self.assertEqual(1014, parse_mft._skip_padding(233, 1024))


if __name__ == '__main__':
    unittest.main()