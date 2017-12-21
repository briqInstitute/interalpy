"""This module contains the capability to estimate the model."""
import shutil
import copy
import os

from statsmodels.tools import eval_measures
from scipy.optimize import minimize
import pandas as pd
import numpy as np

from interalpy.auxiliary.auxiliary import dist_class_attributes
from interalpy.estimate.estimate_auxiliary import estimate_simulate
from interalpy.estimate.clsEstimate import EstimateClass
from interalpy.estimate.clsEstimate import to_optimizer
from interalpy.custom_exceptions import InteralpyError
from interalpy.custom_exceptions import MaxfunError
from interalpy.simulate.simulate import simulate
from interalpy.clsModel import ModelCls


def estimate(fname):
    """This function allow to estimate the model."""
    model_obj = ModelCls(fname)

    # Distribute class attributes for further processing.
    est_file, maxfun, optimizer, opt_options, r, eta, b, nu, sim_agents = \
        dist_class_attributes(model_obj, 'est_file', 'maxfun', 'optimizer', 'opt_options', 'r',
        'eta', 'b', 'nu', 'sim_agents')

    # We read in the estimation dataset.
    df = pd.read_pickle(est_file)

    # We simulate a sample at the starting point.
    x_start = to_optimizer([r, eta, nu])
    estimate_simulate('start', x_start, model_obj)

    # We need to initialize the auxiliary classes.
    estimate_obj = EstimateClass(df, b, maxfun)

    # Not all algorithms are using the starting values as the very first evaluation.
    estimate_obj.evaluate(x_start)

    # We are faced with a serious estimation request.
    if maxfun > 1:

        options = dict()

        if optimizer == 'SCIPY-BFGS':
            options['gtol'] = opt_options['SCIPY-BFGS']['gtol']
            options['eps'] = opt_options['SCIPY-BFGS']['eps']
            method = 'BFGS'
        elif optimizer == 'SCIPY-POWELL':
            options['ftol'] = opt_options['SCIPY-POWELL']['ftol']
            options['xtol'] = opt_options['SCIPY-POWELL']['xtol']
            method = 'POWELL'
        else:
            raise InteralpyError('... flawed choice of optimization method')

        try:
            minimize(estimate_obj.evaluate, x_start, method=method, options=options)
        except MaxfunError:
            pass

    # Now we can wrap up all estimation related tasks.
    estimate_obj.finish()

    # We also simulate a sample at the stop of the estimation.
    x_stop = estimate_obj.get_attr('x_step')
    estimate_simulate('stop', x_stop, model_obj)

    df_stop = pd.read_pickle('stop/stop.interalpy.pkl')

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

        for question in sorted(df['Question'].unique()):
            outfile.write('\n')
            for i, m in enumerate(sorted(df['m'].loc[:, question, :].unique())):
                stat = stats[i]
                string = ' {:>15d}{:>15}{:>15.4f}{:>15.4f}{:>15.4f}\n'
                line = [question, m] + stat + [abs(stat[0] - stat[1])]
                outfile.write(string.format(*line))

    # We only return the best value of the criterion function and the corresponding parameter
    # vector.
    rslt = list()
    rslt.append(estimate_obj.get_attr('f_step'))
    rslt.append(estimate_obj.get_attr('x_step'))

    return rslt
