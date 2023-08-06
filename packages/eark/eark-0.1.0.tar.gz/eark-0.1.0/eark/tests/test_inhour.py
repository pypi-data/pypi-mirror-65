"""Unittests for the inhour module
"""

import numpy as np
import pytest

from eark import inhour


class TestInhour:
    @pytest.fixture(scope='class', autouse=True)
    def beta(self):
        return 0.0075

    @pytest.fixture(scope='class', autouse=True)
    def beta_vector(self):
        return np.array([0.033, 0.219, 0.196, 0.395, 0.115, 0.042])

    @pytest.fixture(scope='class', autouse=True)
    def n_initial(self):
        return 4000

    @pytest.fixture(scope='class', autouse=True)
    def period(self):
        return 6.0e-5

    @pytest.fixture(scope='class', autouse=True)
    def precursor_constants(self):
        return np.array([0.0124, 0.0305, 0.1110, 0.3011, 1.1400, 3.0100])

    @pytest.fixture(scope='class', autouse=True)
    def precursor_density(self):
        return np.array([5000, 6000, 5600, 4700, 7800, 6578])

    @pytest.fixture(scope='class', autouse=True)
    def rho(self, beta):
        return 0.5 * beta

    def test_total_neutron_deriv(self, rho, beta, period, n_initial, precursor_constants, precursor_density):
        res = inhour.total_neutron_deriv(rho=rho,
                                         beta=beta,
                                         period=period,
                                         n=n_initial,
                                         precursor_constants=precursor_constants,
                                         precursor_density=precursor_density)
        np.testing.assert_almost_equal(actual=res, desired=-219026.44999999998, decimal=5)

    def test_delay_neutron_deriv(self, period, n_initial, beta_vector, precursor_constants, precursor_density):
        res = inhour.delay_neutron_deriv(beta_vector=beta_vector,
                                         period=period,
                                         n=n_initial,
                                         precursor_constants=precursor_constants,
                                         precursor_density=precursor_density)
        desired = np.array([2199938., 14599817., 13066045.06667, 26331918.16333, 7657774.66667, 2780200.22])
        np.testing.assert_almost_equal(actual=res, desired=desired, decimal=5)

    def test_solve(self, n_initial, precursor_density, precursor_constants, beta_vector, beta, rho, period):
        soln = inhour.solve(n_initial=n_initial,
                            precursor_density_initial=precursor_density,
                            beta_vector=beta_vector,
                            precursor_constants=precursor_constants,
                            rho=rho,
                            total_beta=beta,
                            period=period,
                            t_max=1,
                            num_iters=3)

        desired = np.array([[4.000e+03, 5.000e+03, 6.000e+03, 5.600e+03, 4.700e+03, 7.800e+03, 6.578e+03],
                            [1.881e+15, 1.856e+16, 1.231e+17, 1.100e+17, 2.210e+17, 6.338e+16, 2.241e+16],
                            [2.397e+27, 2.364e+28, 1.568e+29, 1.402e+29, 2.815e+29, 8.076e+28, 2.856e+28]])
        for a, d in zip(soln.ravel().tolist(), desired.ravel().tolist()):
            np.testing.assert_approx_equal(actual=a, desired=d, significant=3)
