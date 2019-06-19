#!/usr/bin/env python3
"""
This is part of a seminar I'm taking about random numbers.

I deal with the randomness of the linear congruential generator and how the
choices of parameters influences the quality of the random numbers.

Plot the results.

"""
import sys
import argparse
import pickle
import re

from util.logging.logger import CoreLog as cl
from util.opt.greet import ngreeting

def parse_arguments():
    """
    Parse the command line arguments.

    """
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-l", "--log", help="set logging level",
                        choices=["quiet", "debug", "verbose", "info",
                                 "warning", "error", "critical"],
                        default="info")

    parser.add_argument("-i", "--input", help="perform tests on input file",
                        required=True)

    excl_group = parser.add_mutually_exclusive_group()
    excl_group.add_argument("-a", type=str, help="a in (a*x + c) mod m")
    excl_group.add_argument("-c", type=str, help="c in (a*x + c) mod m")
    excl_group.add_argument("-m", type=str, help="m in (a*x + c) mod m")

    parser.add_argument("-o", "--output", help="name of output files")

    args = parser.parse_args()
    return args

def setup_loggers(logging_level):
    """
    Setup the logging level.

    """
    cl(logging_level)
    cl.verbose("starting logging")
    cl.verbose("logging level is set to {}".format(logging_level))
    if logging_level == "verbose" or logging_level == "debug":
        print()                 # newline

def greet():
    """
    Print a greeting.

    """
    print(ngreeting())

def parse_input(input_file):
    """
    Unpickle the input file.

    """
    # see what we have to expect from this input file
    try:
        res = input_file.split("_")
        res.remove("results/results")
        res.remove("x0")
        res.remove("a")
        res.remove("c")
        res.remove("m")
    except ValueError:
        cl.error("Could not determine parameter ranges from input file name")
        sys.exit()

    x0, amin, amax, cmin, cmax, mmin, mmax = res

    x0 = int(x0)
    amin = int(amin)
    amax = int(amax)
    cmin = int(cmin)
    cmax = int(cmax)
    mmin = int(mmin)
    mmax = int(mmax.split(".")[0])

    expected = dict()
    expected["x0"] = x0
    expected["amin"] = amin
    expected["amax"] = amax
    expected["cmin"] = cmin
    expected["cmax"] = cmax
    expected["mmin"] = mmin
    expected["mmax"] = mmax

    cl.debug("Parsed parameter ranges from input file name")

    return_dict = dict()

    with open(input_file, "rb") as ifile:
        input_data = pickle.load(ifile)

    cl.debug("Loaded dictionary from file")

    for a in range(amin, amax+1):
        for c in range(cmin, cmax+1):
            for m in range(mmin, mmax+1):
                try:
                    assert(isinstance(input_data[x0][a][c][m], dict))
                except KeyError as e:
                    cl.error("Could not find parameter x0 {} a {} c {} m {} in "
                             "input file".format(x0, a, c, m))
                    cl.error("Input file appears to be corrupted or incomplete")
                    sys.exit()

    cl.debug("Input file appears to be in ship shape, proceeding")

    return_dict["ranges"] = expected
    return_dict["input_data"] = input_data
    return return_dict

def main():
    """
    Main entry point.

    """
    args = parse_arguments()
    greet()

    logging_level = args.log
    setup_loggers(logging_level)

    cl.info("Using {}".format(args.input))

    input_data = parse_input(args.input)

    x0 = input_data["ranges"]["x0"]
    amin = input_data["ranges"]["amin"]
    amax = input_data["ranges"]["amax"]
    cmin = input_data["ranges"]["cmin"]
    cmax = input_data["ranges"]["cmax"]
    mmin = input_data["ranges"]["mmin"]
    mmax = input_data["ranges"]["mmax"]

    if not args.a and not args.c and not args.m:
        cl.info("x0 is in [{}, {}]".format(x0, x0))
        cl.info(" a is in [{}, {}]".format(amin, amax))
        cl.info(" c is in [{}, {}]".format(cmin, cmax))
        cl.info(" m is in [{}, {}]".format(mmin, mmax))
        cl.info("Pick ONE value from the ranges to generate a plot")
        sys.exit()

if __name__ == "__main__":
    main()
