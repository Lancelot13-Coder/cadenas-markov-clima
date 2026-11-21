"""Parámetros predeterminados del modelo climático educativo."""

WEATHER_STATES = ("Soleado", "Nublado", "Lluvioso")

# Matriz hipotética y configurable. Filas: estado actual; columnas: siguiente estado.
DEFAULT_TRANSITION_MATRIX = (
    (0.70, 0.20, 0.10),
    (0.30, 0.40, 0.30),
    (0.20, 0.30, 0.50),
)

# Distribución predeterminada uniforme, en el mismo orden que WEATHER_STATES.
DEFAULT_INITIAL_DISTRIBUTION = (1 / 3, 1 / 3, 1 / 3)
