"""This module contains the class for the collection of parameters."""
import numpy as np

from interalpy.shared.clsBase import BaseCls
from interalpy.config_interalpy import BOUNDS, SMALL_FLOAT, PARA_LABELS
from interalpy.paras.clsPara import ParaCls
from interalpy.custom_exceptions import InteralpyError
from interalpy.logging.clsLogger import logger_obj

class ParasCls(BaseCls):
    """This class manages all issues about the model specification."""

    def __init__(self, init_dict):
        """This method initializes the parameter class."""

        self.attr = dict()


        self.attr['para_objs'] = []

        # preference parameters
        for label in ['r', 'eta', 'b']:
            value, is_fixed = init_dict['PREFERENCES'][label]
            bounds = BOUNDS[label]
            self.attr['para_objs'] += [ParaCls(label, value, is_fixed, bounds)]

        # Luce model
        value, is_fixed = init_dict['LUCE']['nu']
        bounds = BOUNDS['nu']
        self.attr['para_objs'] += [ParaCls('nu', value, is_fixed, bounds)]

    def get_para(self, label):
        """This method allows to access a single parameter."""
        # TODO: This needs to be aligned with the get_values design which is much better.
        # Distribute class attributes
        para_objs = self.attr['para_objs']

        for para_obj in para_objs:
            if label == para_obj.get_attr('label'):
                value = para_obj.get_attr('value')
                is_fixed = para_obj.get_attr('is_fixed')
                bounds = para_obj.get_attr('bounds')

                return value, is_fixed, bounds

        raise InteralpyError('parameter not available')

    def set_values(self, perspective, which, values):
        """This method allows to directly set the values of the parameters."""
        # Distribute class attributes
        para_objs = self.attr['para_objs']

        count = 0

        for label in PARA_LABELS:
            for para_obj in para_objs:
                # We are only interested in the free parameters.
                if which == 'free' and para_obj.get_attr('is_fixed'):
                    continue
                # We are only interested in one particular parameter.
                if label != para_obj.get_attr('label'):
                    continue

                if perspective in ['econ']:
                    value = values[count]
                elif perspective in ['optim']:
                    bounds = para_obj.get_attr('bounds')
                    value = self._to_econ(values[count], bounds)
                else:
                    raise InteralpyError('misspecified request')

                para_obj.set_attr('value', value)

                count += 1

    def get_values(self, perspective, which):
        """This method allow to directly access the values of the parameters."""
        # Distribute class attributes
        para_objs = self.attr['para_objs']

        # Initialize containers
        values = list()

        for label in PARA_LABELS:
            for para_obj in para_objs:
                # We are only interested in the free parameters.
                if which == 'free' and para_obj.get_attr('is_fixed'):
                    continue
                # We are only interested in one particular parameter.
                if label != para_obj.get_attr('label'):
                    continue

                if perspective in ['econ']:
                    value = para_obj.get_attr('value')
                elif perspective in ['optim']:
                    value = self._to_optimizer(para_obj)
                else:
                    raise InteralpyError('misspecified request')

                values += [value]

        return values

    def _to_optimizer(self, para_obj):
        """This method transfers a single parameter to its value used by the optimizer."""
        # Distribute attributes
        lower, upper = para_obj.get_attr('bounds')
        value = self._to_real(para_obj.get_attr('value'), lower, upper)
        return value

    @staticmethod
    def _to_interval(val, lower, upper):
        """This function maps any value to a bounded interval."""
        interval = upper - lower
        return lower + interval / (1 + np.exp(-val))

    @staticmethod
    def _to_real(value, lower, upper):
        """This function transforms the bounded parameter back to the real line."""
        if np.isclose(value, lower):
            value += SMALL_FLOAT
            logger_obj.record_event(1)
        elif np.isclose(value, upper):
            value -= SMALL_FLOAT
            logger_obj.record_event(1)
        else:
            pass

        interval = upper - lower
        transform = (value - lower) / interval
        return np.log(transform / (1.0 - transform))

    def _to_econ(self, value, bounds):
        """This function transforms parameters over the whole real to a bounded interval."""
        value = self._to_interval(value, *bounds)
        return value