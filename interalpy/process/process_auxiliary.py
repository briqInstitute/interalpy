"""This module contains some auxiliary functions to the processing of the observed dataset."""
import numpy as np


def test_integrity(df, est_agents):
    """This function tests the integrity of the estimation dataset."""
    # Does the number of requested individuals line up with the number available?
    stat = df['Participant.code'].nunique()
    np.testing.assert_equal(stat >= est_agents, True)
