#!/usr/bin/env python3
"""
Perform a runs test on the binary sequence.

"""
import numpy as np

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
    for count in [zc1, oc1]:
        if not (2267 <= count) and not (count <= 2733):
            test_passed = False
    if test_passed:
        cl.verbose("Runs test: {} of 0 and {} of 1 of length {}".format(
            zc1, oc1, 1))
    else:
        cl.verbose_warning("Runs test: {} of 0 and {} of 1 of length {}".format(
            zc1, oc1, 1))
        return test_passed

    zc2, oc2 = runs_instance(binary_sequence, 2)
    for count in [zc2, oc2]:
        if not (1079 <= count) or not (count <= 1421):
            test_passed = False
    if test_passed:
        cl.verbose("Runs test: {} of 0 and {} of 1 of length {}".format(
            zc2, oc2, 2))
    else:
        cl.verbose_warning("Runs test: {} of 0 and {} of 1 of length {}".format(
            zc2, oc2, 2))
        return test_passed

    zc3, oc3 = runs_instance(binary_sequence, 3)
    for count in [zc3, oc3]:
        if not (502 <= count) or not (count <= 748):
            test_passed = False
    if test_passed:
        cl.verbose("Runs test: {} of 0 and {} of 1 of length {}".format(
            zc3, oc3, 3))
    else:
        cl.verbose_warning("Runs test: {} of 0 and {} of 1 of length {}".format(
            zc3, oc3, 3))
        return test_passed

    zc4, oc4 = runs_instance(binary_sequence, 4)
    for count in [zc4, oc4]:
        if not (223 <= count) or not (count <= 402):
            test_passed = False
    if test_passed:
        cl.verbose("Runs test: {} of 0 and {} of 1 of length {}".format(
            zc4, oc4, 4))
    else:
        cl.verbose_warning("Runs test: {} of 0 and {} of 1 of length {}".format(
            zc4, oc4, 4))
        return test_passed

    zc5, oc5 = runs_instance(binary_sequence, 5)
    for count in [zc5, oc5]:
        if not (90 <= count) or not (count <= 223):
            test_passed = False
    if test_passed:
        cl.verbose("Runs test: {} of 0 and {} of 1 of length {}".format(
            zc5, oc5, 5))
    else:
        cl.verbose_warning("Runs test: {} of 0 and {} of 1 of length {}".format(
            zc5, oc5, 5))
        return test_passed

    zc6p = 0
    oc6p = 0

    for it in range(6, 34):
        zc, oc = runs_instance(binary_sequence, it)
        zc6p += zc
        oc6p += oc

    for count in [zc6p, oc6p]:
        if not (90 <= count) or not (count <= 223):
            test_passed = False
    if test_passed:
        cl.verbose("Runs test: {} of 0 and {} of 1 of length {}".format(
            zc6p, oc6p, "6+"))
    else:
        cl.verbose_warning("Runs test: {} of 0 and {} of 1 of length {}".format(
            zc6p, oc6p, "6+"))
        return test_passed
    return test_passed

def long_runs_passed(binary_sequence):
    """
    Perform a runs test with length 34 or more.

    """
    test_passed = True
    for length in range(34, len(binary_sequence)):
        zeros = "0"*length
        ones = "1"*length
        if zeros in binary_sequence:
            cl.verbose_warning("length {} of 0 in binary_sequence".format(length))
            test_passed = False
        if ones in binary_sequence:
            cl.verbose_warning("length {} of 1 in binary_sequence".format(length))
            test_passed = False

    return test_passed
