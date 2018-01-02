"""This module contains the capability to simulate the synthetic outcome for a given model
specification."""
import pandas as pd
import numpy as np

from interalpy.shared.shared_auxiliary import dist_class_attributes
from interalpy.simulate.simulate_auxiliary import format_integer
from interalpy.simulate.simulate_auxiliary import sample_choice
from interalpy.simulate.simulate_auxiliary import format_float
from interalpy.simulate.simulate_auxiliary import write_info
from interalpy.shared.shared_auxiliary import solve_grid
from interalpy.clsModel import ModelCls


def simulate(fname):
    """This function simulated the model from an initialization file."""
    # Process initialization file
    model_obj = ModelCls(fname)

    # Distribute class attributes for further processing.
    paras_obj, sim_seed, sim_agents, sim_file = dist_class_attributes(model_obj, 'paras_obj',
        'sim_seed', 'sim_agents', 'sim_file')

    # Since all individuals are equivalent, we can  simply restrict attention to the choices
    # in the from of a grid.
    r, eta, b, nu = paras_obj.get_values('econ', 'all')

    grid = solve_grid(r, eta, b, nu)

    np.random.seed(sim_seed)

    df_simulated = []
    for i, _ in enumerate(range(sim_agents)):
        grid_agent = grid.copy(deep=True)
        grid_agent['Participant.code'] = i
        grid_agent = grid_agent.apply(sample_choice, axis=1)
        df_simulated += [grid_agent]

    df_simulated = pd.concat(df_simulated)

    df_simulated['Participant.code'] = df_simulated['Participant.code'].astype(int)
    df_simulated.set_index(['Participant.code', 'Question', 'm'], inplace=True, drop=False)

    columns = ['Participant.code', 'Question', 'm', 'D', 'eu_a', 'eu_b', 'prob_a', 'prob_b']
    df_simulated = df_simulated[columns]

    df_simulated.sort_index(inplace=True, sort_remaining=True)

    formats = []
    formats += [format_integer, format_integer, format_float, format_integer, format_float]
    formats += [format_float, format_float, format_float]
    with open(sim_file + '.interalpy.txt', 'w') as file_:
        df_simulated.to_string(file_, index=False, header=True, na_rep='.', formatters=formats)

    df_simulated['Question'] = df_simulated['Question'].astype(np.int)
    df_simulated.to_pickle(sim_file + '.interalpy.pkl')

    write_info(df_simulated, sim_file, sim_seed, b, r, eta, nu)

    return df_simulated


