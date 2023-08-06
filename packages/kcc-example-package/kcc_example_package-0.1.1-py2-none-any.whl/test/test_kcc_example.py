import unittest

from kcc_example import example_function


class TestKCC(unittest.TestCase):

    def test_kcc_output(self):
        self.assertEqual(example_function(), "Hello World!")


if __name__ == "__main__":
    unittest.main()