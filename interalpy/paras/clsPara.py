"""This module contains the class for a single parameter."""
from interalpy.shared.clsBase import BaseCls


class ParaCls(BaseCls):
    """This class manages all issues about a single parameter."""
    def __init__(self, label, value, is_fixed, bounds):
        """This method initializes the parameter class."""
        self.attr = dict()

        self.attr['label'] = label
        self.attr['value'] = value
        self.attr['is_fixed'] = is_fixed
        self.attr['bounds'] = bounds
