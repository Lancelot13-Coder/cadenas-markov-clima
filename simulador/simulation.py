"""Generación de secuencias climáticas reproducibles."""

from numbers import Integral

import numpy as np

from .constants import (
    DEFAULT_INITIAL_DISTRIBUTION,
    DEFAULT_TRANSITION_MATRIX,
    WEATHER_STATES,
)
from .validation import validate_distribution, validate_transition_matrix

MIN_SIMULATION_STEPS = 1
MAX_SIMULATION_STEPS = 100


def simulate_sequence(
    steps,
    initial_distribution=DEFAULT_INITIAL_DISTRIBUTION,
    transition_matrix=DEFAULT_TRANSITION_MATRIX,
    seed=None,
):
    """Devuelve el estado inicial y `steps` transiciones posteriores."""
    if (
        isinstance(steps, bool)
        or not isinstance(steps, Integral)
        or not MIN_SIMULATION_STEPS <= steps <= MAX_SIMULATION_STEPS
    ):
        raise ValueError("La longitud debe ser un entero entre 1 y 100 pasos.")

    initial = validate_distribution(initial_distribution)
    matrix = validate_transition_matrix(transition_matrix)
    rng = np.random.default_rng(seed)

    current = int(rng.choice(len(WEATHER_STATES), p=initial))
    sequence = [WEATHER_STATES[current]]
    for _ in range(int(steps)):
        current = int(rng.choice(len(WEATHER_STATES), p=matrix[current]))
        sequence.append(WEATHER_STATES[current])
    return tuple(sequence)
