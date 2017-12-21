"""This module contains auxiliary functions that are onlz related to the simulation of the model."""
import numpy as np


def sample_choice(row):
    """This function samples the choice for each row."""
    probs = [row['prob_a'], row['prob_b']]
    row['D'] = np.random.choice([True, False], p=probs)
    return row
