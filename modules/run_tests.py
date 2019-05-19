#!/usr/bin/env python3
"""
Run the tests for the LCG.

"""
from util.logging.logger import CoreLog as cl
import modules.gen_parameters_and_numbers as gpn

import modules.statistical_monobit as monobit
import modules.statistical_poker as poker
import modules.statistical_runs as runs
import modules.statistical_autocorrelation as ac

import numpy as np

def run_tests(numbers_from_file=None):
    """
    Run the tests for the LCG.

    """
    if numbers_from_file:
        binary_sequence = numbers_from_file

    else:
        parameters = gpn.gen_params()

        nums = gpn.gen_nums(parameters)

        bin_nums = gpn.gen_binary_nums(nums, modulus=parameters["m"])
        binary_sequence = gpn.gen_binary_sequence(bin_nums)

    general_results = list()

    cl.verbose("Performing MONOBIT test")
    general_results.append(monobit.monobit_passed(binary_sequence))

    cl.verbose("Performing POKER test")
    general_results.append(poker.poker_passed(binary_sequence))

    cl.verbose("Performing RUNS test")
    general_results.append(runs.runs_passed(binary_sequence))

    cl.verbose("Performing LONG RUNS test")
    general_results.append(runs.long_runs_passed(binary_sequence))

    cl.verbose("Performing AUTOCORRELATION test")
    general_results.append(ac.autocorrelation_passed(binary_sequence))

    if numbers_from_file:
        source = "random data from file"
    else:
        source = "parameters {}".format(parameters)

    if np.all(general_results):
        cl.info("\u001b[32;1mGeneral statistical tests passed for "
                "{}\u001b[0m".format(source))
    else:
        cl.info("\u001b[31;1mGeneral statistical tests failed for "
                "{}\u001b[0m".format(source))
