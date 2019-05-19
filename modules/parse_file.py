#!/usr/bin/env python3
"""
Parse random numbers from a file.

"""
import numpy as np

def parse_from_file(file_name):
    """
    Parse random numbers from the provided file name.

    """
    data = str()
    binary_data = np.genfromtxt(file_name, dtype=str, delimiter="")

    if len(binary_data.shape) == 1:
        for i in binary_data:
            data += i

    if len(binary_data.shape) == 2:
        for inner_bin in binary_data:
            for i in inner_bin:
                data += i

    return data[:20000]         # length of 20000 is required, tests are adjusted for that.
