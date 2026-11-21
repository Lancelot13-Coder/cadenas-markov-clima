# Design

## Context

El repositorio contiene el plan de ingeniería y la configuración OpenSpec, pero no contiene una aplicación Django, código fuente ni especificaciones base. El plan establece Python/Django, HTML/CSS/JavaScript y deja NumPy, Chart.js y el marco de pruebas sujetos a evaluación. Las decisiones para este cambio confirman NumPy, Chart.js y Django Test Framework. Los requisitos funcionales se detallan en `specs/simulacion-climatica-markov/spec.md`.

## Goals / Non-Goals

**Goals:** proponer una estructura sencilla que separe presentación, cálculo y validación; mantener los valores matemáticos configurables y justificables; permitir revisar resultados con pruebas independientes.

**Non-Goals:** desplegar o integrar el sistema en esta etapa de planificación; conectarlo con servicios meteorológicos; atribuir realismo empírico a parámetros hipotéticos.

## Decisions

- **Django como aplicación web.** Organizar el proyecto en una aplicación dedicada al simulador, con vistas delgadas para recibir opciones y construir la respuesta, plantillas para la página educativa y recursos estáticos para estilos y gráficas. Se descarta añadir una API independiente porque el alcance descrito es una interfaz web académica y no requiere consumidores externos.
- **Lógica matemática aislada de las vistas.** Colocar validación, propagación de distribuciones y generación de secuencias en un módulo de dominio sin dependencias de Django. Usar NumPy para operaciones matriciales y propagación de π(n) = π(0) × Pⁿ; mantener las comprobaciones de dominio explícitas para dimensiones, rangos y normalización.
- **Convención y matriz inicial.** Mantener filas como estado actual, columnas como siguiente estado y la distribución como vector fila. La matriz configurable predeterminada, en el orden Soleado, Nublado y Lluvioso, es P = [[0.70, 0.20, 0.10], [0.30, 0.40, 0.30], [0.20, 0.30, 0.50]]. Cada fila suma 1. Es hipotética y didáctica: una probabilidad mayor de permanecer en Soleado (0.70) o Lluvioso (0.50) ilustra persistencia de estados; las probabilidades de cambio permiten observar transiciones entre los tres estados; la fila de Nublado distribuye probabilidad de forma equilibrada (0.30, 0.40, 0.30) para servir como caso intermedio. Estos valores no se infieren de clima observado y se rotularán como hipotéticos en la interfaz. Los cálculos se verificarán con referencias independientes y tolerancia numérica explícita.
- **Distribución inicial.** Usar como predeterminada π(0) = [1/3, 1/3, 1/3]. La selección de un estado individual forma el vector concentrado con probabilidad 1 para ese estado. Validar que cualquier configuración conserve tres valores en [0, 1] cuya suma sea 1 dentro de tolerancia.
- **Simulación de secuencias.** Recibir una longitud entera configurable entre 1 y 100 pasos; la respuesta contiene el estado inicial y luego un estado por paso, de modo que el total de estados es longitud + 1. Muestrear el estado inicial desde π(0) y cada transición desde la fila del estado actual. Aceptar semilla opcional para reproducibilidad. Rechazar valores no enteros o fuera de rango.
- **Visualización en la interfaz.** Presentar tabla accesible como forma primaria de lectura y gráfica complementaria con Chart.js. Incluir etiquetas claras, alternativa textual y aviso de que la matriz es hipotética y el simulador no es un pronóstico. No se requiere persistencia ni base de datos para el alcance descrito.
- **Pruebas automatizadas.** Usar Django Test Framework. Probar las funciones matemáticas sin servidor y las vistas mediante el cliente de pruebas de Django. Fijar resultados de referencia calculados independientemente, verificar tolerancias, límites de longitud, validaciones y secuencias reproducibles.

## Risks / Trade-offs

- [Parámetros hipotéticos confundidos con pronóstico] → rotular la matriz y explicar su propósito académico.
- [Error de orientación entre vector fila/columna] → documentar la convención y verificar resultados contra cálculos independientes.
- [Redondeo produce sumas visuales distintas de 1] → conservar precisión en cálculo y redondear solo al presentar; documentar tolerancia de validación.
- [Gráficas inaccesibles] → conservar la tabla completa, etiquetas y alternativa textual.
- [Pruebas estadísticas inestables para frecuencias aleatorias] → probar transiciones imposibles con semillas controladas y cubrir el muestreo sin umbrales probabilísticos frágiles.

## Migration Plan

No aplica migración: no se observan aplicación existente, datos persistidos ni usuarios que deban trasladarse. La implementación posterior creará el proyecto Django y sus componentes como parte de una etapa aprobada separadamente.
