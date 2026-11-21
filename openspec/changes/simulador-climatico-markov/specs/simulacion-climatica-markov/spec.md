# Spec Delta

## Purpose

Define el comportamiento verificable de un simulador educativo de cadenas de Markov para analizar estados climáticos abstractos y visualizar sus distribuciones y secuencias.

## ADDED Requirements

### Requirement: Modelo de tres estados y matriz de transición
El sistema SHALL representar exactamente los estados Soleado, Nublado y Lluvioso en una cadena de Markov de tiempo discreto. La matriz configurable SHALL tener filas para el estado actual y columnas para el siguiente estado, en ese orden. Cada fila SHALL contener probabilidades entre 0 y 1 cuya suma sea 1 dentro de una tolerancia documentada. La matriz predeterminada SHALL identificarse como hipotética y didáctica, nunca como dato meteorológico real.

#### Scenario: Presentación del modelo válido
- **WHEN** el usuario consulta el modelo climático
- **THEN** el sistema muestra los tres estados, la orientación de la matriz, los valores predeterminados `[[0.70, 0.20, 0.10], [0.30, 0.40, 0.30], [0.20, 0.30, 0.50]]` en ese orden, y su carácter hipotético

#### Scenario: Rechazo de matriz inválida
- **WHEN** se intenta calcular con una matriz que no es 3 × 3, tiene valores fuera del intervalo [0, 1] o alguna fila no suma 1 dentro de la tolerancia
- **THEN** el sistema no presenta el resultado como válido y explica qué condición debe corregirse

### Requirement: Distribución inicial
El sistema SHALL representar la distribución inicial como tres probabilidades asociadas en orden a Soleado, Nublado y Lluvioso, cada una entre 0 y 1 y con suma igual a 1 dentro de la tolerancia documentada. La distribución predeterminada SHALL ser uniforme: π(0) = [1/3, 1/3, 1/3]. El sistema SHALL permitir seleccionar un estado inicial único, equivalente a una distribución concentrada con probabilidad 1 en ese estado, y consultar la distribución configurada.

#### Scenario: Distribución uniforme predeterminada
- **WHEN** el usuario abre el simulador sin seleccionar otro estado inicial
- **THEN** el sistema usa y muestra π(0) = [1/3, 1/3, 1/3]

#### Scenario: Selección de estado inicial
- **WHEN** el usuario selecciona uno de los tres estados como inicio
- **THEN** el sistema configura la distribución inicial con probabilidad 1 para ese estado y 0 para los otros dos

#### Scenario: Distribución inicial inválida
- **WHEN** se proporciona una distribución con dimensión incorrecta, valores fuera de [0, 1] o suma distinta de 1 fuera de tolerancia
- **THEN** el sistema rechaza el cálculo y comunica el error de validación

### Requirement: Cálculo de probabilidades por pasos
El sistema SHALL calcular la distribución después de n pasos mediante π(n) = π(0) × Pⁿ para n igual a 1, 3, 5 y 10. Cada distribución presentada SHALL mantener tres valores válidos y sumar aproximadamente 1.

#### Scenario: Consulta de pasos requeridos
- **WHEN** el usuario solicita los resultados del modelo
- **THEN** el sistema presenta las probabilidades para los pasos 1, 3, 5 y 10, identificadas por estado y por número de paso

#### Scenario: Conservación de probabilidad
- **WHEN** se calcula una distribución para cualquiera de los pasos requeridos a partir de entradas válidas
- **THEN** el resultado contiene probabilidades no negativas, no mayores que 1 salvo diferencias de redondeo, y su suma es aproximadamente 1

### Requirement: Visualización educativa de resultados
El sistema SHALL mostrar la matriz, la distribución inicial y los resultados calculados en una tabla y una gráfica legible construida con Chart.js, con etiquetas de estado y paso. SHALL incluir una explicación breve de cómo leerlos y dejar claro que representan un modelo educativo, no un pronóstico oficial.

#### Scenario: Lectura de resultados
- **WHEN** se muestran resultados calculados
- **THEN** el usuario puede relacionar cada valor tabular y gráfico con un estado climático y un número de pasos

#### Scenario: Aviso sobre alcance del modelo
- **WHEN** el usuario consulta la interfaz del simulador
- **THEN** el sistema indica que los parámetros son hipotéticos y que el modelo educativo no constituye un pronóstico meteorológico real

### Requirement: Simulación de secuencias
El sistema SHALL permitir que el usuario configure una longitud entera de simulación entre 1 y 100 pasos y generar una secuencia de estados desde la distribución inicial aplicando las probabilidades de transición correspondientes al estado actual. La secuencia SHALL incluir el estado inicial y los estados sucesivos generados. Cualquier fuente de aleatoriedad configurable para reproducibilidad SHALL conservar el comportamiento probabilístico definido.

#### Scenario: Generación de secuencia válida
- **WHEN** el usuario solicita una simulación con longitud entre 1 y 100 pasos
- **THEN** el sistema devuelve el estado inicial y los estados sucesivos, eligiendo cada siguiente estado conforme a la fila de transición del estado actual

#### Scenario: Rechazo de longitud inválida
- **WHEN** se solicita una secuencia con menos de 1 o más de 100 pasos, o con una longitud no entera
- **THEN** el sistema rechaza la solicitud e indica el intervalo permitido

#### Scenario: Secuencia reproducible
- **WHEN** se repite una simulación con los mismos parámetros y una semilla explícita
- **THEN** el sistema produce la misma secuencia

### Requirement: Validación matemática automatizada
El sistema SHALL contar con pruebas automatizadas usando Django Test Framework para dimensiones, rangos y sumas de la matriz y distribución inicial, resultados para los pasos requeridos, conservación de probabilidad y coherencia de las secuencias. Los resultados de cálculo SHALL contrastarse con referencias matemáticas independientes.

#### Scenario: Verificación contra referencia
- **WHEN** se ejecutan las pruebas del cálculo matricial con casos de referencia definidos
- **THEN** los resultados coinciden con los valores esperados dentro de una tolerancia explícita y documentada

#### Scenario: Verificación de simulación
- **WHEN** se ejecutan las pruebas de generación de secuencias con parámetros y semilla conocidos
- **THEN** cada transición observada en la secuencia tiene probabilidad positiva en la matriz correspondiente

### Requirement: Parámetros declarados como hipotéticos
El sistema SHALL identificar como hipotéticos los valores de transición predeterminados y evitar atribuirlos a observaciones meteorológicas reales.

#### Scenario: Uso de matriz predeterminada
- **WHEN** la interfaz presenta la matriz de transición inicial
- **THEN** la identifica visiblemente como hipotética y explica que los valores se eligieron para fines académicos

