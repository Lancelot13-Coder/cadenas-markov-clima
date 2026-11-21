"""Validaciones del dominio para probabilidades del modelo de Markov."""

import numpy as np

from .constants import WEATHER_STATES

PROBABILITY_TOLERANCE = 1e-9


def _as_numeric_array(values, description):
    try:
        array = np.asarray(values, dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{description} debe contener únicamente números.") from exc
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{description} debe contener únicamente valores finitos.")
    return array


def validate_transition_matrix(matrix, tolerance=PROBABILITY_TOLERANCE):
    """Valida forma, rango y normalización por fila de la matriz de transición."""
    array = _as_numeric_array(matrix, "La matriz de transición")
    expected_shape = (len(WEATHER_STATES), len(WEATHER_STATES))
    if array.shape != expected_shape:
        raise ValueError("La matriz de transición debe tener dimensiones 3 × 3.")
    if np.any((array < 0) | (array > 1)):
        raise ValueError("Cada probabilidad de transición debe estar entre 0 y 1.")
    if not np.allclose(array.sum(axis=1), 1.0, rtol=0.0, atol=tolerance):
        raise ValueError("Cada fila de la matriz de transición debe sumar 1.")
    return array


def validate_distribution(distribution, tolerance=PROBABILITY_TOLERANCE):
    """Valida dimensión, rango y suma de una distribución inicial."""
    array = _as_numeric_array(distribution, "La distribución inicial")
    if array.shape != (len(WEATHER_STATES),):
        raise ValueError("La distribución inicial debe contener exactamente 3 probabilidades.")
    if np.any((array < 0) | (array > 1)):
        raise ValueError("Cada probabilidad inicial debe estar entre 0 y 1.")
    if not np.isclose(array.sum(), 1.0, rtol=0.0, atol=tolerance):
        raise ValueError("La distribución inicial debe sumar 1.")
    return array
