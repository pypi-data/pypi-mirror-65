"""Solving the Inhour equation, coupled differential equations representing neutron populations in reactor

[Vignesh can clean this up]

References:
    [1] Inhour Equation https://en.wikipedia.org/wiki/Inhour_equation
"""

import functools

import numpy as np
from scipy.integrate import odeint


def total_neutron_deriv(rho: float, beta: float, period: float, n, precursor_constants: np.ndarray, precursor_density: np.ndarray) -> float:
    """Compute time derivative of total neutron population, $\frac{dn}{dt}(t)$

    Args:
        rho:
            float, neutron density [UNITS?]
        beta:
            float, ??
        period:
            float, reactor period [UNITS?]
        n:
            float, neutron population count
        precursor_constants:
            ndarray, 1x6 array of lambda_i
        precursor_density:
            ndarray, 1x6 array of c_i

    Returns:
        float, the time derivative of total neutron population

        Examples:
            Computing a sample time derivative
            >>> total_neutron_deriv(rho=0.5*0.0075,
            ...                     beta=0.0075,
            ...                     period=6.0e-05,
            ...                     n=4000,
            ...                     precursor_constants=np.array([0.0124, 0.0305, 0.1110, 0.3011, 1.1400, 3.0100]),
            ...                     precursor_density=np.array([5000, 6000, 5600, 4700, 7800, 6578]))
            -219026.44999999998
    """
    return (((rho - beta) / period) * n) + np.inner(precursor_constants, precursor_density)


def delay_neutron_deriv(beta_vector: np.ndarray, period: float, n: float, precursor_constants: np.ndarray, precursor_density: np.ndarray) -> np.ndarray:
    """Compute time derivative of delayed neutron population, $\frac{dc_i}{dt}(t)$

    Args:
        beta_vector:
            ndarray, 1x6 vector of fraction of delayed neutrons of ith kind
        period:
            float, reactor period [UNITS?]
        n:
            float, neutron population count
        precursor_constants:
            ndarray, 1x6 array of lambda_i
        precursor_density:
            ndarray, 1x6 array of c_i

    Returns:
        ndarray 1x6 vector of the time derivative of each of the "i" components of precursor density

        Examples:
            Computing delayed neutron population vector derivative
            >>> delay_neutron_deriv(beta_vector=np.array([0.033, 0.219, 0.196, 0.395, 0.115, 0.042]),
            ...                     period=0.0075,
            ...                     n=4000,
            ...                     precursor_constants=np.array([0.0124, 0.0305, 0.1110, 0.3011, 1.1400, 3.0100]),
            ...                     precursor_density=np.array([5000, 6000, 5600, 4700, 7800, 6578]))
            array([ 17538.        , 116617.        , 103911.73333333, 209251.49666667,
                    52441.33333333,   2600.22      ])
    """
    return beta_vector * n / period - precursor_constants * precursor_density


def _state_deriv(state: np.ndarray, t: float, beta_vector: np.ndarray, precursor_constants: np.ndarray, rho: float, total_beta: float, period: float) -> np.ndarray:
    """Function to compute the time derivative of the reactor state, including the population count and the precursor densities

    Args:
        state:
            ndarray, 1x7 vector where the components represent the state of the reactor at time "t":
                - Component 0 is "n", total neutron population
                - Components 1-6 are "c_i", precursor densities
            These components are concatenated into a single array to conform to the scipy API
        t:
            float, currently unused parameter for scipy odeint interface

    Returns:
        ndarray, the time derivative of the reactor state at time "t"
    """
    dndt = total_neutron_deriv(rho=rho, beta=total_beta, period=period, n=state[0], precursor_constants=precursor_constants, precursor_density=state[1:])
    dcdt = delay_neutron_deriv(beta_vector=beta_vector, period=period, n=state[0], precursor_constants=precursor_constants, precursor_density=state[1:])
    return np.concatenate((np.array([dndt]), dcdt), axis=0)


def solve(n_initial: float, precursor_density_initial: np.ndarray, beta_vector: np.ndarray, precursor_constants: np.ndarray, rho: float, total_beta: float, period: float,
          t_max: float, t_start: float = 0, num_iters: int = 100):
    """Solve the Inhour equations numerically given some initial reactor state

    Args:
        n_initial:
            float, initial population count
        precursor_density_initial:
            ndarray, 1x6 vector of initial precursor densities
        beta_vector:
            ndarray, 1x6 vector of beta_i
        precursor_constants:
            ndarray, 1x6 vector of lambda_i
        rho:
            float, density (presently time independent)
        total_beta:
            float, ??
        period:
            float, reactor period
        t_max:
            float, ending time of simulation
        t_start:
            float, default 0, starting time of simulation
        num_iters:
            int, default 100, number of iterations (@TODO: perhaps refactor these last three arguments in favor of a (delta_t, num_iters) combo?)

    Returns:
        ndarray, state vector evolution 7xnum_iters
    """
    initial_state = np.concatenate((np.array([n_initial]), precursor_density_initial), axis=0)
    t = np.linspace(t_start, t_max, num_iters)
    deriv_func = functools.partial(_state_deriv, beta_vector=beta_vector, precursor_constants=precursor_constants, rho=rho, total_beta=total_beta, period=period)
    return odeint(deriv_func, initial_state, t)
