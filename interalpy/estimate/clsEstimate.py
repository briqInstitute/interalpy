"""This module contains the class to manage the model estimation."""
from interalpy.shared.shared_auxiliary import criterion_function
from interalpy.estimate.estimate_auxiliary import char_floats
from interalpy.shared.shared_auxiliary import to_optimizer
from interalpy.shared.shared_auxiliary import to_econ
from interalpy.custom_exceptions import MaxfunError
from interalpy.logging.clsLogger import logger_obj
from interalpy.config_interalpy import HUGE_FLOAT
from interalpy.shared.clsBase import BaseCls


class EstimateClass(BaseCls):
    """This class manages all issues about the model estimation."""
    def __init__(self, df, b, max_eval):

        self.attr = dict()

        # Initialization attributes
        self.attr['max_eval'] = max_eval
        self.attr['df'] = df
        self.attr['b'] = b

        # Housekeeping attributes
        self.attr['num_step'] = 0
        self.attr['num_eval'] = 0

        self.attr['x_current'] = None
        self.attr['x_start'] = None
        self.attr['x_step'] = None

        self.attr['f_current'] = HUGE_FLOAT
        self.attr['f_start'] = HUGE_FLOAT
        self.attr['f_step'] = HUGE_FLOAT

    def evaluate(self, x):
        """This method allows to evaluate the criterion function during an estimation"""

        # Distribute class attributes
        df = self.attr['df']
        b = self.attr['b']

        fval = criterion_function(df, b, *to_econ(x))

        self._logging(fval, to_econ(x))

        return fval

    def _logging(self, fval, x):
        """This methods manages all issues related to the logging of the estimation."""
        # Update current information
        self.attr['f_current'] = fval
        self.attr['x_current'] = x
        self.attr['num_eval'] += 1

        # Determine special events
        is_stop = (self.attr['max_eval'] == self.attr['num_eval']) and (self.attr['max_eval'] > 1)
        is_start = self.attr['num_eval'] == 1
        is_step = fval < self.attr['f_step']

        # Record information at start
        if is_start:
            self.attr['f_start'] = fval
            self.attr['x_start'] = x

        # Record information at step
        if is_step:
            self.attr['f_step'] = fval
            self.attr['x_step'] = x
            self.attr['num_step'] += 1

        # Update class attributes
        with open('est.interalpy.info', 'w') as outfile:
            fmt_ = '{:>25}    ' * 4

            # Write out information about criterion function
            outfile.write('\n {:<25}\n\n'.format('Criterion Function'))
            outfile.write(fmt_.format(*['', 'Start', 'Step', 'Current']) + '\n\n')
            args = (self.attr['f_start'], self.attr['f_step'], self.attr['f_current'])
            line = [''] + char_floats(args)
            outfile.write(fmt_.format(*line) + '\n\n')

            outfile.write('\n {:<25}\n\n'.format('Economic Parameters'))
            line = ['Identifier', 'Start', 'Step', 'Current']
            outfile.write(fmt_.format(*line) + '\n\n')
            for i, _ in enumerate(range(3)):
                line = [i]
                line += char_floats([self.attr['x_start'][i], self.attr['x_step'][i]])
                line += char_floats(self.attr['x_current'][i])
                outfile.write(fmt_.format(*line) + '\n')

            outfile.write('\n')
            fmt_ = '\n {:<25}   {:>25}\n'
            outfile.write(fmt_.format(*['Number of Evaluations', self.attr['num_eval']]))
            outfile.write(fmt_.format(*['Number of Steps', self.attr['num_step']]))

        with open('est.interalpy.log', 'a') as outfile:

            outfile.write('\n\n')
            fmt_ = '\n EVALUATION {:>10}  STEP {:>10}\n'
            outfile.write(fmt_.format(*[self.attr['num_eval'], self.attr['num_step']]))

            fmt_ = '\n Criterion {:>28}  \n\n\n'
            outfile.write(fmt_.format(char_floats(self.attr['f_current'])[0]))

            fmt_ = ' {:>10}   ' + '{:>25}    ' * 2
            line = ['Identifier', 'Economic', 'Optimizer']
            outfile.write(fmt_.format(*line) + '\n\n')

            x_values = self.attr['x_current']
            o_values = to_optimizer(x_values)

            for i, _ in enumerate(range(3)):
                line = [i] + char_floats([x_values[i], o_values[i]])
                outfile.write(fmt_.format(*line) + '\n')

            # We need to keep track of captured warnings.
            logger_obj.flush(outfile)

        # We can determine the estimation if the number of requested function evaluations is
        # reached.
        if is_stop:
            raise MaxfunError

    @staticmethod
    def finish(opt):
        """This method collects all operations to wrap up an estimation."""
        with open('est.interalpy.info', 'a') as outfile:
            outfile.write('\n {:<25}'.format('TERMINATED'))

        with open('est.interalpy.log', 'a') as outfile:
            outfile.write('\n {:<25}\n'.format('OPTIMIZER RETURN'))
            outfile.write('\n Message    {:<25}'.format(opt['message']))
            outfile.write('\n Success    {:<25}'.format(str(opt['success'])))
            outfile.write('\n')


