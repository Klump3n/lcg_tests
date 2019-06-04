#!/usr/bin/env python3
"""
Unittests for the parameter and number generation.

"""
import unittest


try:
    import modules.spectral_test as st
except ImportError:
    import sys
    sys.path.append("../..")
    import modules.spectral_test as st

from util.logging.logger import CoreLog as cl


class Test_GenParametersAndNumbers(unittest.TestCase):

    def setUp(self):
        cl("debug")

    def tearDown(self):
        pass

    def test_gen_number_list_range(self):
        """generate a list of numbers, range of numbers

        """
        print()
        params = dict()
        params["x0"] = 0
        params["a"] = 7**5
        params["c"] = 2**8 - 15
        params["m"] = 2**8 - 1

        spectral = st.SpectralTest(params)
        spectral.visualize()

if __name__ == "__main__":
    unittest.main(verbosity=2)
