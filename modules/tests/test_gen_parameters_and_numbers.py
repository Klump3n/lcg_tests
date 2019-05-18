#!/usr/bin/env python3
"""
Unittests for the parameter and number generation.

"""
import unittest


try:
    import modules.gen_parameters_and_numbers as gpn
except ImportError:
    import sys
    sys.path.append("../..")
    import modules.gen_parameters_and_numbers as gpn

from util.logging.logger import CoreLog as cl


class Test_GenParametersAndNumbers(unittest.TestCase):

    def setUp(self):
        cl("debug")

    def tearDown(self):
        pass

    def test_gen_number_list(self):
        """generate a list of numbers

        """
        params = gpn.gen_params()
        nums = gpn.gen_nums(params, 20000)
        self.assertEqual(20000, len(nums))  # make sure we have 20000 numbers

    def test_gen_number_list_range(self):
        """generate a list of numbers, range of numbers

        """
        params = dict()
        params["x0"] = 0
        params["a"] = 1
        params["c"] = 1
        params["m"] = 16

        nums = gpn.gen_nums(params, 16)
        print(nums)
        # self.assertEqual(20000, len(nums))  # make sure we have 20000 numbers

    def test_gen_binary_list(self):
        """generate a list of binary numbers from the numbers

        """
        nums = [1, 2, 15, 31]
        binary_nums = gpn.gen_binary_nums(nums, modulus=32)
        self.assertEqual(binary_nums, ["00001", "00010", "01111", "11111"])

    def test_gen_binary_sequence(self):
        """generate a sequence of binary numbers

        """
        nums = [1, 15]
        binary_nums = gpn.gen_binary_nums(nums, modulus=16)
        binary_sequence = gpn.gen_binary_sequence(binary_nums)
        self.assertEqual(binary_sequence, "00011111")

    def test_gen_binary_sequence_list(self):
        """generate a sequence of binary numbers, verify length

        """
        params = gpn.gen_params()
        nums = gpn.gen_nums(params)
        binary_nums = gpn.gen_binary_nums(nums)
        binary_sequence = gpn.gen_binary_sequence(binary_nums)
        self.assertEqual(len(binary_sequence), 20000)

    def test_gen_expected_statistic(self):
        """generate a expected statistic

        """
        modulus = 4
        res = gpn.gen_expected_statistic(modulus)
        self.assertEqual(res, 1.0)

        modulus = 5             # this adds a bunch of zeros
        res = gpn.gen_expected_statistic(modulus)
        self.assertEqual(res, 2.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
