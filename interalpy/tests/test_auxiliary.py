"""This module contains auxiliary functions for the test runs."""
import linecache
import shlex

import numpy as np

from interalpy.shared.shared_auxiliary import get_random_string
from interalpy.shared.shared_auxiliary import print_init_dict


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

    # We start with sampling all preference parameters.
    dict_['PREFERENCES'] = dict()
    dict_['PREFERENCES']['eta'] = np.random.uniform(low=-0.98, high=0.98)
    dict_['PREFERENCES']['r'] = np.random.uniform(low=-0.98, high=0.98)
    dict_['PREFERENCES']['b'] = np.random.lognormal()

    # We now turn to all simulation details.
    dict_['SIMULATION'] = dict()
    dict_['SIMULATION']['agents'] = sim_agents
    dict_['SIMULATION']['seed'] = np.random.randint(1, 1000)
    dict_['SIMULATION']['file'] = fname

    # We sample the parameters for the Luce (1959) model.
    dict_['LUCE'] = dict()
    dict_['LUCE']['nu'] = np.random.uniform(low=0.01, high=4.99)

    # We sample valid estimation requests.
    dict_['ESTIMATION'] = dict()
    dict_['ESTIMATION']['agents'] = np.random.randint(1, sim_agents)
    dict_['ESTIMATION']['maxfun'] = np.random.randint(1, 10)
    dict_['ESTIMATION']['file'] = fname + '.interalpy.pkl'
    dict_['ESTIMATION']['optimizer'] = np.random.choice(['SCIPY-BFGS', 'SCIPY-POWELL'])

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

    return dict_


def get_rmse():
    """This function returns the RMSE from the information file."""
    stat = float(shlex.split(linecache.getline('compare.interalpy.info', 7))[2])
    return stat
