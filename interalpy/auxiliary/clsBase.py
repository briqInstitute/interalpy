"""This module contains the baseline class."""


class BaseCls(object):
    """This class provides some basic capabilties for all the project's classes"""
    def __init__(self):
        pass

    def get_attr(self, key):
        """This method allows to access class attribute."""
        return self.attr[key]

