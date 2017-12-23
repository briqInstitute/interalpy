"""This module contains some configuration information."""
import os

import numpy as np

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_RESOURCES_DIR = PACKAGE_DIR + '/tests/material'

HUGE_FLOAT = 10e+20
TINY_FLOAT = 10e-15

# We are strict in enforcing data types throughout.
DATA_DTYPES = dict()
DATA_DTYPES.update({'Participant.code': str, 'Question': np.int, 'x': np.float,  'y': np.float})
DATA_DTYPES.update({'I1': np.float, 'I2': np.float, 'm': np.float, 'D': np.int})

# TODO: I need to settle on a specification here.
# We want to be strict about any problems due to floating-point errors.
# np.seterr(all='raise')