#!/usr/bin/env python
"""This module is the first attempt to set up some reliability testing."""
from interalpy import simulate
from interalpy import estimate
from interalpy.clsModel import ModelCls
from interalpy.tests.test_auxiliary import get_random_init
import os

get_random_init()
#simulate('test.interalpy.ini')
#estimate('test.interalpy.ini')

# count = 0
# while True:
#     print(count)
#     get_random_init()
#
#     simulate('test.interalpy.ini')
#     estimate('test.interalpy.ini')
#
#     count = count + 1
#
#     os.system('git clean -d -f')
