import numpy as np
from django.test import SimpleTestCase
from django.urls import reverse

from .calculations import (
    REQUIRED_STEPS,
    distribution_after_steps,
    initial_distribution_for_state,
    required_distributions,
)
from .constants import (
    DEFAULT_INITIAL_DISTRIBUTION,
    DEFAULT_TRANSITION_MATRIX,
    WEATHER_STATES,
)
from .simulation import (
    MAX_SIMULATION_STEPS,
    MIN_SIMULATION_STEPS,
    simulate_sequence,
)
from .validation import (
    PROBABILITY_TOLERANCE,
    validate_distribution,
    validate_transition_matrix,
)


class DefaultModelConstantsTests(SimpleTestCase):
    def test_states_use_the_approved_order(self):
        self.assertEqual(WEATHER_STATES, ("Soleado", "Nublado", "Lluvioso"))

    def test_default_transition_matrix_matches_the_approved_hypothetical_values(self):
        self.assertEqual(
            DEFAULT_TRANSITION_MATRIX,
            (
                (0.70, 0.20, 0.10),
                (0.30, 0.40, 0.30),
                (0.20, 0.30, 0.50),
            ),
        )
        self.assertEqual(len(DEFAULT_TRANSITION_MATRIX), len(WEATHER_STATES))
        for row in DEFAULT_TRANSITION_MATRIX:
            self.assertAlmostEqual(sum(row), 1.0, places=12)
            self.assertEqual(len(row), len(WEATHER_STATES))

    def test_default_initial_distribution_is_uniform(self):
        self.assertEqual(len(DEFAULT_INITIAL_DISTRIBUTION), len(WEATHER_STATES))
        for probability in DEFAULT_INITIAL_DISTRIBUTION:
            self.assertAlmostEqual(probability, 1 / 3)
        self.assertAlmostEqual(sum(DEFAULT_INITIAL_DISTRIBUTION), 1.0)


class ProbabilityValidationTests(SimpleTestCase):
    def test_valid_transition_matrix_and_distribution_are_returned_as_arrays(self):
        self.assertTrue(
            np.array_equal(
                validate_transition_matrix(DEFAULT_TRANSITION_MATRIX),
                np.asarray(DEFAULT_TRANSITION_MATRIX),
            )
        )
        self.assertTrue(
            np.allclose(
                validate_distribution(DEFAULT_INITIAL_DISTRIBUTION),
                DEFAULT_INITIAL_DISTRIBUTION,
                atol=PROBABILITY_TOLERANCE,
            )
        )

    def test_transition_matrix_rejects_wrong_dimensions(self):
        with self.assertRaisesRegex(ValueError, "3 × 3"):
            validate_transition_matrix(((1.0, 0.0), (0.0, 1.0)))

    def test_transition_matrix_rejects_out_of_range_probabilities(self):
        with self.assertRaisesRegex(ValueError, "entre 0 y 1"):
            validate_transition_matrix(
                ((1.1, -0.1, 0.0), (0.3, 0.4, 0.3), (0.2, 0.3, 0.5))
            )

    def test_transition_matrix_rejects_rows_that_do_not_sum_to_one(self):
        with self.assertRaisesRegex(ValueError, "fila.*sumar 1"):
            validate_transition_matrix(
                ((0.7, 0.2, 0.2), (0.3, 0.4, 0.3), (0.2, 0.3, 0.5))
            )

    def test_distribution_rejects_wrong_dimensions(self):
        with self.assertRaisesRegex(ValueError, "exactamente 3"):
            validate_distribution((0.5, 0.5))

    def test_distribution_rejects_out_of_range_probabilities(self):
        with self.assertRaisesRegex(ValueError, "entre 0 y 1"):
            validate_distribution((1.1, -0.1, 0.0))

    def test_distribution_rejects_a_sum_outside_tolerance(self):
        with self.assertRaisesRegex(ValueError, "debe sumar 1"):
            validate_distribution((0.3, 0.3, 0.3))

    def test_distribution_accepts_sum_error_within_tolerance(self):
        values = (1 / 3, 1 / 3, 1 / 3 + PROBABILITY_TOLERANCE / 2)
        validate_distribution(values)

    def test_non_finite_values_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "finitos"):
            validate_distribution((float("nan"), 0.5, 0.5))


class MarkovCalculationTests(SimpleTestCase):
    # Referencias obtenidas mediante multiplicación repetida con listas Python,
    # independiente de NumPy y de la implementación bajo prueba.
    REFERENCE_RESULTS = {
        1: (0.4000000000, 0.3000000000, 0.3000000000),
        3: (0.4440000000, 0.2860000000, 0.2700000000),
        5: (0.4537200000, 0.2833600000, 0.2629200000),
        10: (0.4564552656, 0.2826265072, 0.2609182272),
    }

    def test_required_steps_match_independent_references(self):
        results = required_distributions()
        self.assertEqual(tuple(results), REQUIRED_STEPS)
        for steps, expected in self.REFERENCE_RESULTS.items():
            with self.subTest(steps=steps):
                np.testing.assert_allclose(results[steps], expected, rtol=0.0, atol=1e-10)
                self.assertAlmostEqual(float(results[steps].sum()), 1.0, places=12)
                self.assertTrue(np.all(results[steps] >= 0.0))
                self.assertTrue(np.all(results[steps] <= 1.0))

    def test_zero_steps_returns_the_initial_distribution(self):
        result = distribution_after_steps(0)
        np.testing.assert_allclose(result, (1 / 3, 1 / 3, 1 / 3), atol=1e-12)

    def test_negative_or_non_integer_step_count_is_rejected(self):
        for invalid_steps in (-1, 1.5, True):
            with self.subTest(steps=invalid_steps):
                with self.assertRaisesRegex(ValueError, "entero no negativo"):
                    distribution_after_steps(invalid_steps)


class InitialStateSelectionTests(SimpleTestCase):
    def test_each_weather_state_creates_a_concentrated_distribution(self):
        for index, state in enumerate(WEATHER_STATES):
            with self.subTest(state=state):
                expected = np.zeros(3)
                expected[index] = 1.0
                np.testing.assert_array_equal(initial_distribution_for_state(state), expected)

    def test_unknown_state_is_rejected(self):
        for state in ("Tormenta", None, "soleado"):
            with self.subTest(state=state):
                with self.assertRaisesRegex(ValueError, "Estado inicial no válido"):
                    initial_distribution_for_state(state)


class SequenceSimulationTests(SimpleTestCase):
    def test_sequence_includes_initial_state_and_requested_transitions(self):
        sequence = simulate_sequence(4, seed=123)
        self.assertEqual(len(sequence), 5)
        self.assertIn(sequence[0], WEATHER_STATES)
        self.assertTrue(all(state in WEATHER_STATES for state in sequence))

    def test_same_seed_and_parameters_reproduce_the_sequence(self):
        self.assertEqual(simulate_sequence(20, seed=456), simulate_sequence(20, seed=456))

    def test_minimum_and_maximum_lengths_are_accepted(self):
        self.assertEqual(len(simulate_sequence(MIN_SIMULATION_STEPS, seed=1)), 2)
        self.assertEqual(len(simulate_sequence(MAX_SIMULATION_STEPS, seed=1)), 101)

    def test_invalid_lengths_are_rejected(self):
        for steps in (0, 101, 1.5, True, "5"):
            with self.subTest(steps=steps):
                with self.assertRaisesRegex(ValueError, "entero entre 1 y 100"):
                    simulate_sequence(steps, seed=1)

    def test_zero_probability_transitions_never_occur(self):
        identity = np.eye(3)
        sequence = simulate_sequence(
            20,
            initial_distribution=(1.0, 0.0, 0.0),
            transition_matrix=identity,
            seed=99,
        )
        self.assertEqual(sequence, ("Soleado",) * 21)


class SimulationViewTests(SimpleTestCase):
    def test_get_renders_educational_model_and_default_results(self):
        response = self.client.get(reverse("simulador:index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            tuple(row["steps"] for row in response.context["result_rows"]),
            (1, 3, 5, 10),
        )
        html = response.content.decode()
        for state in WEATHER_STATES:
            self.assertIn(state, html)
        self.assertIn("hipotéticos", html)
        self.assertIn("pronóstico oficial", html)
        self.assertIn("Distribución uniforme predeterminada", html)
        self.assertIn("aria-labelledby", html)
        self.assertIn("&pi;(0)", html)
        self.assertIn("Matriz de transici", html)

    def test_valid_post_uses_selected_state_length_and_renders_sequence(self):
        response = self.client.post(
            reverse("simulador:index"),
            {"initial_state": "Nublado", "steps": "3", "seed": "42"},
        )
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()
        self.assertIn("Secuencia simulada", html)
        self.assertIn("4 estados", html)
        self.assertIn("Nublado", html)

    def test_invalid_post_exposes_form_errors(self):
        response = self.client.post(
            reverse("simulador:index"),
            {"initial_state": "Tormenta", "steps": "101", "seed": ""},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("errorlist", response.content.decode())
        self.assertNotIn("Secuencia simulada", response.content.decode())

    def test_stylesheet_is_referenced(self):
        response = self.client.get(reverse("simulador:index"))
        self.assertContains(response, "simulador/styles.css")

    def test_chart_data_matches_the_table_results(self):
        response = self.client.get(reverse("simulador:index"))
        chart_data = response.context["chart_data"]
        self.assertEqual(chart_data["labels"], ["Paso 1", "Paso 3", "Paso 5", "Paso 10"])
        for index, state in enumerate(WEATHER_STATES):
            with self.subTest(state=state):
                self.assertEqual(chart_data["datasets"][index]["label"], state)
                expected = [float(response.context["result_rows"][i]["probabilities"][index]) for i in range(4)]
                np.testing.assert_allclose(chart_data["datasets"][index]["data"], expected)

    def test_chart_has_text_alternative_and_static_scripts(self):
        response = self.client.get(reverse("simulador:index"))
        html = response.content.decode()
        self.assertIn('role="img"', html)
        self.assertIn('aria-describedby="chart-description"', html)
        self.assertIn("alternativa textual completa", html)
        self.assertIn("simulador/vendor/chart.umd.min.js", html)
        self.assertIn("simulador/results-chart.js", html)

    def test_invalid_input_errors_are_explained_in_spanish_with_allowed_range(self):
        response = self.client.post(
            reverse("simulador:index"),
            {"initial_state": "Tormenta", "steps": "101", "seed": ""},
        )
        html = response.content.decode()
        self.assertIn("Seleccione un estado inicial válido.", html)
        self.assertIn("La longitud debe estar entre 1 y 100 pasos.", html)
