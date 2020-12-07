# -*- coding: utf-8 -*-

import os

import numpy as np

from btb.tuning.tunable import Tunable
from btb.tuning.tuners import GCPEiTuner, GCPTuner, GPEiTuner, GPTuner, UniformTuner


def _tuning_function(tuner_class, scoring_function, tunable_hyperparameters, iterations):
    tunable = Tunable.from_dict(tunable_hyperparameters)
    tuner = tuner_class(tunable)
    gcp_debug_path = os.environ.get('GCP_DEBUG_PATH')
    if gcp_debug_path:
        debug_path = os.path.join(gcp_debug_path, f'{scoring_function.__self__}')
        tuner.debug_path = debug_path
        os.makedirs(debug_path, exist_ok=True)

    best_score = -np.inf

    for _ in range(iterations):
        proposal = tuner.propose()
        score = scoring_function(**proposal)
        tuner.record(proposal, score)
        best_score = max(score, best_score)

    return best_score


def make_btb_tuning_function(tuner_class):
    """Create a tuning function for a tuner class based on ``BTB``.

    Args:
        tuner_class (btb.tuning.tuners.base.BaseTuner):
            A tuner class based on the BTB ``BaseTuner``.

    Return:
        callable:
            Return a tuning function using the given tuner class.
    """
    def btb_tuning_function(scoring_function, tunable_hyperparameters, iterations):
        return _tuning_function(tuner_class, scoring_function, tunable_hyperparameters, iterations)

    return btb_tuning_function


def gptuner(scoring_function, tunable_hyperparameters, iterations):
    return _tuning_function(GPTuner, scoring_function, tunable_hyperparameters, iterations)


def gpeituner(scoring_function, tunable_hyperparameters, iterations):
    return _tuning_function(GPEiTuner, scoring_function, tunable_hyperparameters, iterations)


def gcptuner(scoring_function, tunable_hyperparameters, iterations):
    return _tuning_function(GCPTuner, scoring_function, tunable_hyperparameters, iterations)


def gcpeituner(scoring_function, tunable_hyperparameters, iterations):
    return _tuning_function(GCPEiTuner, scoring_function, tunable_hyperparameters, iterations)


def uniformtuner(scoring_function, tunable_hyperparameters, iterations):
    return _tuning_function(UniformTuner, scoring_function, tunable_hyperparameters, iterations)
