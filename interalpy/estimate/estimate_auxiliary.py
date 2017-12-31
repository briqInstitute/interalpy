"""This module contains auxiliary functions that are only relevant for the estimation process."""
import shutil
import copy
import os

from statsmodels.tools import eval_measures
import pandas as pd
import numpy as np

from interalpy.shared.shared_auxiliary import dist_class_attributes
from interalpy.config_interalpy import HUGE_FLOAT
from interalpy.simulate.simulate import simulate


def estimate_cleanup():
    """This function ensures that we start the estimation with a clean slate."""
    # We remove the directories that contain the simulated choice menus at the start.
    for dirname in ['start', 'stop']:
        if os.path.exists(dirname):
            shutil.rmtree(dirname)

    # We remove the information from earlier estimation runs.
    for fname in ['est.interalpy.info', 'est.interalpy.log']:
        if os.path.exists(fname):
            os.remove(fname)


def estimate_simulate(which, points, model_obj, df_obs):
    """This function allows to easily simulate samples at the beginning and the end of the
    estimation."""
    sim_agents = dist_class_attributes(model_obj, 'sim_agents')

    os.mkdir(which)
    os.chdir(which)

    sim_model = copy.deepcopy(model_obj)
    sim_model.attr['sim_file'] = which

    sim_model.update('optim', 'free', points)
    sim_model.write_out(which + '.interalpy.ini')
    simulate(which + '.interalpy.ini')

    compare_datasets(which, df_obs, sim_agents)

    os.chdir('../')


def compare_datasets(which, df, sim_agents):
    """This function compares the estimation dataset with a simulated dataset using the estimated
    parameter vector."""
    df_stop = pd.read_pickle(which + '.interalpy.pkl')

    stats = []
    for question in sorted(df['Question'].unique()):
        for m in sorted(df['m'].loc[:, question, :].unique()):
            stat = []
            stat += [df['D'].loc[:, question, m].mean()]
            stat += [df_stop['D'].loc[:, question, m].mean()]
            stats += [stat]

    stats = np.array(stats)

    with open('compare.interalpy.info', 'w') as outfile:
        outfile.write('\n')

        fmt_ = '\n {:<25}{:>20}\n'
        stat = df['Participant.code'].nunique()
        outfile.write(fmt_.format(*['Observed Individuals', stat]))
        outfile.write(fmt_.format(*['Simulated Individuals', sim_agents]))

        fmt_ = '\n {:<25}{:>20.4f}\n'
        stat = eval_measures.rmse(stats[:, 0], stats[:, 1])
        outfile.write(fmt_.format(*['Root-Mean-Square Error', stat]))

        string = '\n\n\n {:>15}{:>15}{:>15}{:>15}{:>15}\n'
        outfile.write(string.format(*['Question', 'm', 'Data', 'Simulation', 'Difference']))

        stats = stats.tolist()

        count = 0
        for question in sorted(df['Question'].unique()):
            outfile.write('\n')
            for m in sorted(df['m'].loc[:, question, :].unique()):
                stat = stats[count]
                string = ' {:>15d}{:>15}{:>15.4f}{:>15.4f}{:>15.4f}\n'
                line = [question, m] + stat + [abs(stat[0] - stat[1])]
                outfile.write(string.format(*line))
                count += 1


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


