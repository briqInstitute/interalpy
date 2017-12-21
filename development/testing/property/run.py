#!/usr/bin/env python
"""This module is the first attempt to start some regression tests."""
from interalpy.tests.test_auxiliary import get_random_init
from interalpy import simulate
from interalpy import estimate

import numpy as np

np.random.seed(1423)
while True:
    get_random_init()
    simulate('test.interalpy.ini')
    estimate('test.interalpy.ini')

    import os
    os.system('git clean -d -f')