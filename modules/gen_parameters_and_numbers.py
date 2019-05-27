#!/usr/bin/env python3
"""
Generate a set of random numbers from a LCG.

"""
from util.logging.logger import CoreLog as cl
import modules.lcg as lcg

import numpy as np

def parameter_sweep(
        x0,
        a_min=1,
        a_max=2**4-1,
        c_min=1,
        c_max=2**4-1,
        mod_min=2**11-1,
        mod_max=2**12,
):
    """
    Generate a list of parameters.

    Since we would like to have 20000 bits in a sequence, we need a modulus big
    enough to not repeat in those 20000 digits.

    That should be from roughly 2^11 onwards, since 2^11 needs 11 bits per
    number, and 2^11 = 2048.
    11*2^11 = 22528 bits

    """
    output_list = list()

    for mod in range(mod_min, mod_max+1):
        for c in range(c_min, c_max+1):
            if (c > mod - 1):
                break
            for a in range(a_min, a_max+1):
                if (a > mod - 1):
                    break
                param = dict()
                param["x0"] = int(x0)
                param["a"] = int(a)
                param["c"] = int(c)
                param["m"] = int(mod)
                output_list.append(param)

    cl.info("Created {} parameters".format(len(output_list)))
    cl.info("At one second per check this will take about {} seconds (or "
            "{:.2f} minutes; or {:.2f} hours)".format(
                len(output_list),
                len(output_list)/60,
                len(output_list)/3600)
    )

    return output_list

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

    # x0 = 1231551
    # m = 2**35
    # a = 2**18 + 1
    # c = 3

    # # bad parameters
    # x0 = 1
    # a = 5
    # c = 0
    # m = 9

    # # THIS WORKS
    # # x0 was random, a, c correct, m = m - 1 (Knuth, Eq. (38))
    # x0 = 112312219              # random but odd
    # a = 65539
    # c = 0
    # m = 2**31 - 1               # normally 2**31


    # https://www.cse.wustl.edu/~jain/iucee/ftp/k_26rng.pdf p46
    # "extensively studied and shown to be good"
    # yep, it works
    x0 = 1
    # a = 7**5
    # a = 48271
    # a = 69621
    a = 6303600                 # my own
    # a = 63036001
    c = 0
    m = 2**31 -1

    # shown to be bad
    # yep, it's bad
    x0 = 1
    a = 2**16 + 3
    c = 0
    m = 2**31

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

        if n > 0:
            padding = len("{:b}".format(2**(n-1)))
        else:
            padding = 1
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
