#!/usr/bin/env python3
"""
Implements the poker test.

"""
from util.logging.logger import CoreLog as cl

import numpy as np

def poker_passed(binary_sequence):
    """
    Perform the poker test on the binary sequence.

    Binary sequence must be a string.

    """
    if not isinstance(binary_sequence, str):
        cl.error("binary_sequence must be of type 'str'")
        raise TypeError("binary_sequence must be of type 'str'")

    if not (len(binary_sequence) == 20000):
        cl.warning("binary_sequence is {} digits long but should be 20000 "
                   "digits long, this test will not work properly".format(
                       len(binary_sequence)))
        raise ValueError("binary_sequence has wrong size")

    b = binary_sequence
    f = np.zeros(16, dtype=int)

    # divide the binary sequence into 4 bit sequences and count the occuences of
    # each of the 16 possible sequences
    for j in range(5000):
        cj = 8*int(b[4*j]) + 4*int(b[4*j+1]) + 2*int(b[4*j+2]) + int(b[4*j+3])
        f[cj] += 1

    res = 16/5000 * sum([x*x for x in f]) - 5000

    lower_bound = 1.03
    upper_bound = 57.4
    if (lower_bound < res < upper_bound):
        cl.verbose("Poker test passed, result is {:.4f}".format(res))
        return True
    else:
        cl.verbose_warning("Poker test FAILED, result is {:.2f}".format(res))
        cl.verbose_warning("The result should be between {:.2f} and {:.1f}".format(
            lower_bound, upper_bound))
        return False
