#!/usr/bin/env python
"""This module executes a complete testing of the package."""
import subprocess
import os

# Specification
request = dict()

request['property'] = dict()
request['property']['run'] = True
request['property']['hours'] = 0.0001

request['regression'] = dict()
request['regression']['run'] = True
request['regression']['tests'] = 1

request['robustness'] = dict()
request['robustness']['run'] = True
request['robustness']['hours'] = 0.001

# property-based testing
if request['property']['run']:
    os.chdir('property')
    cmd = 'python run.py --request run --hours ' + str(request['property']['hours'])
    subprocess.check_call(cmd, shell=True)
    os.chdir('../')

# regression testing
tests = 1
if request['regression']['run']:
    os.chdir('regression')
    cmd = 'python run.py --request check --tests ' + str(request['regression']['tests'])
    subprocess.check_call(cmd, shell=True)
    os.chdir('../')

# robustness testing
hours = 1
if request['robustness']['run']:
    os.chdir('robustness')
    cmd = 'python run.py --hours ' + str(request['robustness']['hours'])
    subprocess.check_call(cmd, shell=True)
    os.chdir('../')



