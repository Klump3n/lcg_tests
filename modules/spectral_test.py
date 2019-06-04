#!/usr/bin/env python3
"""
Performs the spectral test.

"""
import numpy as np
from matplotlib import pyplot as plt

import modules.gen_parameters_and_numbers as gpn

from util.logging.logger import CoreLog as cl

class SpectralTest:
    """
    Performs the spectral test.

    We follow D. Knuth, pp.98

    """
    def __init__(self, parameters):
        """
        Generate random numbers and so on.

        """
        cl.debug("Calling spectral_test with parameters {}".format(parameters))
        self.x0 = parameters["x0"]
        self.a = parameters["a"]
        self.c = parameters["c"]
        self.m = parameters["m"]

        self.random_numbers = gpn.gen_nums(parameters)


    def visualize(self):
        """
        Visualize the random numbers in two dimensions.

        """
        points = 1000
        x = np.asarray(self.random_numbers[0:points]) / self.m
        y = np.asarray(self.random_numbers[1:points+1]) / self.m

        plt.figure()
        plt.plot(x, y, marker="o", ls="None")
        plt.show()
