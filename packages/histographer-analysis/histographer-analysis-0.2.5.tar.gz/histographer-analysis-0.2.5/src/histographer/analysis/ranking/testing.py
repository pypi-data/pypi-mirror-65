from histographer.analysis.ranking.algorithms import balanced_rank_estimation, elo, rank_centrality, iterate_active_elo, active_elo
from histographer.analysis.ranking.mock import generate_mock_comparisons, generate_mock_comparisons_btl
from histographer.analysis.ranking.error import e_vs_error_rate, e_vs_n_comparisons, e_vs_n_objects
from random import sample
import numpy as np

N_COMPARISONS = 500
N_OBJECTS = 10
ERROR_RATE = 0.05

print(active_elo(N_COMPARISONS, N_OBJECTS))
