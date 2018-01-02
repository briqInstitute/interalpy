#!/usr/bin/env python
"""This module is the first attempt to start some regression tests."""
from datetime import timedelta
from datetime import datetime
import importlib
import functools
import argparse
import shutil
import random
import os

import numpy as np

from interalpy.tests.test_auxiliary import get_random_string
from auxiliary_property import send_notification
from auxiliary_property import print_rslt_ext
from auxiliary_property import collect_tests
from auxiliary_property import finish


def run(args):
    """This function runs the property test battery."""

    is_check = args.request == 'investigate'

    if is_check:
        seed = args.seed
    else:
        hours = args.hours


    test_dict = collect_tests()

    rslt = dict()
    for module in test_dict.keys():
        rslt[module] = dict()
        for test in test_dict[module]:
            rslt[module][test] = [0, 0]



    os.system('git clean -d -f')


    #
    if is_check:

        np.random.seed(seed)

        # Now I can run a random test.
        module = np.random.choice(sorted(list(test_dict.keys())))
        test = np.random.choice(test_dict[module])

        print('\n ... running ' + module + ', ' + test + ' with seed ' + str(seed))
        mod = importlib.import_module('interalpy.tests.' + module.replace('.py', ''))
        test_fun = getattr(mod, test)

        test_fun()

    else:
        err_msg = []

        start, timeout = datetime.now(), timedelta(hours=hours)

        print_rslt = functools.partial(print_rslt_ext, start, timeout)

        print_rslt(rslt, err_msg)

        while True:

            seed = random.randrange(1, 100000)

            np.random.seed(seed)

            dirname = get_random_string()

            # Now I can run a random test.
            module = np.random.choice(sorted(list(test_dict.keys())))

            test = np.random.choice(test_dict[module])

            mod = importlib.import_module('interalpy.tests.' + module.replace('.py', ''))
            test_fun = getattr(mod, test)


            if os.path.exists(dirname):
                shutil.rmtree(dirname)

            os.mkdir(dirname)
            os.chdir(dirname)

            try:
                test_fun()
                rslt[module][test][0] += 1
            except Exception:
                rslt[module][test][1] += 1
                msg = traceback.format_exc()
                err_msg += [(module, test, seed, msg)]

            os.chdir('../')

            shutil.rmtree(dirname)

            print_rslt(rslt, err_msg)

            if timeout < datetime.now() - start:
                break

        finish(rslt)

        send_notification('property', hours=hours)


if __name__ == '__main__':

    parser = argparse.ArgumentParser('Work with property tests.')

    parser.add_argument('--request', action='store', dest='request', help='task to perform',
                        required=True, choices=['run', 'investigate'])

    parser.add_argument('--seed', action='store', dest='seed', type=int, help='seed')

    parser.add_argument('--hours', action='store', dest='hours', type=float, help='hours')

    run(parser.parse_args())
