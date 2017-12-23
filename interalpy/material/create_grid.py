"""This module contains the capabilities to create auxiliary resources used throughout the
package."""
import os

import pandas as pd

from interalpy.config_interalpy import DATA_DTYPES

# I need to create a fixed grid for the questions that is used throughout the package. This will
# be extended as we use more and more questions.
DATAPATH = os.environ['INTERTEMPORAL_ALTRUISM'] + '/sandbox/peisenha/structural_attempt/data'
df = pd.read_pickle(DATAPATH + '/risk_data_estimation.pkl')
code = df['Participant.code'].values[0]
grid = df[df['Participant.code'] == code].copy(deep=True)
grid = grid.astype(DATA_DTYPES)
grid.set_index(['Participant.code', 'Question', 'm'], inplace=True, drop=False)
grid.to_pickle('grid.interalpy.pkl',  protocol=2)
