# Tasks

## 1. Estructura y dependencias

- [x] 1.1 Crear el proyecto Django y la aplicación del simulador con la separación de módulos, plantillas y estáticos descrita en el diseño; verificar que Django reconoce el proyecto y la aplicación.
- [x] 1.2 Declarar NumPy, Chart.js y Django Test Framework según corresponda a sus mecanismos de instalación; verificar la configuración de dependencias y que el framework de pruebas de Django está disponible.

## 2. Modelo matemático y validaciones

- [x] 2.1 Implementar constantes configurables para los estados, la matriz P hipotética `[[0.70, 0.20, 0.10], [0.30, 0.40, 0.30], [0.20, 0.30, 0.50]]` y la distribución uniforme predeterminada [1/3, 1/3, 1/3]; verificar valores, orden de estados y sumas de filas con pruebas Django.
- [x] 2.2 Implementar validaciones de dimensión, rango y normalización de matriz y distribución inicial con tolerancia documentada; verificar casos válidos y errores para cada condición inválida.
- [x] 2.3 Implementar el cálculo π(n) = π(0) × Pⁿ con NumPy para n = 1, 3, 5 y 10; verificar resultados contra referencias independientes y conservación de probabilidad dentro de tolerancia.
- [x] 2.4 Implementar la conversión de un estado seleccionado a distribución concentrada y la validación de selección; verificar los tres estados y las entradas inválidas.
- [x] 2.5 Implementar generación reproducible de secuencias con semilla opcional y longitud de 1 a 100 pasos, incluyendo el estado inicial; verificar secuencia de longitud n + 1, reproducción con semilla, transiciones permitidas y rechazo de longitudes no enteras o fuera de rango.

## 3. Interfaz educativa

- [x] 3.1 Implementar vistas Django y formularios de entrada para consultar resultados y configurar estado inicial y longitud de secuencia; verificar respuestas correctas y mensajes de validación con el cliente de pruebas de Django.
- [x] 3.2 Crear la plantilla y estilos para presentar estados, matriz, distribución inicial, resultados de pasos 1, 3, 5 y 10 y secuencia generada; verificar que cada dato tenga etiquetas comprensibles y se anuncie el carácter hipotético del modelo.
- [x] 3.3 Integrar las gráficas Chart.js con la tabla como alternativa accesible, etiquetas de estado y de pasos; verificar que la gráfica use los mismos resultados que la tabla y que exista una alternativa textual.

## 4. Documentación e integración

- [x] 4.1 Documentar instalación, ejecución, configuración de parámetros, justificación didáctica de la matriz, límites de longitud, ejecución de pruebas y la advertencia de que el modelo no es un pronóstico; verificar que las instrucciones se puedan seguir en una instalación limpia.
- [x] 4.2 Ejecutar la suite Django y la revisión funcional integrada de cálculo, validaciones, interfaz y secuencias; verificar que todas las pruebas pasen y que los resultados se mantengan coherentes entre presentación y lógica.
