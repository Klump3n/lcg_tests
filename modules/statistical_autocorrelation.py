#!/usr/bin/env python3
"""
Perform autocorrelation tests.

"""
import numpy as np

from util.logging.logger import CoreLog as cl

def autocorrelation_passed(binary_sequence):
    """
    Returns if the binary sequence passes the autocorrelation test.

    """
    test_passed = True

    seqset = int(len(binary_sequence) / 4)
    tau = range(1,seqset)
    v = np.asarray(list(binary_sequence[0:seqset]), dtype=int)
    for t in tau:
        vtau = np.asarray(list(binary_sequence[t:t+seqset]), dtype=int)
        ctau = np.sum(v ^ vtau)  # XOR
        if not (2326 < ctau) or not (ctau < 2674):
            cl.verbose_warning("Autocorrelation failed for tau = {}, needs "
                               "2326 < {} < 2674".format(t, ctau))
            test_passed = False

    if test_passed:
        cl.verbose("Autocorrelation test passed")
    else:
        cl.verbose_warning("Autocorrelation test failed")

    return test_passed
