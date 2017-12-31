#!/usr/bin/env python
"""This module is the first attempt to start some regression tests."""
import argparse
import json
import os

import numpy as np

from interalpy.shared.shared_auxiliary import dist_class_attributes
from interalpy.shared.shared_auxiliary import criterion_function
from interalpy.tests.test_regression import run_single_test
from interalpy.tests.test_auxiliary import get_random_init
from interalpy.config_interalpy import TEST_RESOURCES_DIR
from interalpy import simulate
from interalpy import ModelCls


def create_regression_vault(num_tests):
    """This function creates a set of regression tests."""
    np.random.seed(123)

    tests = []
    for _ in range(num_tests):

        print('\n ... creating test ' + str(_))

        # Create and process initialization file
        init_dict = get_random_init()
        model_obj = ModelCls('test.interalpy.ini')

        # Distribute class attributes for further processing.
        paras_obj = dist_class_attributes(model_obj, 'paras_obj')
        r, eta, b, nu = paras_obj.get_values('econ', 'all')

        df = simulate('test.interalpy.ini')
        crit_val = criterion_function(df, r, eta, b, nu)
        tests += [(init_dict, crit_val)]

        os.system('git clean -d -f')

    json.dump(tests, open('regression_vault.interalpy.json', 'w'))


def check_regression_vault(num_tests):
    """This function checks an existing regression tests."""
    fname = TEST_RESOURCES_DIR + '/regression_vault.interalpy.json'
    tests = json.load(open(fname, 'r'))

    for i, test in enumerate(tests[:num_tests]):
        print('... running test ', i)
        run_single_test(test)
        os.system('git clean -d -f > /dev/null')


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
