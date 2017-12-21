"""This module contains auxiliary functions that are only relevant for the estimation process."""
import shutil
import copy
import os

from interalpy.simulate.simulate import simulate


def estimate_simulate(which, points, model_obj):
    """This function allows to easily simulate samples at the beginning and the end of the
    estimation."""
    if os.path.exists(which):
        shutil.rmtree(which)

    os.mkdir(which)
    os.chdir(which)

    sim_model = copy.deepcopy(model_obj)
    sim_model.attr['sim_file'] = which

    sim_model.update(points)
    sim_model.write_out(which + '.interalpy.ini')
    simulate(which + '.interalpy.ini')
    os.chdir('../')