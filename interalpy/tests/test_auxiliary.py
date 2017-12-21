"""This module contains auxiliary functions for the test runs."""
import numpy as np

from interalpy.auxiliary.auxiliary import get_random_string
from interalpy.auxiliary.auxiliary import print_init_dict


def get_random_init(fname='test.interalpy.ini'):
    """This function prints a random dictionary."""
    init_dict = random_dict()
    print_init_dict(init_dict, fname)
    return init_dict


def random_dict():
    """This function creates a random initialization file."""

    dict_ = dict()

    # Initial setup to ensure constraints across options.
    sim_agents = np.random.randint(2, 10)
    fname = get_random_string()

    # We start with sampling all preference parameters.
    dict_['PREFERENCES'] = dict()
    dict_['PREFERENCES']['eta'] = np.random.uniform(low=-0.99, high=0.99)
    dict_['PREFERENCES']['r'] = np.random.uniform(low=-0.99, high=0.99)
    dict_['PREFERENCES']['b'] = np.random.lognormal()

    # We now turn to all simulation details.
    dict_['SIMULATION'] = dict()
    dict_['SIMULATION']['agents'] = sim_agents
    dict_['SIMULATION']['seed'] = np.random.randint(1, 1000)
    dict_['SIMULATION']['file'] = fname

    # We sample the parameters for the Luce (1959) model.
    dict_['LUCE'] = dict()
    dict_['LUCE']['nu'] = np.random.lognormal()

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

    return dict_
