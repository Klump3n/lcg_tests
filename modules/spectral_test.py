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
        self.par_x0 = parameters["x0"]
        self.par_a = parameters["a"]
        self.par_c = parameters["c"]
        self.par_m = parameters["m"]

        self.random_numbers = gpn.gen_nums(parameters)

        # perform calculations
        self._step_1()

    def _step_1(self):
        """
        Initialization step for dimension t=2.

        """
        cl.debug("Step 1 (Initialization)")
        self._h = self.par_a
        self._hprime = self.par_m
        self._p = 1
        self._pprime = 0
        self._r = self.par_a
        self._s = 1 + self.par_a * self.par_a

        # (p - a*h) mod m == (p' - a*h') mod m
        assert(
            (self._h - self.par_a * self._p) % self.par_m
            ==
            (self._hprime - self.par_a * self._pprime) % self.par_m
        )

        # h*p' - h'*p == +-m
        subtr = self._h * self._pprime - self._hprime * self._p
        assert(
            subtr == 1*self.par_m or subtr == -1*self.par_m
        )

        # go to step 2
        self._step_2()

    def _step_2(self):
        """
        Perform a step for dimension t=2.

        """
        cl.debug("Step 2")

        self._q = np.floor(self._hprime / self._h)

        self._u = self._hprime - self._q * self._h
        self._v = self._pprime - self._q * self._p

        distsq = self._u * self._u + self._v * self._v

        if distsq < self._s:

            self._s = distsq
            self._hprime = self._h
            self._h = self._u
            self._pprime = self._p
            self._p = self._v

            # redo step 2
            self._step_2()

        else:
            self._step_3()

    def _step_3(self):
        """
        Perform step 3.

        """
        cl.debug("Step 3")

        self._u = self._u - self._h
        self._v = self._v - self._p

        distsq = self._u * self._u + self._v * self._v

        if distsq < self._s:

            self._s = distsq
            self._hprime = self._u
            self._pprime = self._v

            self._step_3()

        else:
            print("v2 = {}".format(np.sqrt(self._s)))
            self._intermediate_step_3()
            self._step_4()

    def _intermediate_step_3(self):
        """
        Set up the matrices for higher dimensions.

        """
        self._mat_U = np.asarray([
            [ -1*self._h      , +1*self._p      ],
            [ -1*self._hprime , +1*self._pprime ]
        ])

        prefactor = -1 if self._pprime > 0 else +1
        self._mat_V = prefactor * np.asarray([
            [ +1*self._pprime , +1*self._hprime ],
            [ -1*self._p      , -1*self._h      ]
        ])

    def visualize(self):
        """
        Visualize the random numbers in two dimensions.

        """
        points = 200
        x = np.asarray(self.random_numbers[0:points]) / self.par_m
        y = np.asarray(self.random_numbers[1:points+1]) / self.par_m

        plt.figure()
        plt.plot(x, y, marker="o", ls="None")
        plt.show()
