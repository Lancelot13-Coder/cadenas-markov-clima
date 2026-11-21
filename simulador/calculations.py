"""Cálculos de propagación de distribuciones de Markov."""

from numbers import Integral

import numpy as np

from .constants import (
    DEFAULT_INITIAL_DISTRIBUTION,
    DEFAULT_TRANSITION_MATRIX,
)
from .validation import validate_distribution, validate_transition_matrix

REQUIRED_STEPS = (1, 3, 5, 10)


def distribution_after_steps(
    steps,
    initial_distribution=DEFAULT_INITIAL_DISTRIBUTION,
    transition_matrix=DEFAULT_TRANSITION_MATRIX,
):
    """Calcula π(n) = π(0) × Pⁿ, con la distribución como vector fila."""
    if isinstance(steps, bool) or not isinstance(steps, Integral) or steps < 0:
        raise ValueError("El número de pasos debe ser un entero no negativo.")

    initial = validate_distribution(initial_distribution)
    matrix = validate_transition_matrix(transition_matrix)
    result = initial @ np.linalg.matrix_power(matrix, int(steps))
    return result


def required_distributions(
    initial_distribution=DEFAULT_INITIAL_DISTRIBUTION,
    transition_matrix=DEFAULT_TRANSITION_MATRIX,
):
    """Devuelve las distribuciones para los pasos educativos requeridos."""
    return {
        steps: distribution_after_steps(
            steps,
            initial_distribution=initial_distribution,
            transition_matrix=transition_matrix,
        )
        for steps in REQUIRED_STEPS
    }


def initial_distribution_for_state(state):
    """Construye la distribución concentrada para un estado inicial elegido."""
    from .constants import WEATHER_STATES

    try:
        index = WEATHER_STATES.index(state)
    except (ValueError, AttributeError) as exc:
        raise ValueError("Estado inicial no válido. Seleccione Soleado, Nublado o Lluvioso.") from exc

    distribution = np.zeros(len(WEATHER_STATES), dtype=float)
    distribution[index] = 1.0
    return distribution
