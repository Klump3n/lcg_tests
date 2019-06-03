#!/usr/bin/env python3
"""
Implements the monobit test.

http://csrc.nist.gov/publications/fips/fips1401.htm

"""
from util.logging.logger import CoreLog as cl

def monobit_passed(binary_sequence):
    """
    Test the binary sequence for occurences of 0 and 1.

    Binary sequence must be a string.

    """
    bin_len = len(binary_sequence)
    bin_sum = sum([int(i) for i in binary_sequence])

    ratio = bin_sum/bin_len

    lower_bound = 9654/20000
    upper_bound = 10346/20000
    if (lower_bound < ratio < upper_bound):
        cl.verbose("Monobit test passed, ratio is {:.4f}".format(ratio))
        return True
    else:
        cl.verbose_warning("Monobit test failed, ratio is {:.4f}".format(ratio))
        cl.verbose_warning("The ratio should be between {:.4f} and {:.4f}".format(
            lower_bound, upper_bound))
        return False
