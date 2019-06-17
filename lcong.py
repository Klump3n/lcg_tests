#!/usr/bin/env python3
"""
This is part of a seminar I'm taking about random numbers.

I deal with the randomness of the linear congruential generator and how the
choices of parameters influences the quality of the random numbers.

Some usable parameter choices are:

./lcong.py -x 1 -a 33 -c 0 -m 251 -l verbose               (works but period too short)
./lcong.py -x 1 -a 1103515245 -c 453816694 -m "2**31 - 0"  (does not work)
./lcong.py -x 1 -a 1103515245 -c 453816694 -m "2**31 - 1"  (does work)
./lcong.py -x 1 -a 1103515245 -c 453816694 -m "2**31 - 2"  (does work)
./lcong.py -x 1 -a 1103515245 -c 453816694 -m "2**31 - 3"  (does work)
./lcong.py -x 1 -a 1103515245 -c 453816694 -m "2**31 - 4"  (does not work)
./lcong.py -x 1 -a 1103515245 -c 12345 -m "2**31"          (cpp implementation, does NOT work)
./lcong.py -x 1 -a 1103515245 -c 12345 -m "2**31 - 1"      (slight change to cpp implementation, does work)
./lcong.py -x 1 -a "7**5" -c 0 -m "2**31 - 1"              ("extensively studied and shown to be good")
                                                           https://www.cse.wustl.edu/~jain/iucee/ftp/k_26rng.pdf p46

From what I learned so far is that often times when someone writes something
like "MOD = 2**N" they actually MEAN "MOD = 2**N - 1".

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

    parser.add_argument("-i", "--input", help="perform tests on input file")

    parser.add_argument("-x", type=int, help="initial x in (a*x + c) mod m",
                        default=1)

    parser.add_argument("-a", type=str, help="interval for parameter "
                        "scan of a in (a*x + c) mod m", nargs="+",
                        default=["3141592621"])
    parser.add_argument("-c", type=str, help="interval for parameter "
                        "scan of c in (a*x + c) mod m", nargs="+",
                        default=["1"])
    parser.add_argument("-m", type=str, help="interval for parameter "
                        "scan of m in (a*x + c) mod m, should "
                        "be bigger than 2^11", nargs="+",
                        default=["10 ** 10"])

    parser.add_argument("-p", "--print", help="print sequence of random "
                        "numbers to screen", type=int)
    parser.add_argument("-f", "--force", help="force recalculation",
                        action="store_true")
    parser.add_argument("-j", help="number of parallel processes in runs test",
                        type=int, default=4)
    parser.add_argument("-t", "--test", help="perform unittests and exit",
                        action="store_true")

    args = parser.parse_args()
    return args

def perform_unittests():
    """
    Start unittest for the program.
    """
    tests = unittest.TestLoader().discover('.')
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
    if args.input:
        binary_sequence = parse_file.parse_from_file(args.input)
        cl.info("Testing random numbers from file {}".format(args.input))
    else:
        cl.info("Starting LCG testing")

    cl.verbose("Using {} processes in parallel (in (long) runs test)".format(
        args.j))

    if not args.force:
        cl.info("Skipping parameters where the results are already calculated")
        cl.info("To disable skipping consider setting the '-f' flag")

    # run the tests for the LCG (or the random data provided)
    run_tests.run_tests(args, binary_sequence)

if __name__ == "__main__":
    main()
