"""This module contains some auxiliary functions for the structural estimations in the
intertemporal altruism project."""
import functools
import string
import copy

import pandas as pd
import numpy as np

from interalpy.config_interalpy import PACKAGE_DIR
from interalpy.logging.clsLogger import logger_obj
from interalpy.config_interalpy import HUGE_FLOAT
from interalpy.config_interalpy import TINY_FLOAT


def solve_grid(r, eta, b, nu):
    """This function solves the grid of the model that is relevant for all individuals in the
    dataset."""
    # Since all individuals are equivalent, we can  simply restrict attention to the choices
    # in the from of a grid.
    grid = pd.read_pickle(PACKAGE_DIR + '/material/grid.interalpy.pkl')

    # We now calculate the expected utilities for each choice for the given parameterization of
    # the model.
    construct_expected_utilities_row = functools.partial(construct_expected_utilities, r, eta, b)
    grid = grid.apply(construct_expected_utilities_row, axis=1)

    # We are ready to construct the choice probabilites based on Luce's (1959) model.
    construct_choice_probabilities_row = functools.partial(construct_choice_probabilities, nu)
    grid = grid.apply(construct_choice_probabilities_row, axis=1)

    # We restrict attention to only a subset of information.
    grid.set_index(['Question', 'm'], inplace=True, drop=False)
    grid = grid[['Question', 'm', 'prob_a', 'prob_b', 'eu_a', 'eu_b']]

    return grid


def dist_class_attributes(model_obj, *args):
    """ This function distributes a host of class attributes.
    """
    # Initialize container
    ret = []

    # Process requests
    for arg in args:
        ret.append(model_obj.get_attr(arg))

    # There is some special handling for the case where only one element is returned.
    if len(ret) == 1:
        ret = ret[0]

    # Finishing
    return ret


def atemporal_utility(payments, r, eta, b):
    """This function calculates the atemporal utility."""
    own, charity = payments
    u = (own ** (1 - r) / (1 - r)) + b * (charity ** (1 - r) / (1 - r))
    return (u ** (1 - eta)) / (1 - eta)


def luce_prob(u_x, u_y, nu):
    """This function computes the choice probabilites using Luce's model."""
    try:
        x = u_x ** (1 / nu)
    except (OverflowError, FloatingPointError) as _:
        logger_obj.record_event(0)
        x = HUGE_FLOAT
    try:
        y = u_y ** (1 / nu)
    except (OverflowError, FloatingPointError) as _:
        logger_obj.record_event(0)
        y = HUGE_FLOAT

    prob = x / (x + y)
    return prob, 1 - prob


def construct_choice_probabilities(nu, row):
    """This function returns the expected utility from both lotteries."""
    row['prob_a'], row['prob_b'] = np.nan, np.nan
    row[['prob_a', 'prob_b']] = luce_prob(row['eu_a'], row['eu_b'], nu)
    return row


def construct_expected_utilities(r, eta, b, row):
    """This function returns the expected utility from both lotteries."""
    if row['Question'] in [1, 2, 3]:
        eu_a = 0

        payments = (row['x'] + row['I1'], row['y'])
        eu_a += 0.5 * atemporal_utility(payments, r, eta, b)

        payments = (row['x'] + row['I2'], row['y'])
        eu_a += 0.5 * atemporal_utility(payments, r, eta, b)

        eu_b = 0

        payments = (row['x'] + row['I1'] + row['I2'] + row['m'], row['y'])
        eu_b += 0.5 * atemporal_utility(payments, r, eta, b)

        payments = (row['x'] + row['m'], row['y'])
        eu_b += 0.5 * atemporal_utility(payments, r, eta, b)

    elif row['Question'] in [4, 5, 6]:

        eu_a = 0

        payments = (row['x'], row['y'] + row['I1'])
        eu_a += 0.5 * atemporal_utility(payments, r, eta, b)

        payments = (row['x'], row['y'] + row['I2'])
        eu_a += 0.5 * atemporal_utility(payments, r, eta, b)

        eu_b = 0

        payments = (row['x'], row['y'] + row['I1'] + row['I2'] + row['m'])
        eu_b += 0.5 * atemporal_utility(payments, r, eta, b)

        payments = (row['x'], row['y'] + row['m'])
        eu_b += 0.5 * atemporal_utility(payments, r, eta, b)

    elif row['Question'] in [7, 8, 9]:

        eu_a = 0

        payments = (row['x'] + row['I1'], row['y'])
        eu_a += 0.5 * atemporal_utility(payments, r, eta, b)

        payments = (row['x'], row['y'] + row['I2'])
        eu_a += 0.5 * atemporal_utility(payments, r, eta, b)

        eu_b = 0

        payments = (row['x'] + row['I1'] + row['m'], row['y'] + row['I2'])
        eu_b += 0.5 * atemporal_utility(payments, r, eta, b)

        payments = (row['x'] + row['m'], row['y'])
        eu_b += 0.5 * atemporal_utility(payments, r, eta, b)

    else:
        raise AssertionError

    row['eu_a'], row['eu_b'] = eu_a, eu_b

    return row


def get_random_string(size=6):
    """This function samples a random string of varying size."""
    chars = list(string.ascii_lowercase)
    str_ = ''.join(np.random.choice(chars) for x in range(size))
    return str_


def print_init_dict(dict_, fname='test.interalpy.ini'):
    """This function prints an initialization dictionary."""
    keys = ['PREFERENCES', 'LUCE', 'SIMULATION', 'ESTIMATION', 'SCIPY-BFGS', 'SCIPY-POWELL']

    with open(fname, 'w') as outfile:
        for key_ in keys:
            outfile.write(key_ + '\n\n')
            for label in sorted(dict_[key_].keys()):
                info = dict_[key_][label]

                str_ = '{:<10}'
                if label in ['ftol', 'gtol', 'eps', 'xtol']:
                    str_ += ' {:25.4f}\n'

                elif label in ['r', 'eta', 'b', 'nu']:
                    str_ += ' {:25.4f} {:>5} '
                else:
                    str_ += ' {:>25}\n'

                if label in ['detailed']:
                    info = str(info)

                if label in ['r', 'eta', 'b', 'nu']:
                    line, str_ = format_coefficient_line(label, info, str_)
                else:
                    line = [label, info]

                outfile.write(str_.format(*line))

            outfile.write('\n')


def format_coefficient_line(label, info, str_):
    """This function returns a properly formatted coefficient line."""
    value, is_fixed, bounds = info

    # We need to make sure this is an independent copy as otherwise the bound in the original
    # dictionary are overwritten with the value None.
    bounds = copy.deepcopy(bounds)

    line = []
    line += [label, value]

    if is_fixed == 'True':
        line += ['!']
    else:
        line += ['']

    # Bounds might be printed or now.
    for i in range(2):
        value = bounds[i]
        if abs(value) > HUGE_FLOAT:
            bounds[i] = None
        else:
            bounds[i] = np.round(value, decimals=4)

    if bounds.count(None) == 2:
        bounds = ['', '']
        str_ += '{:}\n'
    else:
        str_ += '({:},{:})\n'

    line += bounds

    return line, str_


def criterion_function(df, r, eta, b, nu):
    """This function evaluates the value of the criterion function for a given parameterization
    of the model."""
    # We need to ensure that only information from an observed dataset is included.
    df_est = df.copy(deep=True)
    df_est = df_est[['Participant.code', 'Question', 'm', 'D']]

    # We start by simply solving for the alternative-specific choice probabilities.
    grid = solve_grid(r, eta, b, nu)

    # We can now simply merge the alternative specific-choice probabilities and select the relevant
    # value for the likelihood evaluation.
    df_est = pd.merge(df_est, grid, right_on=['Question', 'm'], left_on=['Question', 'm'])

    df_est['prob'] = df_est['D'] * df_est['prob_a'] + (1 - df_est['D']) * df_est['prob_b']
    fval = -np.mean(np.log(np.clip(df_est['prob'], TINY_FLOAT, np.inf)))

    np.testing.assert_equal(np.isfinite(fval), True)

    return fval


def char_floats(floats):
    """This method ensures a pretty printing of all floats."""
    # We ensure that this function can also be called on for a single float value.
    if isinstance(floats, float):
        floats = [floats]

    line = []
    for value in floats:
        if abs(value) > HUGE_FLOAT:
            line += ['{:>25}'.format('---')]
        else:
            line += ['{:25.15f}'.format(value)]

    return line
