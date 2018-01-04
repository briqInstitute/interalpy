#!/usr/bin/env python
"""This module just starts numerous estimations on our empirical data. The goal is to ensure that
the code handles it all well. This increases the robustness of the package as the data is not so
well-behaved as our simulations."""
from datetime import timedelta
from datetime import datetime
import random

from auxiliary_tests import distribute_command_line_arguments
from auxiliary_tests import process_command_line_arguments
from auxiliary_robustness import run_robustness_test
from auxiliary_tests import send_notification
from auxiliary_tests import cleanup


def run(args):
    """This function runs the robustness test battery."""
    args = distribute_command_line_arguments(args)

    cleanup()

    if args['is_check']:
        run_robustness_test(args['seed'])
    else:

        start, timeout = datetime.now(), timedelta(hours=args['hours'])
        num_tests = 0
        while True:

            seed = random.randrange(1, 100000)
            try:
                run_robustness_test(seed)
            except Exception:
                send_notification('robustness', is_failed=True, seed=seed)
                raise SystemExit

            cleanup()

            num_tests += 1

            if timeout < datetime.now() - start:
                break

        send_notification('robustness', is_failed=False, hours=args['hours'], num_tests=num_tests)


if __name__ == '__main__':

    args = process_command_line_arguments('robustness')

    run(args)
