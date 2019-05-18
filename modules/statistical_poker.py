#!/usr/bin/env python3
"""
Implements the poker test.

http://csrc.nist.gov/publications/fips/fips1401.htm

"""
from util.logging.logger import CoreLog as cl

import numpy as np

def poker_passed(binary_sequence):
    """
    Perform the poker test on the binary sequence.

    Binary sequence must be a string.

    """
    b = binary_sequence

    # divide the binary sequence into 4 bit sequences and count the occurences
    # of each of the 16 possible sequences
    c = list()
    for j in range(5000):
        c.append(b[4*j:4*j+4])

    _, f = np.unique(c, return_counts=True)

    res = 16/5000 * sum(f*f) - 5000

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
