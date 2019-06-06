#!/usr/bin/env python3
"""
Performs the spectral test.

"""
import sys
import numpy as np

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
        cl.verbose("Calling spectral_test with parameters {}".format(parameters))

        cl.debug("Recursion limit is set to {}".format(sys.getrecursionlimit()))
        new_recursion_limit = 10000
        cl.debug("Setting recursion limit to {}".format(new_recursion_limit))
        sys.setrecursionlimit(new_recursion_limit)

        self._T = T

        self.par_x0 = parameters["x0"]
        self.par_a = parameters["a"]
        self.par_c = parameters["c"]
        self.par_m = parameters["m"]

        self.results = [None] * (T+1)

        # calc v2 and prepare everything for higher dimensionality
        self._step_1()

        # calc higher dimensional v values
        while (self._t < self._T):
            self._step_4()

    def get_results(self):
        """
        Return the results list.

        """
        return self.results

    def _step_1(self):
        """
        Initialization step for dimension t=2.

        """
        cl.verbose("Calculating v2")
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
            cl.verbose("v2 = {}".format( np.sqrt(self._s) ))
            self.results[self._t] = np.sqrt(self._s)
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
        # self._step_4()

    def _step_4(self):
        """
        Step 4.

        """
        cl.debug("Step 4 (Advance t)")

        self._t += 1
        cl.verbose("Calculating v{}".format(self._t))

        # enlarge matrices
        shape_u_x, shape_u_y = self._mat_U.shape
        U = np.zeros( (shape_u_x + 1, shape_u_y + 1) )
        U[:shape_u_x, :shape_u_y] = self._mat_U
        self._mat_U = U.copy()

        shape_v_x, shape_v_y = self._mat_V.shape
        V = np.zeros( (shape_v_x + 1, shape_v_y + 1) )
        V[:shape_v_x, :shape_v_y] = self._mat_V
        self._mat_V = V.copy()

        self._r = (self.par_a * self._r) % self.par_m

        Ut = np.zeros( (1, self._t) )
        Ut[0, 0] = -1*self._r
        Ut[0, -1] = 1

        Vt = np.zeros( (1, self._t) )
        Vt[0, -1] = self.par_m

        self._mat_U[self._t - 1, :] = Ut
        self._mat_V[self._t - 1, :] = Vt

        for i in range(self._t - 1):
            self._q = np.round(self._mat_V[i, 0] * self._r / self.par_m)
            self._mat_V[i, self._t - 1] = self._mat_V[i, 0] * self._r - self._q * self.par_m
            self._mat_U[self._t - 1, :] = self._mat_U[self._t - 1, :] + self._q * self._mat_U[i, :]

        Ut = self._mat_U[self._t - 1, :]
        self._s = np.min( [self._s, (Ut @ Ut) ])

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

            ViVj = (self._mat_V[i, :] @ self._mat_V[self._j, :])
            VjVj = (self._mat_V[self._j, :] @ self._mat_V[self._j, :])

            if not (i == self._j) and (2 * np.abs(ViVj) > VjVj):
                self._q = np.round(ViVj / VjVj)
                self._mat_V[ i       , : ] = self._mat_V[ i       , : ] - self._q * self._mat_V[ self._j , : ]
                self._mat_U[ self._j , : ] = self._mat_U[ self._j , : ] + self._q * self._mat_U[ i       , : ]
                self._k = self._j

        self._step_6()

    def _step_6(self):
        """
        Step 6.

        """
        cl.debug("Step 6 (Examine new bound)")
        if (self._k == self._j):
            value = self._mat_U[self._j, :] @ self._mat_U[self._j, :]
            self._s = np.min([self._s, value])

        self._step_7()

    def _step_7(self):
        """
        Step 7.

        """
        cl.debug("Step 7 (Advance j)")

        if (self._j == self._t - 1):
            self._j = 1 - 1     # 0
        else:
            self._j += 1

        if not (self._j == self._k):
            self._step_5()
        else:
            self._step_8()

    def _step_8(self):
        """
        Step 8.

        """
        cl.debug("Step 8 (Prepare for search)")

        self._X = np.zeros((1, self._t))
        self._Y = np.zeros((1, self._t))
        self._Z = np.zeros((1, self._t))

        self._k = self._t - 1

        for j in range(self._t):
            VjVj = self._mat_V[j, :].T @ self._mat_V[j, :]
            self._Z[0, j] = np.floor(np.sqrt(np.floor(VjVj * self._s / self.par_m / self.par_m)))

        self._step_9()

    def _step_9(self):
        """
        Step 9.

        """
        cl.debug("Step 9 (Advance x_k)")

        if (self._X[0, self._k] == self._Z[0, self._k]):
            self._step_11()
        else:
            self._X[0, self._k] += 1
            self._Y[0, :] = self._Y[0, :] + self._mat_U[self._k, :]
            self._step_10()

    def _step_10(self):
        """
        Step 10.

        """
        cl.debug("Step 10 (Advance k)")

        self._k += 1

        if (self._k <= self._t - 1):
            self._X[0, self._k] = -1*self._Z[0, self._k]
            self._Y[0, :] = self._Y[0, :] - 2 * self._Z[0, self._k] * self._mat_U[self._k, :]
            self._step_10()
        else:
            value = self._Y[0, :].T @ self._Y[0, :]
            self._s = np.min([self._s, value])
            self._step_11()

    def _step_11(self):
        """
        Step 11.

        """
        cl.debug("Step 11 (Decrease k)")

        self._k -= 1

        if (self._k >= 0):       # adjusted index
            self._step_9()
        else:
            cl.verbose("v{} = {}".format(self._t, np.sqrt(self._s)))
            self.results[self._t] = np.sqrt(self._s)
