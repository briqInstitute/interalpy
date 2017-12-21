#!/usr/bin/env python
"""This module is the first attempt to set up some reliability testing."""
from interalpy import simulate
from interalpy import estimate

simulate('truth.interalpy.ini')
estimate('start.interalpy.ini')
