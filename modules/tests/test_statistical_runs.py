#!/usr/bin/env python3
"""
Unittests for the runs tests.

"""
import unittest

try:
    import modules.statistical_test_runs as runs
except ImportError:
    import sys
    sys.path.append("../..")
    import modules.statistical_test_runs as runs

from util.logging.logger import CoreLog as cl

import modules.gen_parameters_and_numbers as gpn

class Test_StatisticalRuns(unittest.TestCase):

    def setUp(self):
        cl("debug")

    def tearDown(self):
        pass

    def test_instance(self):
        """test one instance

        """
        bin_seq = "01010101"
        zero_count, one_count = runs.runs_instance(bin_seq, 1)
        self.assertEqual(zero_count, 3)
        self.assertEqual(one_count, 3)

        bin_seq = "0011001100110011"
        zero_count, one_count = runs.runs_instance(bin_seq, 2)
        self.assertEqual(zero_count, 3)
        self.assertEqual(one_count, 3)

        bin_seq = "0100110001110"
        zero_count, one_count = runs.runs_instance(bin_seq, 1)
        self.assertEqual(zero_count, 0)
        self.assertEqual(one_count, 1)
        zero_count, one_count = runs.runs_instance(bin_seq, 2)
        self.assertEqual(zero_count, 1)
        self.assertEqual(one_count, 1)
        zero_count, one_count = runs.runs_instance(bin_seq, 3)
        self.assertEqual(zero_count, 1)
        self.assertEqual(one_count, 1)

    def test_runs_test(self):
        """test the runs test

        """
        parameters = gpn.gen_params()
        nums = gpn.gen_nums(parameters)
        bin_nums = gpn.gen_binary_nums(nums, modulus=parameters["m"])
        binary_sequence = gpn.gen_binary_sequence(bin_nums)

        runs.runs_passed(binary_sequence)

    def test_long_runs_test(self):
        """test the runs test

        """
        parameters = gpn.gen_params()
        nums = gpn.gen_nums(parameters)
        bin_nums = gpn.gen_binary_nums(nums, modulus=parameters["m"])
        binary_sequence = gpn.gen_binary_sequence(bin_nums)

        runs.long_runs_passed(binary_sequence)

if __name__ == "__main__":
    unittest.main(verbosity=2)
