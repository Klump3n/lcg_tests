#!/usr/bin/env python3
"""
Perform autocorrelation tests.

"""
import numpy as np

from util.logging.logger import CoreLog as cl

def autocorrelation_passed(binary_sequence, length=20000):
    """
    Returns if the binary sequence passes the autocorrelation test.

    """
    test_passed = True

    seqset = int(length / 4)
    tau = range(1,seqset)
    v = np.asarray(list(binary_sequence[0:seqset]), dtype=int)
    for t in tau:
        vtau = np.asarray(list(binary_sequence[t:t+seqset]), dtype=int)
        ctau = np.sum(v ^ vtau)
        if not (2326 < ctau) or not (ctau < 2674):
            cl.verbose_warning("Autocorrelation failed for tau = {}, needs "
                               "2326 < {} < 2674".format(t, ctau))
            test_passed = False

    return test_passed
