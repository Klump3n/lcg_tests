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

def run_tests(args, numbers_from_file=None):
    """
    Run the tests for the LCG.

    """
    if numbers_from_file:
        binary_sequence = numbers_from_file
        sequence_test(binary_sequence)

    else:
        x0 = args.x

        if args.a is not None:
            amin = eval(args.a)
            amax = eval(args.a)
        else:
            amin = min(eval(args.a_minmax[0]), eval(args.a_minmax[1]))
            amax = max(eval(args.a_minmax[0]), eval(args.a_minmax[1]))

        if args.c is not None:
            cmin = eval(args.c)
            cmax = eval(args.c)
        else:
            cmin = min(eval(args.c_minmax[0]), eval(args.c_minmax[1]))
            cmax = max(eval(args.c_minmax[0]), eval(args.c_minmax[1]))

        if args.m is not None:
            mmin = eval(args.m)
            mmax = eval(args.m)
        else:
            mmin = min(eval(args.m_minmax[0]), eval(args.m_minmax[1]))
            mmax = max(eval(args.m_minmax[0]), eval(args.m_minmax[1]))

        param_list = gpn.parameter_sweep(x0, amin, amax, cmin, cmax, mmin, mmax)
        for parameters in param_list:
            nums = gpn.gen_nums(parameters)

            bin_nums = gpn.gen_binary_nums(nums, modulus=parameters["m"])
            binary_sequence = gpn.gen_binary_sequence(bin_nums)

            sequence_test(binary_sequence, parameters)


def sequence_test(binary_sequence, parameters=None):
    """
    Run a test on a binary sequence.

    """
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

    if parameters:
        source = "parameters {}".format(parameters)
    else:
        source = "random data from file"

    if np.all(general_results):
        cl.info("\u001b[32;1mGeneral statistical tests passed for "
                "{}\u001b[0m".format(source))
    else:
        cl.info("\u001b[31;1mGeneral statistical tests failed for "
                "{}\u001b[0m".format(source))
