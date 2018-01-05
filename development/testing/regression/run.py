#!/usr/bin/env python
"""This module is the first attempt to start some regression tests."""
import json

import numpy as np

from interalpy.shared.shared_auxiliary import dist_class_attributes
from interalpy.shared.shared_auxiliary import criterion_function
from auxiliary_tests import distribute_command_line_arguments
from interalpy.tests.test_regression import run_regression_test
from interalpy.tests.test_auxiliary import get_random_init
from auxiliary_tests import process_command_line_arguments
from interalpy.config_interalpy import TEST_RESOURCES_DIR
from auxiliary_tests import send_notification
from auxiliary_tests import cleanup
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

        cleanup()

    json.dump(tests, open('regression_vault.interalpy.json', 'w'))


def check_regression_vault(num_tests):
    """This function checks an existing regression tests."""
    fname = TEST_RESOURCES_DIR + '/regression_vault.interalpy.json'
    tests = json.load(open(fname, 'r'))

    for i, test in enumerate(tests[:num_tests]):
        try:
            run_regression_test(test)
        except Exception:
            send_notification('regression', is_failed=True, count=i)
            raise SystemError

        cleanup()

    send_notification('regression', is_failed=False, num_tests=num_tests)


def run(args):
    """Create or check the regression tests."""
    args = distribute_command_line_arguments(args)
    if args['is_check']:
        check_regression_vault(args['num_tests'])
    else:
        create_regression_vault(args['num_tests'])


if __name__ == '__main__':

    args = process_command_line_arguments('regression')

    run(args)
