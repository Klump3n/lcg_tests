#!/usr/bin/env python3
"""
Unittests for the parameter and number generation.

"""
import unittest


try:
    import modules.spectral_test as st
    import modules.spectral_test_noclass as stn
except ImportError:
    import sys
    sys.path.append("../..")
    import modules.spectral_test as st
    import modules.spectral_test_noclass as stn

from util.logging.logger import CoreLog as cl


class Test_GenParametersAndNumbers(unittest.TestCase):

    def setUp(self):
        cl("debug")

    def tearDown(self):
        pass

    def xtest_gen_number_list_range(self):
        """generate a list of numbers, range of numbers

        """
        print()
        params = dict()

        # params["x0"] = 0
        # params["a"] = 7**5
        # params["c"] = 2**8 - 15
        # params["m"] = 2**16 - 1

        # good basic test
        params["x0"] = 1
        params["a"] = 1103515245
        params["c"] = 453816694
        params["m"] = 2**32 - 1

        spectral = st.SpectralTest(params, T=10)

        res = spectral.get_results()

    def test_knuth_parameters(self):
        """test the spectral test with the parameters and results given by Knuth

        """
        params = dict()

        # lcg parameters given by knuth
        params["x0"] = 0
        params["a"] = 3141592621
        params["c"] = 1
        params["m"] = 10**10

        spectral = st.SpectralTest(params, T=3)

        res = spectral.get_results()

        # results given by knuth
        self.assertAlmostEqual(res[2], 67654.37748, 5)
        self.assertAlmostEqual(res[3],  1017.21089, 5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
