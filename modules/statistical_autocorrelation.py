#!/usr/bin/env python3
"""
Perform autocorrelation tests.

"""
import numpy as np

import multiprocessing
from itertools import repeat

from util.logging.logger import CoreLog as cl

def autocorrelate_tau(bin_seq, tau):
    """
    XOR a part of the given binary sequence with a shifted (by tau) part of the
    same sequence. return the sum.

    This is bitwise autocorrelation.
    http://noosphere.princeton.edu/bitwise.autocorrelation.html

    """
    seq1 = bin_seq[0:5000]
    seq2 = bin_seq[tau:tau+5000]
    return np.sum(seq1 ^ seq2)  # XOR of two lists

def autocorrelation_passed(binary_sequence):
    """
    Returns if the binary sequence passes the autocorrelation test.

    """
    test_passed = True

    b = np.asarray(list(binary_sequence), dtype=int)

    seqset = int(len(binary_sequence) / 4)
    tau = range(1,seqset)

    with multiprocessing.Pool(4) as p:
        res = p.starmap(autocorrelate_tau, zip(repeat(b), tau))

    for t, ctau in enumerate(res):
        if not (2326 < ctau) or not (ctau < 2674):
            cl.verbose_warning("Autocorrelation failed for tau = {}, needs "
                               "2326 < {} < 2674".format(t, ctau))
            test_passed = False

    if test_passed:
        cl.verbose("Autocorrelation test passed")
    else:
        cl.verbose_warning("Autocorrelation test failed")

    return test_passed
