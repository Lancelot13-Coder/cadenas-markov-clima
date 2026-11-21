from django import forms

from .constants import WEATHER_STATES
from .simulation import MAX_SIMULATION_STEPS, MIN_SIMULATION_STEPS


class SimulationForm(forms.Form):
    initial_state = forms.ChoiceField(
        label="Estado inicial",
        required=False,
        choices=[("", "Distribución uniforme predeterminada")]
        + [(state, state) for state in WEATHER_STATES],
        error_messages={"invalid_choice": "Seleccione un estado inicial válido."},
    )
    steps = forms.IntegerField(
        label="Pasos de la secuencia",
        initial=10,
        min_value=MIN_SIMULATION_STEPS,
        max_value=MAX_SIMULATION_STEPS,
        error_messages={
            "required": "Ingrese una longitud entre 1 y 100 pasos.",
            "invalid": "La longitud debe ser un entero entre 1 y 100 pasos.",
            "min_value": "La longitud debe estar entre 1 y 100 pasos.",
            "max_value": "La longitud debe estar entre 1 y 100 pasos.",
        },
    )
    seed = forms.IntegerField(
        label="Semilla (opcional)",
        required=False,
        error_messages={"invalid": "La semilla debe ser un número entero."},
    )
