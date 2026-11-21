from django.shortcuts import render

from .calculations import initial_distribution_for_state, required_distributions
from .constants import (
    DEFAULT_INITIAL_DISTRIBUTION,
    DEFAULT_TRANSITION_MATRIX,
    WEATHER_STATES,
)
from .forms import SimulationForm
from .simulation import simulate_sequence


def index(request):
    form = SimulationForm(request.POST or None)
    selected_state = ""
    steps = 10
    seed = None
    sequence = None

    if request.method == "POST" and form.is_valid():
        selected_state = form.cleaned_data["initial_state"]
        steps = form.cleaned_data["steps"]
        seed = form.cleaned_data["seed"]

    if selected_state:
        initial_distribution = initial_distribution_for_state(selected_state)
    else:
        initial_distribution = DEFAULT_INITIAL_DISTRIBUTION

    results = required_distributions(initial_distribution=initial_distribution)
    if request.method == "POST" and form.is_valid():
        sequence = simulate_sequence(
            steps,
            initial_distribution=initial_distribution,
            seed=seed,
        )

    transition_rows = [
        {"current_state": state, "probabilities": DEFAULT_TRANSITION_MATRIX[index]}
        for index, state in enumerate(WEATHER_STATES)
    ]
    result_rows = [
        {"steps": count, "probabilities": distribution}
        for count, distribution in results.items()
    ]
    initial_rows = tuple(zip(WEATHER_STATES, initial_distribution))
    chart_data = {
        "labels": [f"Paso {count}" for count in results],
        "datasets": [
            {
                "label": state,
                "data": [float(results[count][index]) for count in results],
            }
            for index, state in enumerate(WEATHER_STATES)
        ],
    }

    return render(
        request,
        "simulador/index.html",
        {
            "form": form,
            "states": WEATHER_STATES,
            "transition_rows": transition_rows,
            "initial_rows": initial_rows,
            "result_rows": result_rows,
            "chart_data": chart_data,
            "sequence": sequence,
            "selected_state": selected_state,
        },
    )
