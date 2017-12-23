#!/usr/bin/env python
"""This module just starts numerous estimations on our empirical data. The goal is to ensure that
the code handles it all well. This increases the robustness of the package as the data is not so
well-behaved as our simulations."""
from datetime import timedelta
from datetime import datetime
import argparse
import os

import numpy as np

from interalpy.tests.test_auxiliary import get_random_init
from interalpy import estimate

# This requires access to a private repository that ensures that the data remains confidential.
DATA_PATH = os.environ['INTERTEMPORAL_ALTRUISM'] + '/sandbox/peisenha/structural_attempt/data'


def run(args):

    hours = args.hours

    start, timeout = datetime.now(), timedelta(hours=hours)

    # Initial cleanup
    os.system('git clean -d -f')

    while True:

        constr = dict()
        constr['est_file'] = DATA_PATH + '/risk_data_estimation.pkl'
        constr['num_agents'] = np.random.randint(1, 244 + 1)
        constr['maxfun'] = np.random.randint(500, 10000)

        get_random_init(constr)

        estimate('test.interalpy.ini')

        os.system('git clean -d -f')

        if timeout < datetime.now() - start:
            break


if __name__ == '__main__':

    parser = argparse.ArgumentParser('Test robustness of package with empirical data.')

    parser.add_argument('--hours', action='store', dest='hours', type=float, help='hours')

    run(parser.parse_args())
