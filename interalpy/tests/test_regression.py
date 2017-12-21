"""This module contains some integration tests."""
import json

import numpy as np

from interalpy.auxiliary.auxiliary import dist_class_attributes, criterion_function
from interalpy.auxiliary.auxiliary import print_init_dict
from interalpy.config_interalpy import TEST_RESOURCES_DIR
from interalpy import simulate
from interalpy import ModelCls


def test_1():
    """This test simply runs a small sample of the regression test battery."""
    with open(TEST_RESOURCES_DIR + '/regression_vault.interalpy.json', 'r') as infile:
        tests = json.load(infile)

    for test in tests[:5]:
        # Create and process initialization file
        init_dict, crit_val = test
        print_init_dict(init_dict)
        model_obj = ModelCls('test.interalpy.ini')

        # Distribute class attributes for further processing.
        r, eta, nu, b = dist_class_attributes(model_obj, 'r', 'eta', 'nu', 'b')
        df = simulate('test.interalpy.ini')

        np.testing.assert_almost_equal(criterion_function(df, b, r, eta, nu), crit_val)
