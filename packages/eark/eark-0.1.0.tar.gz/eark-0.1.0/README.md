# Emulating Astronautical Reactor Kinetics
The `eark` module is a compilation of utilities for analyzing reactor kinetics, with
a bias towards astronautical engineering applications.

[![Build Status](https://travis-ci.com/vigneshwar-manickam/eark.svg?branch=master)](https://travis-ci.com/vigneshwar-manickam/eark) 

## Installation
The `eark` package is pip-installable and is tested against python 3.6 and 3.7.

```bash
pip install eark
```  

## Using `eark`

### Inhour Equation Solver
The `eark.inhour` module contains utilities for solving the Inhour equations, for example:
```python
>>> import numpy as np
>>> from eark import inhour

# Setup initial state
>>> beta = 0.0075
>>> beta_vector = np.array([0.033, 0.219, 0.196, 0.395, 0.115, 0.042])
>>> n_initial = 4000
>>> period = 6.0e-5
>>> precursor_constants = np.array([0.0124, 0.0305, 0.1110, 0.3011, 1.1400, 3.0100])
>>> precursor_density = np.array([5000, 6000, 5600, 4700, 7800, 6578])
>>> rho =  0.5 * beta

# Solve 
>>> inhour.solve(n_initial=n_initial,
                 precursor_density_initial=precursor_density,
                 beta_vector=beta_vector,
                 precursor_constants=precursor_constants,
                 rho=rho,
                 total_beta=beta,
                 period=period,
                 t_max=1,
                 num_iters=3)

[[4.000e+03, 5.000e+03, 6.000e+03, 5.600e+03, 4.700e+03, 7.800e+03, 6.578e+03],
 [1.881e+15, 1.856e+16, 1.231e+17, 1.100e+17, 2.210e+17, 6.338e+16, 2.241e+16],
 [2.397e+27, 2.364e+28, 1.568e+29, 1.402e+29, 2.815e+29, 8.076e+28, 2.856e+28]]
```

### Running the test suite
The simplest usage of `eark` is to run the test suite. This can ensure the installation was successful.
```python
>>> import eark
>>> eark.test()
```
