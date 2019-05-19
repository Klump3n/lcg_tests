#!/usr/bin/env python3
"""
This is part of a seminar I'm taking about random numbers.

I deal with the randomness of the linear congruential generator and how the
choices of paramters influences the quality of the random numbers.

"""
import sys
import unittest
import argparse

from util.logging.logger import CoreLog as cl
from util.opt.greet import ngreeting

import modules.parse_file as parse_file
import modules.run_tests as run_tests

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
    parser.add_argument("-f", "--file", help="perform tests on file")
    parser.add_argument("-t", "--test", help="perform unittests",
                        action="store_true")
    args = parser.parse_args()
    return args

def perform_unittests():
    """
    Start unittest for the program.
    """
    tests = unittest.TestLoader().discover('.')
    # unittest.runner.TextTestRunner(verbosity=2, buffer=False).run(tests)
    unittest.runner.TextTestRunner(verbosity=2, buffer=True).run(tests)

    sys.exit("--- Performed unittests, exiting ---")

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

def main():
    """
    Main entry point.

    """
    args = parse_arguments()

    if args.test:
        perform_unittests()
    else:
        greet()

    logging_level = args.log
    setup_loggers(logging_level)

    binary_sequence = None      # instantiate to None

    # if we have a random data file present we can parse that
    if args.file:
        binary_sequence = parse_file.parse_from_file(args.file)
        cl.info("Testing random numbers from file {}".format(args.file))
    else:
        cl.info("Starting LCG testing")

    # run the tests for the LCG (or the random data provided)
    run_tests.run_tests(binary_sequence)

if __name__ == "__main__":
    main()
