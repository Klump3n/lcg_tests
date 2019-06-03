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
import h5py
import pathlib
import json

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

        param_list = gpn.parameter_sweep(x0, amin, amax, cmin, cmax, mmin, mmax)

        # open file to save results in
        res_file = pathlib.Path(__file__).parent.parent / "results_file.h5"

        if not res_file.exists():
            cl.verbose("Creating results file {}".format(res_file))
            asize, csize, msize = (1024, 1024, 1024)

            pathlib.Path(res_file).touch()

            with h5py.File(res_file, "r+") as h5file:
                dt = h5py.special_dtype(vlen=str)  # string
                # resizeable h5 dataset
                h5file.create_dataset("results_a_c_m", (asize, csize, msize),
                                      maxshape=(None, None, None), dtype=dt)

        with h5py.File(res_file, "r+") as h5file:

            cl.verbose("Using results file {}".format(res_file))

            results = h5file["results_a_c_m"]

            calculation_counter = 0
            max_calculations = len(param_list)

            for parameters in param_list:

                a = parameters["a"]
                c = parameters["c"]
                m = parameters["m"]

                try:
                    old = results[a, c, m]
                    if not old == "":
                        calculation_counter += 1
                        cl.verbose("Datapoint for parameters {} exits, doing "
                                   "nothing".format(parameters))
                        continue
                except json.decoder.JSONDecodeError as e:
                    cl.debug("Exception when trying to parse json for "
                             "parameter {} from file: {}".format(parameters, e))

                # increase size of file if the datapoint can not be accessed
                except ValueError:
                    nasize, ncsize, nmsize = results.shape
                    if a >= nasize:
                        nasize = a + 1
                    if c >= ncsize:
                        ncsize = c + 1
                    if m >= nmsize:
                        nmsize = m + 1

                    results.shape = (nasize, ncsize, nmsize)
                    cl.debug("Increasing storage size of results file "
                             "to {}".format(results.shape))

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

                res_dict = dict()
                res_dict["params"] = parameters
                res_dict["results"] = sequence_res
                result = json.dumps(res_dict)

                # write to file
                results[a, c, m] = result
                cl.verbose("Writing results to output file")



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
