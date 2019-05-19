#!/usr/bin/env python3
"""
Perform a runs test on the binary sequence.

http://csrc.nist.gov/publications/fips/fips1401.htm

"""
import numpy as np

import multiprocessing
from itertools import repeat

from util.logging.logger import CoreLog as cl


def runs_instance(binary_sequence, length=1):
    """
    Perform a runs test for a given instance.

    """
    ones = "0{}0".format("1" * length)
    zeros = "1{}1".format("0" * length)

    substrings = list()
    for i, k in enumerate(binary_sequence):
        sstring = binary_sequence[i:i+2+length]
        if len(sstring) == 2+length:
            substrings.append(sstring)

    string_instance, instance_count = np.unique(
        substrings, return_counts=True)

    zero_count = 0
    one_count = 0

    for it, inst in enumerate(string_instance):
        if inst == zeros:
            zero_count = instance_count[it]
        if inst == ones:
            one_count = instance_count[it]

    return zero_count, one_count

def runs_passed(binary_sequence):
    """
    Perform a runs test.

    Length of Run 	Required Interval
    1 	            2267-2733
    2 	            1079-1421
    3 	            502-748
    4 	            223-402
    5 	            90-223
    6 (or more)     90-223

    """
    test_passed = True

    zc1, oc1 = runs_instance(binary_sequence, 1)
    pass1 = True
    for count in [zc1, oc1]:
        if not (2267 <= count) and not (count <= 2733):
            pass1 = False
            test_passed = False
    if pass1:
        cl.verbose("Runs test: {} 0 runs and {} 1 runs of length {}".format(
            zc1, oc1, 1))
    else:
        cl.verbose_warning("Runs test: {} 0 runs and {} 1 runs of length {} "
                           "(not in [2267, 2733])".format(zc1, oc1, 1))


    zc2, oc2 = runs_instance(binary_sequence, 2)
    pass2 = True
    for count in [zc2, oc2]:
        if not (1079 <= count) or not (count <= 1421):
            pass2 = False
            test_passed = False
    if pass2:
        cl.verbose("Runs test: {} 0 runs and {} 1 runs of length {}".format(
            zc2, oc2, 2))
    else:
        cl.verbose_warning("Runs test: {} 0 runs and {} 1 runs of length {} "
                           "(not in [1079, 1421])".format(zc2, oc2, 2))

    zc3, oc3 = runs_instance(binary_sequence, 3)
    pass3 = True
    for count in [zc3, oc3]:
        if not (502 <= count) or not (count <= 748):
            pass3 = False
            test_passed = False
    if pass3:
        cl.verbose("Runs test: {} 0 runs and {} 1 runs of length {}".format(
            zc3, oc3, 3))
    else:
        cl.verbose_warning("Runs test: {} 0 runs and {} 1 runs of length {} "
                           "(not in [502, 748])".format(zc3, oc3, 3))

    zc4, oc4 = runs_instance(binary_sequence, 4)
    pass4 = True
    for count in [zc4, oc4]:
        if not (223 <= count) or not (count <= 402):
            pass4 = False
            test_passed = False
    if pass4:
        cl.verbose("Runs test: {} 0 runs and {} 1 runs of length {}".format(
            zc4, oc4, 4))
    else:
        cl.verbose_warning("Runs test: {} 0 runs and {} 1 runs of length {} "
                           "(not in [223, 402])".format(zc4, oc4, 4))

    zc5, oc5 = runs_instance(binary_sequence, 5)
    pass5 = True
    for count in [zc5, oc5]:
        if not (90 <= count) or not (count <= 223):
            pass5 = False
            test_passed = False
    if pass5:
        cl.verbose("Runs test: {} 0 runs and {} 1 runs of length {}".format(
            zc5, oc5, 5))
    else:
        cl.verbose_warning("Runs test: {} 0 runs and {} 1 runs of length {} "
                           "(not in [90, 223])".format(zc5, oc5, 5))

    zc6p = 0
    oc6p = 0

    lengths = range(6, 34)
    with multiprocessing.Pool(4) as p:
        res = p.starmap(runs_instance, zip(repeat(binary_sequence), lengths))

    for r in res:
        zc6p += r[0]
        oc6p += r[1]

    pass6 = True
    for count in [zc6p, oc6p]:
        if not (90 <= count) or not (count <= 223):
            pass6 = False
            test_passed = False
    if pass6:
        cl.verbose("Runs test: {} 0 runs and {} 1 runs of length {}".format(
            zc6p, oc6p, "6+"))
    else:
        cl.verbose_warning("Runs test: {} 0 runs and {} 1 runs of length {} "
                           "(not in [90, 223])".format(zc6p, oc6p, "6+"))

    if test_passed:
        cl.verbose("Runs test passed, all within tolerance")
    else:
        cl.verbose_warning("Runs test failed")

    return test_passed

def long_runs_instance(binary_sequence, length):
    """
    One instance (length) of the long runs test.

    """
    test_passed = True

    zeros = "0"*length
    if zeros in binary_sequence:
        cl.verbose_warning("length {} of 0 in binary_sequence".format(length))
        test_passed = False

    ones = "1"*length
    if ones in binary_sequence:
        cl.verbose_warning("length {} of 1 in binary_sequence".format(length))
        test_passed = False

    return test_passed

def long_runs_passed(binary_sequence):
    """
    Perform a runs test with length 34 or more.

    """
    test_passed = True

    lengths = range(34, len(binary_sequence))
    with multiprocessing.Pool(4) as p:
        res = p.starmap(long_runs_instance, zip(repeat(binary_sequence), lengths))

    for r in res:
        if r is False:
            test_passed = False

    if test_passed:
        cl.verbose("Long runs test passed, no long runs")
    else:
        cl.verbose_warning("Long runs test failed")

    return test_passed
