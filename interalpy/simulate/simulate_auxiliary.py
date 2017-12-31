"""This module contains auxiliary functions that are onlz related to the simulation of the model."""
import numpy as np
import pandas as pd

from interalpy.shared.shared_auxiliary import criterion_function


def sample_choice(row):
    """This function samples the choice for each row."""
    row['D'] = np.random.choice([1, 0], p=[row['prob_a'], row['prob_b']])
    return row


def write_info(df, sim_file, sim_seed, b, r, eta, nu):
    """This function writes some basic information to file to ease inspection of dataset
    properties."""

    with open(sim_file + '.interalpy.info', 'w') as outfile:
        fmt_ = '\n {:<25}{:>20}\n'
        stat = df['Participant.code'].nunique()
        outfile.write(fmt_.format(*[' Number of Individuals', stat]))

        stat = '{:10.5f}'.format(criterion_function(df, r, eta, b, nu))
        outfile.write(fmt_.format(*[' Criterion Function', stat]))

        outfile.write(fmt_.format(*[' Seed', sim_seed]))

        string = '\n\n\n {:>15}{:>15}{:>15}{:>15}\n'
        outfile.write(string.format(*['Question', 'm', 'Share A', 'Share B']))

        for question in sorted(df['Question'].unique()):
            outfile.write('\n')
            for m in sorted(df['m'].loc[:, question, :].unique()):
                stat = df['D'].loc[:, question, m].mean()

                line = [question, m, stat, (1 - stat)]

                string = ' {:>15}{:>15}{:>15.5f}{:>15.5f}\n'
                outfile.write(string.format(*line))

        outfile.write('\n')

        outfile.write(fmt_.format(*[' Parameterization', '']))
        fmt_ = '\n {:>15}{:>15}\n'

        outfile.write(fmt_.format(*['Identifier', 'Value']))
        outfile.write('\n')

        for i, val in enumerate([r, eta, b, nu]):
            string = ' {:>15}{:>15.5f}\n'
            outfile.write(string.format(*[i, val]))


def format_float(x):
    """This function ensures the pretty formatting of floats."""
    if pd.isnull(x):
        return '    .'
    else:
        return '{0:10.2f}'.format(x)


def format_integer(x):
    """This function ensures the pretty formatting of integers."""
    if pd.isnull(x):
        return '    .'
    else:
        return '{0:<5}'.format(int(x))