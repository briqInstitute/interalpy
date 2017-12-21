

class MaxfunError(Exception):
    """This custom exception is raised if the maximum number of function evaluations is reached."""
    def __init__(self):
        pass


class InteralpyError(Exception):
    """This custom exception is used throughout the package."""
    def __init__(self, message):
        self.message = message
