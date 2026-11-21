# Simulador climático con cadenas de Markov

Aplicación web educativa para explorar cómo evoluciona una distribución de probabilidades sobre tres estados abstractos: Soleado, Nublado y Lluvioso. El simulador no es un pronóstico meteorológico.

## Requisitos

- Python 3.14 o compatible con las versiones declaradas en `requirements.txt`.
- Node.js y npm para instalar las dependencias de interfaz.

## Instalación en Windows PowerShell

Desde la raíz de este repositorio:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
npm ci
```

Las dependencias de Python quedan aisladas en `.venv`; no se instalan globalmente. Chart.js se declara en `package.json` y su distribución web y licencia se incluyen en los recursos estáticos del proyecto.

## Ejecución

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py runserver
```

Abre `http://127.0.0.1:8000/`. No se requiere base de datos ni ejecutar migraciones para el simulador actual.

## Uso y modelo matemático

- El modelo tiene exactamente tres estados, en este orden: Soleado, Nublado y Lluvioso.
- La matriz predeterminada está en `simulador/constants.py`. Sus filas representan el estado actual y sus columnas el siguiente estado:

  ```text
  [[0.70, 0.20, 0.10],
   [0.30, 0.40, 0.30],
   [0.20, 0.30, 0.50]]
  ```

- La matriz es hipotética y configurable en el código. Puede cambiarse `DEFAULT_TRANSITION_MATRIX` conservando dimensiones 3 × 3, valores entre 0 y 1 y suma 1 por fila. Las funciones de cálculo y simulación también aceptan una matriz explícita.
- Didácticamente, la probabilidad más alta de permanecer en Soleado (0.70) y Lluvioso (0.50) ilustra persistencia; las transiciones entre estados permiten observar cambios; la fila equilibrada de Nublado ofrece un caso intermedio. Los valores no provienen de observaciones meteorológicas.
- La distribución inicial predeterminada es uniforme, π(0) = [1/3, 1/3, 1/3]. También se puede seleccionar un estado único, con probabilidad 1 para ese estado.
- La página calcula π(n) = π(0) × Pⁿ para 1, 3, 5 y 10 pasos. La tabla conserva los valores de referencia y acompaña la gráfica Chart.js.
- La longitud de una secuencia se configura entre 1 y 100 pasos. La secuencia muestra el estado inicial y cada transición posterior; la longitud total mostrada es, por tanto, n + 1. La semilla opcional permite repetir una simulación.
- Las sumas de probabilidades se validan con tolerancia absoluta `1e-9`.

## Pruebas

```powershell
.\.venv\Scripts\python.exe manage.py test
node --check simulador/static/simulador/results-chart.js
```

Las pruebas Django cubren valores predeterminados, validaciones matemáticas, resultados comparados con referencias independientes, selección inicial, secuencias reproducibles y respuestas de la interfaz. La tabla HTML es la alternativa textual completa de la gráfica.

## Estructura principal

- `config/`: configuración y rutas del proyecto Django.
- `simulador/constants.py`: estados y parámetros predeterminados.
- `simulador/validation.py`: validación de probabilidades.
- `simulador/calculations.py`: propagación de distribuciones con NumPy.
- `simulador/simulation.py`: generación de secuencias.
- `simulador/forms.py`, `views.py` y `templates/`: interacción y presentación.
- `simulador/static/simulador/`: estilos, gráfica y distribución de Chart.js.

## Alcance

Los parámetros son hipotéticos y educativos. No se consultan fuentes meteorológicas ni se generan pronósticos oficiales; los resultados solo describen el modelo configurado.
