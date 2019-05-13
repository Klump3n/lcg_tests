#!/usr/bin/env python3
"""
Run the tests for the LCG.

"""
from util.logging.logger import CoreLog as cl
import modules.gen_parameters_and_numbers as gpn

import modules.statistical_monobit as monobit
import modules.statistical_poker as poker

import numpy as np

def run_tests():
    """
    Run the tests for the LCG.

    """
    parameters = gpn.gen_params()
    binary_sequence = gpn.gen_nums(parameters)

    general_results = list()

    cl.verbose("Performing MONOBIT test")
    general_results.append(monobit.monobit_passed(binary_sequence))

    cl.verbose("Performing POKER test")
    general_results.append(poker.poker_passed(binary_sequence))

    if np.all(general_results):
        cl.info("\u001b[32;1mGeneral statistical tests passed for "
                "parameters {}\u001b[0m".format(parameters))
    else:
        cl.info("\u001b[31;1mGeneral statistical tests failed for "
                "parameters {}\u001b[0m".format(parameters))
