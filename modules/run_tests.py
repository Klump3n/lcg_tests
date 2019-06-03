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
import pickle
import pathlib

def run_tests(args, numbers_from_file=None):
    """
    Run the tests for the LCG.

    """
    if numbers_from_file:
        binary_sequence = numbers_from_file
        sequence_test(args, binary_sequence)

    else:
        x0 = args.x

        if len(args.a) == 1:
            amin = eval(args.a[0])
            amax = eval(args.a[0])
        elif len(args.a) == 2:
            amin = min(eval(args.a[0]), eval(args.a[1]))
            amax = max(eval(args.a[0]), eval(args.a[1]))
        else:
            cl.error("Can't parse a")

        if len(args.c) == 1:
            cmin = eval(args.c[0])
            cmax = eval(args.c[0])
        elif len(args.c) == 2:
            cmin = min(eval(args.c[0]), eval(args.c[1]))
            cmax = max(eval(args.c[0]), eval(args.c[1]))
        else:
            cl.error("Can't parse c")

        if len(args.m) == 1:
            mmin = eval(args.m[0])
            mmax = eval(args.m[0])
        elif len(args.m) == 2:
            mmin = min(eval(args.m[0]), eval(args.m[1]))
            mmax = max(eval(args.m[0]), eval(args.m[1]))
        else:
            cl.error("Can't parse m")

        if args.force:
            cl.info("Forcing recalculation for every parameter")

        # open file to save results in
        results_dir = pathlib.Path(__file__).parent.parent / "results"

        if not results_dir.is_dir():
            results_dir.mkdir()

        filename = "results_x0_{}_a_{}_{}_c_{}_{}_m_{}_{}.pickle".format(
            x0, amin, amax, cmin, cmax, mmin, mmax)
        res_file = results_dir / filename

        if not res_file.exists():
            res_file.touch()

        cl.verbose("Using results file {}".format(res_file))

        param_list = gpn.parameter_sweep(x0, amin, amax, cmin, cmax, mmin, mmax)

        calculation_counter = 0
        max_calculations = len(param_list)

        # calculations
        for parameters in param_list:

            x0 = parameters["x0"]
            a = parameters["a"]
            c = parameters["c"]
            m = parameters["m"]

            with open(res_file, "rb") as output_file:
                cl.debug("Reading results from output file")

                try:
                    res_dict = pickle.load(output_file)
                    cl.debug("Loading existing dictionary")
                except EOFError:
                    res_dict = dict()
                    cl.debug("Creating new dictionary")
                else:
                    try:
                        if (
                                isinstance(res_dict[x0][a][c][m], dict)
                                and
                                not args.force
                        ):
                            cl.verbose("Datapoint {} exists, skipping".format(
                                parameters))
                            continue
                        if (
                                isinstance(res_dict[x0][a][c][m], dict)
                                and
                                args.force
                        ):
                            cl.verbose("Datapoint {} exists, forcing "
                                       "recalculation".format(parameters))
                    except KeyError:
                        pass

            # create the dictionary step by step
            try:
                res = res_dict[x0]
            except KeyError:
                res_dict[x0] = dict()

            try:
                res = res_dict[x0][a]
            except KeyError:
                res_dict[x0][a] = dict()

            try:
                res = res_dict[x0][a][c]
            except KeyError:
                res_dict[x0][a][c] = dict()

            try:
                res = res_dict[x0][a][c][m]
            except KeyError:
                res_dict[x0][a][c][m] = dict()


            # perform the actual calculation
            nums = gpn.gen_nums(parameters)

            bin_nums = gpn.gen_binary_nums(nums, modulus=parameters["m"])
            binary_sequence = gpn.gen_binary_sequence(bin_nums)

            calculation_counter += 1

            sequence_res = sequence_test(
                args, binary_sequence,
                calculation_counter, max_calculations,
                parameters
            )

            res_dict[x0][a][c][m] = sequence_res
            with open(res_file, "wb") as output_file:
                cl.debug("Writing results to output file")
                pickle.dump(res_dict, output_file)


def sequence_test(args, binary_sequence, calc_count=1, max_count=1, parameters=None):
    """
    Run a test on a binary sequence.

    """
    num_proc = args.j

    general_results = list()
    general_results_dict = dict()

    cl.verbose("Performing MONOBIT test")
    monobit_result = monobit.monobit_passed(binary_sequence)
    general_results.append(monobit_result)
    general_results_dict["monobit"] = monobit_result

    cl.verbose("Performing POKER test")
    poker_result = poker.poker_passed(binary_sequence)
    general_results.append(poker_result)
    general_results_dict["poker"] = poker_result

    cl.verbose("Performing RUNS test")
    runs_result = runs.runs_passed(binary_sequence, parallel=num_proc)
    general_results.append(runs_result)
    general_results_dict["runs"] = runs_result

    cl.verbose("Performing LONG RUNS test")
    long_runs_result = runs.long_runs_passed(binary_sequence, parallel=num_proc)
    general_results.append(long_runs_result)
    general_results_dict["long_runs"] = long_runs_result

    cl.verbose("Performing AUTOCORRELATION test")
    autocorrelation_result = ac.autocorrelation_passed(binary_sequence)
    general_results.append(autocorrelation_result)
    general_results_dict["autocorrelation"] = autocorrelation_result

    count = 0
    for res in general_results:
        if res is True:
            count += 1
    if parameters:
        source = "parameters {}".format(parameters)
    else:
        source = "random data from file"

    if np.all(general_results):
        cl.info("[{} of {}]: \u001b[32;1m({}/{} tests passed) General "
                "statistical tests passed for {}\u001b[0m".format(
                    calc_count, max_count, count, len(general_results), source))
    else:
        cl.info("[{} of {}]: \u001b[31;1m({}/{} tests passed) General "
                "statistical tests failed for {}\u001b[0m".format(
                    calc_count, max_count, count, len(general_results), source))

    return general_results_dict
