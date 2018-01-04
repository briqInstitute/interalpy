"""This module contains some integration tests."""
import json

import numpy as np

from interalpy.shared.shared_auxiliary import dist_class_attributes
from interalpy.shared.shared_auxiliary import criterion_function
from interalpy.shared.shared_auxiliary import print_init_dict
from interalpy.config_interalpy import TEST_RESOURCES_DIR
from interalpy.config_interalpy import DEFAULT_BOUNDS
from interalpy import simulate
from interalpy import ModelCls


def run_regression_test(test):
    """This function runs a single regression test. It is repeatedly used by the testing
    infrastructure. Thus, manual modifications are only required here."""
    # Create and process initialization file
    init_dict, crit_val = test

    print_init_dict(init_dict)
    model_obj = ModelCls('test.interalpy.ini')

    # Distribute class attributes for further processing.
    paras_obj = dist_class_attributes(model_obj, 'paras_obj')
    r, eta, b, nu = paras_obj.get_values('econ', 'all')

    df = simulate('test.interalpy.ini')

    np.testing.assert_almost_equal(criterion_function(df, r, eta, b, nu), crit_val)


def test_1():
    """This test simply runs a small sample of the regression test battery."""
    with open(TEST_RESOURCES_DIR + '/regression_vault.interalpy.json', 'r') as infile:
        tests = json.load(infile)

    for test in tests[:5]:
        run_regression_test(test)
