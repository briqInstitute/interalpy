"""This module contains the capability to simulate the synthetic outcome for a given model
specification."""
import pandas as pd
import numpy as np

from interalpy.simulate.simulate_auxiliary import sample_choice
from interalpy.shared.shared_auxiliary import dist_class_attributes
from interalpy.shared.shared_auxiliary import criterion_function
from interalpy.shared.shared_auxiliary import solve_grid
from interalpy.clsModel import ModelCls


def simulate(fname):
    """This function simulated the model from an initialization file."""
    # Process initialization file
    model_obj = ModelCls(fname)

    # Distribute class attributes for further processing.
    r, eta, nu, b, sim_seed, sim_agents, sim_file = dist_class_attributes(model_obj, 'r', 'eta',
        'nu', 'b', 'sim_seed', 'sim_agents', 'sim_file')

    # Since all individuals are equivalent, we can  simply restrict attention to the choices
    # in the from of a grid.
    grid = solve_grid(r, eta, b, nu)

    np.random.seed(sim_seed)

    df_simulated = []
    for i, _ in enumerate(range(sim_agents)):
        grid_agent = grid.copy(deep=True)
        grid_agent['Participant.code'] = i
        grid_agent = grid_agent.apply(sample_choice, axis=1)
        df_simulated += [grid_agent]

    df_simulated = pd.concat(df_simulated)

    df_simulated['Participant.code'] = df_simulated['Participant.code'].astype(int)
    df_simulated.set_index(['Participant.code', 'Question', 'm'], inplace=True, drop=False)

    columns = ['Participant.code', 'Question', 'm', 'D', 'eu_a', 'eu_b', 'prob_a', 'prob_b']
    df_simulated = df_simulated[columns]

    formats = []
    formats += [_format_integer, _format_integer, _format_float, _format_integer, _format_float]
    formats += [_format_float, _format_float, _format_float]
    with open(sim_file + '.interalpy.txt', 'w') as file_:
        df_simulated.to_string(file_, index=False, header=True, na_rep='.', formatters=formats)

    df_simulated['Question'] = df_simulated['Question'].astype(np.int)
    df_simulated.to_pickle(sim_file + '.interalpy.pkl')

    write_info(df_simulated, sim_file, sim_seed, b, r, eta, nu)

    return df_simulated


def write_info(df, sim_file, sim_seed, b, r, eta, nu):
    """This function writes some basic information to file to ease inspection of dataset
    property."""

    with open(sim_file + '.interalpy.info', 'w') as outfile:
        fmt_ = '\n {:<25}{:>20}\n'
        stat = df['Participant.code'].nunique()
        outfile.write(fmt_.format(*[' Number of Individuals', stat]))

        stat = '{:10.5f}'.format(criterion_function(df, b, r, eta, nu))
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

        for i, val in enumerate([r, eta, nu, b]):
            string = ' {:>15}{:>15.5f}\n'
            outfile.write(string.format(*[i, val]))


def _format_float(x):
    """This function ensures the pretty formatting of floats."""
    if pd.isnull(x):
        return '    .'
    else:
        return '{0:10.2f}'.format(x)


def _format_integer(x):
    """This function ensures the pretty formatting of integers."""
    if pd.isnull(x):
        return '    .'
    else:
        return '{0:<5}'.format(int(x))
