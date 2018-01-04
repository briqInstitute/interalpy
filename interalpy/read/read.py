"""This module contains all the required capabilities to read an initialization file."""
import shlex
import os

import numpy as np

from interalpy.config_interalpy import DEFAULT_BOUNDS


def read(fname):
    """This function reads the initialization file."""
    # Check input
    np.testing.assert_equal(os.path.exists(fname), True)

    # Initialization
    dict_, group = {}, None

    with open(fname) as in_file:

        for line in in_file.readlines():

            list_ = shlex.split(line)

            # Determine special cases
            is_empty, is_group, is_comment = process_cases(list_)

            # Applicability
            if is_empty or is_comment:
                continue

            # Prepare dictionary
            if is_group:
                group = list_[0]
                dict_[group] = {}
                continue

            flag, value = list_[:2]

            # Type conversions
            value = type_conversions(flag, value)

            # We need to allow for additional information about the potential estimation
            # parameters.
            if flag in ['r', 'eta', 'b', 'nu']:
                dict_[group][flag] = process_coefficient_line(list_, value)
            else:
                dict_[group][flag] = value

    return dict_


def process_coefficient_line(list_, value):
    """This function processes a coefficient line and extracts the relevant information. We also
    impose the default values for the bounds here."""
    def process_bounds(bounds):
        """This function extracts the proper bounds."""
        bounds = bounds.replace(')', '')
        bounds = bounds.replace('(', '')
        bounds = bounds.split(',')
        for i in range(2):
            if bounds[i] == 'None':
                bounds[i] = DEFAULT_BOUNDS[label][i]
            else:
                bounds[i] = float(bounds[i])

        return bounds

    label = list_[0]

    if len(list_) == 2:
        is_fixed, bounds = False, DEFAULT_BOUNDS[label]
    elif len(list_) == 4:
        is_fixed = True
        bounds = process_bounds(list_[3])
    elif len(list_) == 3:
        is_fixed = (list_[2] == '!')

        if not is_fixed:
            bounds = process_bounds(list_[2])
        else:
            bounds = DEFAULT_BOUNDS[label]

    return value, is_fixed, bounds


def process_cases(list_):
    """Process cases and determine whether group flag or empty line."""
    # Get information
    is_empty = (len(list_) == 0)

    if not is_empty:
        is_group = list_[0].isupper()
        is_comment = list_[0] == '#'
    else:
        is_group = False
        is_comment = False

    # Finishing
    return is_empty, is_group, is_comment


def type_conversions(flag, value):
    """ Type conversions
    """
    # Type conversion
    if flag in ['seed', 'agents', 'maxfun']:
        value = int(value)
    elif flag in ['file', 'optimizer']:
        value = str(value)
    elif flag in ['detailed']:
        assert (value.upper() in ['TRUE', 'FALSE'])
        value = (value.upper() == 'TRUE')
    elif flag in []:
        value = value.upper()
    else:
        value = float(value)

    # Finishing
    return value

