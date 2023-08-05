import unittest
import pandas as pd
from bwgds.bwlibrary.handy_mix import HandyMix

class TestClasses(unittest.TestCase):
    """ Testing the implemented classes """

    def test_handy_functions(self):
        """ Test the HandyMix methods """
        list_sample = [[1], [2, 3]]
        test_result = HandyMix().flatten_nested_list(list_sample)
        self.assertEqual(test_result, [1, 2, 3])

if __name__ == '__main__':
    TestClasses().test_handy_functions()
