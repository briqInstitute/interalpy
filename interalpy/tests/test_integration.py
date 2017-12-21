"""This module contains some integration tests."""
from interalpy.tests.test_auxiliary import get_random_init
from interalpy import simulate
from interalpy import estimate


def test_1():
    """This test simply runs the core workflow of simulation and estimation."""
    for _ in range(5):
        get_random_init()
        simulate('test.interalpy.ini')
        estimate('test.interalpy.ini')
