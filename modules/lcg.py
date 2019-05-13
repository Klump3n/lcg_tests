#!/usr/bin/env python3
"""
Implements a Linear Congruential Generator.

"""
def lcg(x0, a, c, m):
    """
    Returns the next number from a linear congruential generator.

    """
    x0 = (a*x0 + c) % m
    return x0
