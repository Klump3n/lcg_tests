#!/usr/bin/env python3
"""
Generate a set of random numbers from a LCG.

"""
from util.logging.logger import CoreLog as cl
import modules.lcg as lcg

def gen_params():
    """
    Generate a set of parameters for the LCG.

    """
    # cpp
    m = 2**31
    a = 1103515245
    c = 12345

    x0 = 54911

    params = dict()
    params["x0"] = x0 # 1
    params["a"] = a # 5
    params["c"] = c # 0
    params["m"] = m # 9

    return params

def gen_nums(params):
    """
    Generate a binary sequence with the LCG.

    """
    x0 = params["x0"]
    a = params["a"]
    c = params["c"]
    m = params["m"]

    # store the result in a string
    binary_sequence = ""

    cl.verbose(
        "Generating binary sequence for parameters x0 = {}, a = {}, c = {}, m = {}".format(
            x0, a, c, m))

    # cl.info("Generating binary sequence")
    while len(binary_sequence) < 20000:
        x0 = lcg.lcg(x0, a, c, m)
        binary_sequence += "{:b}".format(x0)

    # prune the binary sequence to be exactly 20000 digits long
    binary_sequence = binary_sequence[:20000]

    return binary_sequence
