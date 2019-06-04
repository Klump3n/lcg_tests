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

        # params["x0"] = 0
        # params["a"] = 7**5
        # params["c"] = 2**8 - 15
        # params["m"] = 2**16 - 1

        # # good basic test
        # params["x0"] = 1
        # params["a"] = 1103515245
        # params["c"] = 453816694
        # params["m"] = 2**32 - 1

        # good basic test
        params["x0"] = 0
        params["a"] = 3141592621
        params["c"] = 1
        params["m"] = 10**10

        spectral = st.SpectralTest(params)
        # spectral.visualize()

if __name__ == "__main__":
    unittest.main(verbosity=2)
