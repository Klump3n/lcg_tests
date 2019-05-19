#!/usr/bin/env python3
"""
Generate a set of random numbers from a LCG.

"""
from util.logging.logger import CoreLog as cl
import modules.lcg as lcg

import numpy as np

def gen_params():
    """
    Generate a set of parameters for the LCG.

    APPARENTLY

    m=2**k
    a=4c+1

    """

    # # paper
    # x0 = 1 + i
    # a = 33                  # 231
    # c = 0
    # m = 251

    # # microsoft
    # x0 = 1 + i
    # a = 214013
    # c = 2531011
    # m = 2**31

    x0 = 1231551
    m = 2**35
    a = 2**18 + 1
    c = 3

    # # bad parameters
    # x0 = 1
    # a = 5
    # c = 0
    # m = 9

    # # cpp
    # # x0 = 5491                   # fails
    # x0 = 549                   # works
    # m = 2**31
    # a = 1103515245
    # c = 12345


    params = dict()
    params["x0"] = x0 # 1
    params["a"] = a # 5
    params["c"] = c # 0
    params["m"] = m # 9

        # paramlist.append(params)


    # for x0 in range(1,10):
    #     for a in range(1,10):
    #         for c in range(1,10):
    #             for n in range(1,4):
    #                 m = 2**n
    #                 params = dict()
    #                 params["x0"] = x0 # 1
    #                 params["a"] = a # 5
    #                 params["c"] = c # 0
    #                 params["m"] = m # 9

    #                 paramlist.append(params)
    # return paramlist
    return params

def gen_expected_statistic(modulus):
    """
    Generate the ratio of 0s to 1s for a given modulus.

    """
    nums = list()

    # put every number until modulus in a list
    for i in range(modulus):
        nums.append(i)

    binary_nums = gen_binary_nums(nums, modulus=modulus)
    binary_sequence = gen_binary_sequence(
        binary_nums, length=modulus*len(binary_nums))

    bin_sorted = sorted(binary_sequence)
    one_zero, counts = np.unique(bin_sorted, return_counts=True)

    zero_over_one = counts[0] / counts[1]

    return zero_over_one

def gen_nums(params, length=20000):
    """
    Generate a list of pseudorandom numbers with the LCG.

    """
    x0 = params["x0"]
    a = params["a"]
    c = params["c"]
    m = params["m"]

    # output list
    res = list()

    cl.verbose(
        "Generating pseudorandom numbers for parameters x0 = {}, a = {}, "
        "c = {}, m = {}".format(x0, a, c, m))

    for _ in range(length):
        x0 = lcg.lcg(x0, a, c, m)
        res.append(x0)

    return res

def gen_binary_nums(nums, modulus=None):
    """
    Turn a list of numbers into a list of binary numbers.

    Optional modulus for padding the numbers.

    """
    res = list()

    padding = 0

    if modulus:
        n = 0
        while 2**n < modulus:
            n += 1

        padding = len("{:b}".format(2**(n-1)))
        cl.verbose("Padding numbers to {} digits".format(padding))

    for num in nums:
        res.append("{:b}".format(num).zfill(padding))

    return res

def gen_binary_sequence(binary_nums, length=20000):
    """
    Turn a list of binary numbers into a sequence.

    """
    res = str()

    for num in binary_nums:
        res += num

    res = res[0:length]

    return res
