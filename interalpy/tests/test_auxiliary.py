"""This module contains auxiliary functions for the test runs."""
import linecache
import shlex

import numpy as np

from interalpy.shared.shared_auxiliary import get_random_string
from interalpy.shared.shared_auxiliary import print_init_dict
from interalpy.config_interalpy import HUGE_FLOAT
from interalpy.config_interalpy import NUM_PARAS
from interalpy.config_interalpy import BOUNDS


def get_random_init(constr=dict()):
    """This function prints a random dictionary."""
    init_dict = random_dict(constr)
    print_init_dict(init_dict, 'test.interalpy.ini')
    return init_dict


def random_dict(constr):
    """This function creates a random initialization file."""

    dict_ = dict()

    # Initial setup to ensure constraints across options.
    sim_agents = np.random.randint(2, 10)
    fname = get_random_string()
    is_fixed = np.random.choice([True, False], size=NUM_PARAS)

    # We start with sampling all preference parameters.
    dict_['PREFERENCES'] = dict()

    for label in ['r', 'eta', 'b']:
        lower, upper = BOUNDS[label]
        # We need to deal with the special case when there are no bounds defined.
        lower, upper = max(-HUGE_FLOAT, lower), min(HUGE_FLOAT, upper)
        is_fixed = np.random.choice([True, False])
        value = np.random.uniform(low=lower, high=upper)

        dict_['PREFERENCES'][label] = (value, is_fixed)

    # We sample the parameters for the Luce (1959) model.
    dict_['LUCE'] = dict()

    lower, upper = BOUNDS['nu']
    lower, upper = max(-HUGE_FLOAT, lower), min(HUGE_FLOAT, upper)
    is_fixed = np.random.choice([True, False])
    value = np.random.uniform(low=lower, high=upper)

    dict_['LUCE']['nu'] = (value, is_fixed)

    # We now turn to all simulation details.
    dict_['SIMULATION'] = dict()
    dict_['SIMULATION']['agents'] = sim_agents
    dict_['SIMULATION']['seed'] = np.random.randint(1, 1000)
    dict_['SIMULATION']['file'] = fname

    # We sample valid estimation requests.
    dict_['ESTIMATION'] = dict()
    dict_['ESTIMATION']['optimizer'] = np.random.choice(['SCIPY-BFGS', 'SCIPY-POWELL'])
    dict_['ESTIMATION']['detailed'] = np.random.choice(['True', 'False'])
    dict_['ESTIMATION']['agents'] = np.random.randint(1, sim_agents)
    dict_['ESTIMATION']['maxfun'] = np.random.randint(1, 10)
    dict_['ESTIMATION']['file'] = fname + '.interalpy.pkl'

    # We sample optimizer options.
    dict_['SCIPY-BFGS'] = dict()
    dict_['SCIPY-BFGS']['gtol'] = np.random.lognormal()
    dict_['SCIPY-BFGS']['eps'] = np.random.lognormal()

    dict_['SCIPY-POWELL'] = dict()
    dict_['SCIPY-POWELL']['xtol'] = np.random.lognormal()
    dict_['SCIPY-POWELL']['ftol'] = np.random.lognormal()

    # Now we need to impose possible constraints.
    if constr is not None:
        if 'maxfun' in constr.keys():
            dict_['ESTIMATION']['maxfun'] = constr['maxfun']

        if 'num_agents' in constr.keys():
            dict_['SIMULATION']['agents'] = constr['num_agents']
            dict_['ESTIMATION']['agents'] = constr['num_agents']

        if 'est_file' in constr.keys():
            dict_['ESTIMATION']['file'] = constr['est_file']

        if 'detailed' in constr.keys():
            dict_['ESTIMATION']['detailed'] = constr['detailed']

    return dict_


def get_rmse():
    """This function returns the RMSE from the information file."""
    stat = float(shlex.split(linecache.getline('compare.interalpy.info', 7))[2])
    return stat
