"""This module contains the capability to estimate the model."""
import shutil

from scipy.optimize import minimize
import pandas as pd

from interalpy.estimate.estimate_auxiliary import estimate_simulate
from interalpy.shared.shared_auxiliary import dist_class_attributes
from interalpy.shared.shared_auxiliary import to_optimizer
from interalpy.estimate.clsEstimate import EstimateClass
from interalpy.custom_exceptions import InteralpyError
from interalpy.custom_exceptions import MaxfunError
from interalpy.clsModel import ModelCls


def estimate(fname):
    """This function allow to estimate the model."""
    model_obj = ModelCls(fname)

    # Distribute class attributes for further processing.
    est_file, maxfun, optimizer, opt_options, r, eta, b, nu, sim_agents, est_agents = \
        dist_class_attributes(model_obj, 'est_file', 'maxfun', 'optimizer', 'opt_options', 'r',
            'eta', 'b', 'nu', 'sim_agents', 'est_agents')

    # We read in the estimation dataset.
    df = pd.read_pickle(est_file)

    # We might want to estimate on a subset of individuals only.
    subset = df['Participant.code'].unique()[:est_agents]
    df = df.loc[(subset, slice(None), slice(None)), :]

    # We simulate a sample at the starting point.
    x_start = to_optimizer([r, eta, nu])
    estimate_simulate('start', x_start, model_obj, df)

    # We need to initialize the shared classes.
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
    x_stop = to_optimizer(estimate_obj.get_attr('x_step'))
    estimate_simulate('stop', x_stop, model_obj, df)

    # We can compare a simulated sample using the estimation results with the observed estimation
    # dataset.
    shutil.copy('stop/compare.interalpy.info', '.')

    # We only return the best value of the criterion function and the corresponding parameter
    # vector.
    rslt = list()
    rslt.append(estimate_obj.get_attr('f_step'))
    rslt.append(estimate_obj.get_attr('x_step'))

    return rslt
