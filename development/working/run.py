#!/usr/bin/env python
"""This module is the first attempt to set up some reliability testing."""
import os

import numpy as np

from interalpy.tests.test_auxiliary import get_random_init
from interalpy import simulate
from interalpy import estimate

np.random.seed(123)


get_random_init()

count = 0
while False:
    print(count)
    get_random_init()

    simulate('test.interalpy.ini')
    estimate('test.interalpy.ini')

    count = count + 1

    os.system('git clean -d -f')
