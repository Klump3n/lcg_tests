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






    # filename = "thisfile.h5"

    # if pathlib.Path(filename).exists():
    #     pathlib.Path(filename).unlink()
    #     pathlib.Path(filename).touch()

    # asize = 20
    # csize = 20
    # msize = 20

    # with h5py.File(filename, "r+") as h5file:
    #     dt = h5py.special_dtype(vlen=str)     # PY3
    #     h5file.create_dataset("success_rates_json", (asize, csize, msize), maxshape=(None, None, None), dtype=dt)  # resizeable

    # # some profiling
    # # open once and write all
    # start = time.time()

    # with h5py.File(filename, "r+") as h5file:
    #     dset_json = h5file["success_rates_json"]
    #     for a in np.arange(0, 2*asize, 3):
    #     # for a in range(asize):
    #         for c in np.arange(0, 2*csize, 3):
    #         # for c in range(csize):
    #             for m in np.arange(0, 2*msize, 3):
    #             # for m in range(msize):

    #                 try:
    #                     write = dict()
    #                     write["res1"] = random.random()
    #                     write["res2"] = random.random()
    #                     write["res3"] = random.random()
    #                     write["res4"] = random.random()
    #                     write["res5"] = random.random()
    #                     json_write = json.dumps(write)
    #                     dset_json[a, c, m] = json_write

    #                 except ValueError:
    #                     nasize, ncsize, nmsize = dset_json.shape
    #                     if a >= nasize:
    #                         nasize = a + 1
    #                     if c >= ncsize:
    #                         ncsize = c + 1
    #                     if m >= nmsize:
    #                         nmsize = m + 1
    #                     dset_json.shape = (nasize, ncsize, nmsize)
    #                     print("Reshape to {}".format(dset_json.shape))
    #                     dset_json[a, c, m] = json_write

    # print("Opening once and writing entries took {:.2f} seconds".format(time.time() - start))









        # open file to save results in
        res_file = pathlib.Path(__file__).parent.parent / "results_file.h5"

        if not res_file.exists():

            asize, csize, msize = (1024, 1024, 1024)

            pathlib.Path(res_file).touch()

            with h5py.File(res_file, "r+") as h5file:
                dt = h5py.special_dtype(vlen=str)  # string
                h5file.create_dataset("results_a_c_m", (asize, csize, msize), maxshape=(None, None, None), dtype=dt)  # resizeable


        with h5py.File(res_file, "r+") as h5file:

            results = h5file["results_a_c_m"]

            for parameters in param_list:
                nums = gpn.gen_nums(parameters)

                bin_nums = gpn.gen_binary_nums(nums, modulus=parameters["m"])
                binary_sequence = gpn.gen_binary_sequence(bin_nums)

                sequence_res = sequence_test(binary_sequence, parameters)

                res_dict = dict()
                res_dict["params"] = parameters
                res_dict["results"] = sequence_res
                result = json.dumps(res_dict)

                a = parameters["a"]
                c = parameters["c"]
                m = parameters["m"]

                # write to file
                try:
                    results[a, c, m] = result

                # increase size of file
                except ValueError:
                    nasize, ncsize, nmsize = results.shape
                    if a >= nasize:
                        nasize = a + 1
                    if c >= ncsize:
                        ncsize = c + 1
                    if m >= nmsize:
                        nmsize = m + 1

                    results.shape = (nasize, ncsize, nmsize)
                    results[a, c, m] = result


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

    count = 0
    for res in general_results:
        if res is True:
            count += 1
    if parameters:
        source = "parameters {}".format(parameters)
    else:
        source = "random data from file"

    if np.all(general_results):
        cl.info("\u001b[32;1m({}/{} passed) General statistical tests passed "
                "for {}\u001b[0m".format(count, len(general_results), source))
    else:
        cl.info("\u001b[31;1m({}/{} passed) General statistical tests failed "
                "for {}\u001b[0m".format(count, len(general_results), source))

    return general_results
