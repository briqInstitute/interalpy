"""This module contains ensures that all events are logged properly."""
from interalpy.shared.clsBase import BaseCls


class LoggerCls(BaseCls):
    """This class manages the logging of events."""
    def __init__(self):
        self.attr = dict()
        self.attr['errors'] = []

    def record_event(self, error_code):
        """This method records the error codes of events."""
        self.attr['errors'].append(error_code)

    def flush(self, outfile):
        """This method records all things related to an evaluation"""
        for error_code in set(self.attr['errors']):
            msg = '\n Warning: '

            if error_code == 0:
                msg += 'Overflow, FloatingPoint errors in luce_prob()'
            elif error_code == 1:
                msg += 'small adjustment to bounds in to_real()'
            else:
                raise NotImplementedError

            outfile.write(msg + '\n')

        # Reset the container for the error cases.
        self.attr['errors'] = []


logger_obj = LoggerCls()
