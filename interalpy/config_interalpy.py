"""This module contains some configuration information."""
import os

import numpy as np

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_RESOURCES_DIR = PACKAGE_DIR + '/tests/material'

HUGE_FLOAT = 10e+20
TINY_FLOAT = 10e-25

# We are strict in enforcing data types throughout.
DATA_DTYPES = dict()
DATA_DTYPES.update({'Participant.code': str, 'Question': np.int, 'x': np.float,  'y': np.float})
DATA_DTYPES.update({'I1': np.float, 'I2': np.float, 'm': np.float, 'D': np.int})

# We want to be strict about any problems due to floating-point errors.
np.seterr(all='raise')

# We need to impose some bounds on selected estimation parameters. The bounds are included in the
#  package's admissible values.
BOUNDS = dict()
BOUNDS['eta'] = (-0.99, 0.99)
BOUNDS['b'] = (0.01, np.inf)
BOUNDS['r'] = (-0.99, 0.99)
BOUNDS['nu'] = (0.01, 5.00)
