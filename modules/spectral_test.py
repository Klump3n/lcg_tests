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
    def __init__(self, parameters, T=3):
        """
        Generate random numbers and so on.

        """
        cl.debug("Calling spectral_test with parameters {}".format(parameters))

        self._T = T

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

        self._t = 2

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
        cl.debug("Step 2 (Euclidean step)")

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
        cl.debug("Step 3 (Compute v2)")

        self._u = self._u - self._h
        self._v = self._v - self._p

        distsq = self._u * self._u + self._v * self._v

        if distsq < self._s:

            self._s = distsq
            self._hprime = self._u
            self._pprime = self._v

            self._step_3()

        else:
            cl.info("v2 = {}".format( np.sqrt(self._s) ))
            self._intermediate_step_3()

    def _intermediate_step_3(self):
        """
        Set up the matrices for higher dimensions.

        """
        cl.debug("Intermediate step, preparing matrices for higher dimensions")
        self._mat_U = np.asarray([
            [ -1*self._h      , +1*self._p      ],
            [ -1*self._hprime , +1*self._pprime ]
        ])

        prefactor = -1 if self._pprime > 0 else +1
        self._mat_V = prefactor * np.asarray([
            [ +1*self._pprime , +1*self._hprime ],
            [ -1*self._p      , -1*self._h      ]
        ])
        self._step_4()

    def _step_4(self):
        """
        Step 4.

        """
        cl.debug("Step 4 (Advance t)")

        # enlarge matrices
        shape_u_x, shape_u_y = self._mat_U.shape
        U = np.zeros( (shape_u_x + 1, shape_u_y + 1) )
        U[:shape_u_x, :shape_u_y] = self._mat_U
        self._mat_U = U.copy()

        shape_v_x, shape_v_y = self._mat_V.shape
        V = np.zeros( (shape_v_x + 1, shape_v_y + 1) )
        V[:shape_v_x, :shape_v_y] = self._mat_V
        self._mat_V = V.copy()

        self._t += 1

        self._r = (self.par_a * self._r) % self.par_m

        Ut = np.zeros( (1, self._t) )
        Ut[0, 0] = -1*self._r
        Ut[0, -1] = 1

        Vt = np.zeros( (1, self._t) )
        Vt[0, -1] = self.par_m

        self._mat_V[:, self._t - 1] = Vt

        for i in range(self._t - 1):
            self._q = np.round(self._mat_V[i, 0] * self._r / self.par_m)
            self._mat_V[i, self._t - 1] = self._mat_V[i, 0] * self._r - self._q * self.par_m
            Ut = Ut + self._q * self._mat_U[i, :]
            self._mat_U[self._t - 1, :] = Ut

        self._s = np.min( [self._s, int((Ut @ Ut.T)[0, 0]) ] )

        # adjust indices by 1
        self._k = self._t - 1
        self._j = 1 - 1

        self._step_5()

    def _step_5(self):
        """
        Step 5.

        """
        cl.debug("Step 5 (Transform)")

        for i in range(self._t):
            ViVj = (self._mat_V[:, i] @ self._mat_V[:, self._j])
            VjVj = (self._mat_V[:, self._j] @ self._mat_V[:, self._j])
            if not (i == self._j) and (2 * np.abs(ViVj) > VjVj):
                self._q = np.round(ViVj / VjVj)
                self._mat_V[:, i] = self._mat_V[:, i] - self._q * self._mat_V[:, self._j]
                self._mat_U[:, self._j] = self._mat_U[:, self._j] - self._q * self._mat_U[:, i]
                self._k = self._j

        self._step_6()

    def _step_6(self):
        """
        Step 6.

        """
        cl.debug("Step 6 (Examine new bound)")
        if (self._k == self._j):
            value = self._mat_U[:, self._j] @ self._mat_U[:, self._j]
            self._s = np.min([self._s, value])

        self._step_7()

    def _step_7(self):
        """
        Step 7.

        """
        cl.debug("Step 7 (Advance j)")

        if (self._j == self._t - 1):
            self._j = 1 - 1
        else:
            self._j += 1

        if (self._j == self._k):
            self._step_5()

        self._step_8()

    def _step_8(self):
        """
        Step 8.

        """
        cl.debug("Step 8 (Prepare for search)")

        X = np.zeros((1, self._t))
        Y = np.zeros((1, self._t))
        Z = np.zeros((1, self._t))

        self._j = self._t - 1

        for j in range(self._t):
            VjVj = self._mat_V[:, j].T @ self._mat_V[:, j]
            Z[0, j] = np.floor(np.sqrt(np.floor(VjVj * self._s / self.par_m / self.par_m)))

        cl.warning("NOT DONE")

    def _step_9(self):
        """
        Step 9.

        """
        cl.debug("Step 9 (Advance x_k)")

    def _step_10(self):
        """
        Step 10.

        """
        cl.debug("Step 10 (Advance k)")

    def _step_11(self):
        """
        Step 11.

        """
        cl.debug("Step 11 (Decrease k)")


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
