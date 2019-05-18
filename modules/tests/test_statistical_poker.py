#!/usr/bin/env python3
"""
Unittests for the poker tests.

"""
import unittest

try:
    import modules.statistical_poker as poker
except ImportError:
    import sys
    sys.path.append("../..")
    import modules.statistical_poker as poker

from util.logging.logger import CoreLog as cl

import modules.gen_parameters_and_numbers as gpn

class Test_StatisticalPoker(unittest.TestCase):

    def setUp(self):
        cl("debug")

    def tearDown(self):
        pass

    def test_poker(self):
        """test poker test

        """
        parameters = gpn.gen_params()
        nums = gpn.gen_nums(parameters)
        bin_nums = gpn.gen_binary_nums(nums, modulus=parameters["m"])
        binary_sequence = gpn.gen_binary_sequence(bin_nums)

        poker.poker_passed(binary_sequence)

if __name__ == "__main__":
    unittest.main(verbosity=2)
