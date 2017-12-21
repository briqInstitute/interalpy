#!/usr/bin/env python
"""This module is the first attempt to start some regression tests."""
import argparse
import json
import os

import numpy as np

from interalpy.auxiliary.auxiliary import dist_class_attributes, criterion_function
from interalpy.tests.test_auxiliary import get_random_init
from interalpy.auxiliary.auxiliary import print_init_dict
from interalpy.config_interalpy import TEST_RESOURCES_DIR
from interalpy import simulate
from interalpy import ModelCls


def create_regression_vault(num_tests):
    """This function creates a set of regression tests."""
    np.random.seed(123)

    tests = []
    for _ in range(num_tests):

        # Create and process initialization file
        init_dict = get_random_init()
        model_obj = ModelCls('test.interalpy.ini')

        # Distribute class attributes for further processing.
        r, eta, nu, b = dist_class_attributes(model_obj, 'r', 'eta', 'nu', 'b')
        df = simulate('test.interalpy.ini')

        crit_val = criterion_function(df, b, r, eta, nu)
        tests += [(init_dict, crit_val)]

    json.dump(tests, open('regression_vault.interalpy.json', 'w'))


def check_regression_vault(num_tests):
    """This function checks an existing regression tests."""
    fname = TEST_RESOURCES_DIR + '/regression_vault.interalpy.json'
    tests = json.load(open(fname, 'r'))

    for test in tests[:num_tests]:

        # Create and process initialization file
        init_dict, crit_val = test
        print_init_dict(init_dict)
        model_obj = ModelCls('test.interalpy.ini')

        # Distribute class attributes for further processing.
        r, eta, nu, b = dist_class_attributes(model_obj, 'r', 'eta', 'nu', 'b')
        df = simulate('test.interalpy.ini')

        np.testing.assert_almost_equal(criterion_function(df, b, r, eta, nu), crit_val)

        os.system('git clean -d -f')


def run(args):
    """Create or check the regression tests."""
    # Distribute arguments
    num_tests = args.num_tests
    request = args.request

    # Check input
    assert num_tests > 0

    if request in ['check']:
        check_regression_vault(num_tests)
    elif request in ['create']:
        create_regression_vault(num_tests)
    else:
        raise AssertionError


if __name__ == '__main__':

    parser = argparse.ArgumentParser('Work with regression tests.')

    parser.add_argument('--request', action='store', dest='request', help='task to perform',
                        required=True, choices=['check', 'create'])

    parser.add_argument('--tests', action='store', dest='num_tests', required=True, type=int,
                        help='number of tests')

    run(parser.parse_args())
