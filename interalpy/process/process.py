"""This module contains all capabilites related to the processing of observed datasets."""
import os

import pandas as pd

from interalpy.process.process_auxiliary import test_integrity
from interalpy.custom_exceptions import InteralpyError


def process(est_file, est_agents):
    """This function processes the observed dataset."""
    # We read in the estimation dataset.
    if not os.path.exists(est_file):
        raise InteralpyError('estimation dataset does not exist')

    df = pd.read_pickle(est_file)

    test_integrity(df, est_agents)

    # We might want to estimate on a subset of individuals only.
    subset = df['Participant.code'].unique()[:est_agents]
    df = df.loc[(subset, slice(None), slice(None)), :]

    with open('est.interalpy.log', 'w') as outfile:
        outfile.write('\n ESTIMATION SETUP\n')

        fmt_ = '\n Agents {:>14}\n'
        outfile.write(fmt_.format(est_agents))

    return df
