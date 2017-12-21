"""This module contains the class for the model specification."""
import numpy as np

from interalpy.shared.shared_auxiliary import dist_class_attributes, to_econ
from interalpy.shared.shared_auxiliary import print_init_dict
from interalpy.shared.clsBase import BaseCls
from interalpy.read.read import read


class ModelCls(BaseCls):
    """This class manages all issues about the model specification."""
    def __init__(self, fname):
        init_dict = read(fname)

        self.attr = dict()

        # Preferences
        self.attr['eta'] = init_dict['PREFERENCES']['eta']
        self.attr['b'] = init_dict['PREFERENCES']['b']
        self.attr['r'] = init_dict['PREFERENCES']['r']

        # Luce Model
        self.attr['nu'] = init_dict['LUCE']['nu']

        # Simulation
        self.attr['sim_agents'] = init_dict['SIMULATION']['agents']
        self.attr['sim_seed'] = init_dict['SIMULATION']['seed']
        self.attr['sim_file'] = init_dict['SIMULATION']['file']

        # Estimation
        self.attr['optimizer'] = init_dict['ESTIMATION']['optimizer']
        self.attr['est_agents'] = init_dict['ESTIMATION']['agents']
        self.attr['est_file'] = init_dict['ESTIMATION']['file']
        self.attr['maxfun'] = init_dict['ESTIMATION']['maxfun']

        # Optimizer options
        self.attr['opt_options'] = dict()

        self.attr['opt_options']['SCIPY-BFGS'] = dict()
        self.attr['opt_options']['SCIPY-BFGS']['gtol'] = init_dict['SCIPY-BFGS']['gtol']
        self.attr['opt_options']['SCIPY-BFGS']['eps'] = init_dict['SCIPY-BFGS']['eps']

        self.attr['opt_options']['SCIPY-POWELL'] = dict()
        self.attr['opt_options']['SCIPY-POWELL']['xtol'] = init_dict['SCIPY-POWELL']['xtol']
        self.attr['opt_options']['SCIPY-POWELL']['ftol'] = init_dict['SCIPY-POWELL']['ftol']

        # We now need to check the integrity of the class instance.
        self._check_integrity()

    def update(self, x):
        """This method updates the estimation parameters."""
        x_econ = to_econ(x)

        self.attr['r'] = x_econ[0]
        self.attr['eta'] = x_econ[1]
        self.attr['nu'] = x_econ[2]

    def write_out(self, fname='test.interalpy.ini'):
        """This method write the class instance to the corresponding initialization file."""

        init_dict = dict()

        # Preferences
        init_dict['PREFERENCES'] = dict()

        init_dict['PREFERENCES']['eta'] = self.attr['eta']
        init_dict['PREFERENCES']['b'] = self.attr['b']
        init_dict['PREFERENCES']['r'] = self.attr['r']

        # Luce Model
        init_dict['LUCE'] = dict()
        init_dict['LUCE']['nu'] = self.attr['nu']

        # Simulation
        init_dict['SIMULATION'] = dict()
        init_dict['SIMULATION']['agents'] = self.attr['sim_agents']
        init_dict['SIMULATION']['seed'] = self.attr['sim_seed']
        init_dict['SIMULATION']['file'] = self.attr['sim_file']

        # Estimation
        init_dict['ESTIMATION'] = dict()
        init_dict['ESTIMATION']['optimizer'] = self.attr['optimizer']
        init_dict['ESTIMATION']['agents'] = self.attr['est_agents']
        init_dict['ESTIMATION']['file'] = self.attr['est_file']
        init_dict['ESTIMATION']['maxfun'] = self.attr['maxfun']

        # Optimizer options
        init_dict['SCIPY-BFGS'] = dict()
        init_dict['SCIPY-BFGS']['gtol'] = self.attr['opt_options']['SCIPY-BFGS']['gtol']
        init_dict['SCIPY-BFGS']['eps'] = self.attr['opt_options']['SCIPY-BFGS']['eps']

        init_dict['SCIPY-POWELL'] = dict()
        init_dict['SCIPY-POWELL']['xtol'] = self.attr['opt_options']['SCIPY-POWELL']['xtol']
        init_dict['SCIPY-POWELL']['ftol'] = self.attr['opt_options']['SCIPY-POWELL']['ftol']

        print_init_dict(init_dict, fname)

    def _check_integrity(self):
        """This method checks the integrity of the class instance."""
        # Distribute class attributes for further processing.
        r, eta, nu, b, sim_seed, sim_agents, sim_file, est_agents, maxfun, est_file, \
            optimizer, opt_options = dist_class_attributes(self, 'r',  'eta', 'nu', 'b', 'sim_seed',
                'sim_agents', 'sim_file', 'est_agents', 'maxfun', 'est_file', 'optimizer',
                'opt_options')

        # Preference parameters
        np.testing.assert_equal((eta > -1) and (eta < 1), True)
        np.testing.assert_equal((r > -1) and (r < 1), True)
        np.testing.assert_equal(b >= 0, True)

        # Simulation request
        np.testing.assert_equal(isinstance(sim_agents, int), True)
        np.testing.assert_equal(sim_agents >= 0, True)

        np.testing.assert_equal(isinstance(sim_file, str), True)

        np.testing.assert_equal(isinstance(sim_seed, int), True)
        np.testing.assert_equal(sim_seed >= 0, True)

        # Luce specification
        np.testing.assert_equal((nu > 0) and (nu < 5), True)

        # Estimation request
        np.testing.assert_equal(isinstance(est_file, str), True)

        np.testing.assert_equal(est_agents > 0, True)
        np.testing.assert_equal(isinstance(est_agents, int), True)

        np.testing.assert_equal(maxfun >= 0, True)
        np.testing.assert_equal(isinstance(maxfun, int), True)

        np.testing.assert_equal(optimizer in ['SCIPY-POWELL', 'SCIPY-BFGS'], True)

        # Optimizer options
        cond = set(opt_options.keys()) == set(['SCIPY-BFGS', 'SCIPY-POWELL'])
        np.testing.assert_equal(cond, True)

        # Optimizer options, SCIPY-BFGS
        scipy_bfgs = opt_options['SCIPY-BFGS']
        for label in scipy_bfgs.keys():
            np.testing.assert_equal(scipy_bfgs[label] > 0, True)
            np.testing.assert_equal(isinstance(scipy_bfgs[label], float), True)

