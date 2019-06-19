#!/usr/bin/env python3
"""
Perform autocorrelation tests.

"""
import numpy as np
from matplotlib import pyplot as plt

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

def autocorrelation_passed(binary_sequence, plot=False):
    """
    Returns if the binary sequence passes the autocorrelation test.

    """
    test_passed = True

    b = np.asarray(list(binary_sequence), dtype=int)

    seqset = int(len(binary_sequence) / 4)
    tau = range(1, seqset)

    with multiprocessing.Pool(4) as p:
        res = p.starmap(autocorrelate_tau, zip(repeat(b), tau))

    failcount = 0

    plot_x = list()
    plot_y = list()

    for t, ctau in enumerate(res):

        plot_x.append(t+1)
        plot_y.append(ctau)

        if not (2326 < ctau) or not (ctau < 2674):
            # cl.verbose_warning("Autocorrelation test failed for tau = {}, "
            #                    "2326 !< {} !< 2674".format(t, ctau))
            test_passed = False
            failcount += 1

    if test_passed:
        cl.verbose("Autocorrelation test passed, no correlations found")
    else:
        cl.verbose_warning("Autocorrelation test failed "
                           "for {}/{} sequences".format(
                               failcount, len(tau)))

    if plot:
        plt.figure()
        plt.plot(plot_x, plot_y, zorder=0)
        plt.hlines([2326, 2500, 2674], xmin=0, xmax=5000, color="r", linestyle="dashed", zorder=1)
        plt.xlabel(r"Indexshift $n$")
        plt.ylabel(r"$X_{n} = \sum_{j} b_j \oplus b_{j+n}$")
        plt.xlim([-1, 5001])
        plt.tight_layout()
        plt.show()

    return test_passed
