"""This module contains the capability to estimate the model."""
import shutil
import copy

from scipy.optimize import minimize

from interalpy.estimate.estimate_auxiliary import estimate_simulate
from interalpy.shared.shared_auxiliary import dist_class_attributes
from interalpy.estimate.estimate_auxiliary import estimate_cleanup
from interalpy.estimate.clsEstimate import EstimateClass
from interalpy.custom_exceptions import InteralpyError
from interalpy.custom_exceptions import MaxfunError
from interalpy.process.process import process
from interalpy.clsModel import ModelCls


def estimate(fname):
    """This function allow to estimate the model."""
    estimate_cleanup()

    model_obj = ModelCls(fname)

    # Distribute class attributes for further processing.
    est_file, maxfun, optimizer, opt_options, paras_obj, sim_agents, est_agents, \
        est_detailed = dist_class_attributes(model_obj, 'est_file', 'maxfun', 'optimizer',
            'opt_options', 'paras_obj', 'sim_agents', 'est_agents', 'est_detailed')

    df = process(est_file, est_agents)

    x_optim_free_start = paras_obj.get_values('optim', 'free')

    # We simulate a sample at the starting point.
    if est_detailed:
        estimate_simulate('start', x_optim_free_start, model_obj, df)

    # We need to initialize the shared classes, which also starts the logfile and writes out some
    # initial information.
    estimate_obj = EstimateClass(df, copy.deepcopy(paras_obj), maxfun)

    # Not all algorithms are using the starting values as the very first evaluation.
    estimate_obj.evaluate(x_optim_free_start)

    # We are faced with a serious estimation request.
    opt = dict()
    opt['message'] = 'Optimization reached maximum number of function evaluations.'
    opt['success'] = False

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
            raise InteralpyError('flawed choice of optimization method')

        try:
            opt = minimize(estimate_obj.evaluate, x_optim_free_start, method=method, options=options)
        except MaxfunError:
            pass

    # Now we can wrap up all estimation related tasks.
    estimate_obj.finish(opt)

    # We also simulate a sample at the stop of the estimation.
    x_econ_all_step = estimate_obj.get_attr('x_econ_all_step')
    paras_obj.set_values('econ', 'all', x_econ_all_step)
    x_optim_free_step = paras_obj.get_values('optim', 'free')

    if est_detailed:
        # We can compare a simulated sample using the estimation results with the observed
        # estimation dataset.
        estimate_simulate('stop', x_optim_free_step, model_obj, df)
        shutil.copy('stop/compare.interalpy.info', '.')

    # We only return the best value of the criterion function and the corresponding parameter
    # vector.
    rslt = list()
    rslt.append(estimate_obj.get_attr('f_step'))
    rslt.append(estimate_obj.get_attr('x_econ_all_step'))

    return rslt
