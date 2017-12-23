"""This module contains some unit tests."""
import numpy as np

from interalpy.shared.shared_auxiliary import dist_class_attributes, to_econ, to_optimizer
from interalpy.shared.shared_auxiliary import atemporal_utility
from interalpy.tests.test_auxiliary import get_random_init
from interalpy.shared.shared_auxiliary import luce_prob
from interalpy.estimate.estimate import estimate
from interalpy.simulate.simulate import simulate
from interalpy.clsModel import ModelCls
from interalpy.read.read import read


def test_1():
    """This test simply checks that some basic functions are properly evaluated for all valid
    specifications of the initialization files."""
    get_random_init()

    model_obj = ModelCls('test.interalpy.ini')
    r, eta, nu, b = dist_class_attributes(model_obj, 'r', 'eta', 'nu', 'b')

    for _ in range(100):

        payments = np.random.lognormal(size=2)
        u = atemporal_utility(payments, r, eta, b)
        np.testing.assert_equal(u >= 0, True)

        u_x, u_y = np.random.lognormal(size=2)
        prob = luce_prob(u_x, u_y, nu)
        np.testing.assert_almost_equal(np.sum(prob), 1.0)
        np.testing.assert_equal(np.all(prob) >= 0, True)


def test_2():
    """This test checks the special case of linear atemporal utility."""
    r, eta, b = 0, 0, 1
    for _ in range(1000):
        payment = np.random.lognormal(size=2)
        stat = atemporal_utility(payment, r, eta, b)
        np.testing.assert_equal(stat, payment.sum())


def test_3():
    """This test checks that the random initialization files can all be properly processed."""
    for _ in range(100):
        get_random_init()
        read('test.interalpy.ini')


def test_4():
    """This test ensures the back an fourth transformations for the parameter values."""
    for _ in range(500):
        x = np.random.normal(loc=0, scale=5, size=3)
        np.testing.assert_almost_equal(x, to_optimizer(to_econ(x)))


def test_5():
    """This test ensures that writing out an initialization fi"""
    get_random_init()
    simulate('test.interalpy.ini')

    x, _ = estimate('test.interalpy.ini')

    model_obj = ModelCls('test.interalpy.ini')
    model_obj.write_out('alt.interalpy.ini')
    y, _ = estimate('alt.interalpy.ini')

    np.testing.assert_almost_equal(y, x)

