# Propuesta: Simulador Climático mediante Cadenas de Markov

## Why

El plan de ingeniería plantea una aplicación educativa para hacer comprensible cómo evoluciona una distribución climática bajo probabilidades de transición. Esta propuesta convierte ese objetivo en requisitos revisables para calcular y simular un modelo de Markov discreto, sin presentarlo como pronóstico meteorológico real.

## What Changes

- Incorporar los estados Soleado, Nublado y Lluvioso, con una matriz de transición hipotética inicial de 3 × 3 cuyas filas representan el estado actual y columnas el siguiente, en ese orden: `[[0.70, 0.20, 0.10], [0.30, 0.40, 0.30], [0.20, 0.30, 0.50]]`. Cada fila suma 1. La matriz se identificará como exclusivamente didáctica, no derivada de observaciones meteorológicas, y sus valores serán configurables.
- Usar como distribución inicial predeterminada la uniforme π(0) = [1/3, 1/3, 1/3], además de permitir seleccionar un estado único, equivalente a asignarle probabilidad 1.
- Calcular las distribuciones para 1, 3, 5 y 10 pasos mediante π(n) = π(0) × Pⁿ y mostrar los resultados en tablas y gráficas educativas.
- Permitir generar secuencias cuyo número de pasos configure el usuario entre 1 y 100. La salida incluye el estado inicial y cada estado sucesivo.
- Validar dimensiones, rangos y sumas de probabilidades; comprobar resultados mediante pruebas automatizadas y referencias matemáticas independientes.
- Proponer una interfaz web clara que explique estados, matriz, distribución, pasos y límites del modelo.

## Alcance y exclusiones

El alcance contempla una aplicación web académica en Python y Django, con presentación HTML, CSS y JavaScript, cálculo probabilístico mediante NumPy, gráficas con Chart.js y pruebas automatizadas con Django Test Framework. La interfaz permitirá consultar o seleccionar el estado inicial, configurar la longitud de secuencia y explorar los pasos indicados.

Quedan fuera los pronósticos operativos, la integración de fuentes o datos meteorológicos reales, la calibración con observaciones, la geolocalización, los modelos de más de tres estados y la pretensión de representar el clima real. El sistema ilustra el comportamiento del modelo bajo parámetros declarados.

## Capabilities

### New Capabilities

- `simulacion-climatica-markov`: modelado de los tres estados, distribución inicial, matriz de transición, cálculo por pasos, simulación de secuencias, validación y presentación educativa.

### Modified Capabilities

Ninguna. El inventario del proyecto no contiene especificaciones existentes.

## Impact

Se prevé una aplicación Django organizada entre vistas, lógica matemática, plantillas y recursos de interfaz. NumPy realizará las operaciones matriciales, Chart.js presentará las gráficas y Django Test Framework cubrirá pruebas unitarias y de integración. No se han observado aplicaciones ni dependencias de ejecución existentes en el repositorio; la implementación posterior partirá de un proyecto aún por crear. No se modificarán README.md ni PLAN_INGENIERIA.md como parte de este cambio.
