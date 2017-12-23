"""This module contains all the required capabilities to read an initialization file."""
import shlex
import os


def read(fname):
    """This function reads the initialization file."""

    # Check input
    assert os.path.exists(fname)

    # Initialization
    dict_, group = {}, None

    with open(fname) as in_file:

        for line in in_file.readlines():

            list_ = shlex.split(line)

            # Determine special cases
            is_empty, is_group, is_comment = _process_cases(list_)

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
            value = _type_conversions(flag, value)

            # Process blocks of information
            dict_[group][flag] = value

    return dict_


def _process_cases(list_):
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


def _type_conversions(flag, value):
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

