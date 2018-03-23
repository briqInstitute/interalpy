"""This module contains auxiliary functions for the test runs."""
import linecache
import shlex

import numpy as np

from interalpy.shared.shared_auxiliary import get_random_string
from interalpy.shared.shared_auxiliary import print_init_dict
from interalpy.custom_exceptions import InteralpyError
from interalpy.config_interalpy import NUM_PARAS


def get_random_init(constr=None):
    """This function prints a random dictionary."""
    if constr == None:
        constr=dict()
    init_dict = random_dict(constr)
    print_init_dict(init_dict, 'test.interalpy.ini')
    return init_dict


def random_dict(constr):
    """This function creates a random initialization file."""
    dict_ = dict()

    # Initial setup to ensure constraints across options.
    sim_agents = np.random.randint(2, 10)
    fname = get_random_string()
    is_fixed = np.random.choice(['True', 'False'], size=NUM_PARAS)

    # We need to ensure at least one parameter is free for a valid estimation request.
    if is_fixed.tolist().count('False') == 0:
        is_fixed[0] = 'False'

    bounds = list()
    for label in ['r', 'eta', 'b', 'nu']:
        bounds += [get_bounds(label)]

    values = list()
    for i, label in enumerate(['r', 'eta', 'b', 'nu']):
        values += [get_value(bounds[i])]

    # We want to include the case where the bounds are not specified by the user. In this case
    # the default bounds are relevant.
    probs = [0.2, 0.8]
    for bound in bounds:
        if np.random.choice([True, False], p=probs):
            bound[0] = -np.inf
        if np.random.choice([True, False], p=probs):
            bound[1] = np.inf

    # We start with sampling all preference parameters.
    dict_['PREFERENCES'] = dict()
    for i, label in enumerate(['r', 'eta', 'b']):
        dict_['PREFERENCES'][label] = (values[i], is_fixed[i], bounds[i])

    # We sample the parameters for the Luce (1959) model.
    dict_['LUCE'] = dict()
    dict_['LUCE']['nu'] = (values[3], is_fixed[3], bounds[3])

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


def get_bounds(label):
    """This function returns a set of valid bounds tailored for each parameter."""
    wedge = float(np.random.uniform(0.03, 0.10))

    if label in ['r', 'eta']:
        lower = float(np.random.uniform(-0.98, 0.98 - wedge))
        upper = lower + wedge
    elif label in ['b', 'nu']:
        lower = float(np.random.uniform(0.01, 4.99 - wedge))
        upper = lower + wedge
    else:
        raise InteralpyError('flawed request for bounds')

    bounds = [float(lower), float(upper)]

    return bounds


def get_value(bounds):
    """This function returns a value for the parameter that honors the bounds."""
    lower, upper = bounds
    value = float(np.random.uniform(lower + 0.01, upper - 0.01))
    return value
