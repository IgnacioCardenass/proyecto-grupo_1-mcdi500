Pendiente: incorporar los enlaces específicos de descarga del dataset y la bibliografía efectivamente utilizada en el informe y el curso.

Proyecto Grupo 1 — MCDI500

Magíster en Ciencia de Datos e Inteligencia Artificial

1. ## Descripción del proyecto

Este proyecto estudia las licitaciones públicas registradas en Chile durante el primer semestre de 2026.

El objetivo es explorar las características de las licitaciones declaradas desiertas y compararlas con aquellas adjudicadas, utilizando técnicas de programación, limpieza de datos y análisis exploratorio.

Pregunta de investigación

¿Qué diferencias se observan entre las licitaciones desiertas y adjudicadas durante el primer semestre de 2026, considerando sus características y variables disponibles?

El análisis es descriptivo y no pretende establecer relaciones causales.

2. ## Datos utilizados

Se trabaja con un archivo ZIP que contiene registros de licitaciones correspondientes al período enero-junio de 2026.

El conjunto original puede contener varias filas asociadas a un mismo CodigoExterno, por lo que el procesamiento consolida la información para obtener una observación por licitación.

Procedencia de los datos: pendiente de documentar mediante enlaces oficiales de ChileCompra, de acuerdo con la retroalimentación docente.

Obtención provisional del archivo

Por el tamaño del dataset, este no está incluido en el repositorio.

Mientras se resuelve la documentación de la descarga oficial, se utiliza provisionalmente el archivo compartido por el equipo:

https://drive.google.com/file/d/1rlzN_3OmS7v3z6Yaiw5jbf3qjrGtuFI1/view?usp=sharing

Guardar el archivo descargado en:

F1/data/raw/licitaciones_enero_junio_2026.zip

No es necesario descomprimirlo manualmente.

Pendiente: registrar enlaces oficiales, fecha de descarga y hash SHA-256 del archivo. La disponibilidad del enlace provisional no constituye evidencia suficiente de procedencia oficial.

3. ## Estructura del proyecto

proyecto-grupo_1-mcdi500/
├── F1/
│   └── notebooks/
│       └── F1_Definición.ipynb
├── F2/
│   ├── data/
│   │   └── processed/
│   └── notebooks/
│       └── Exploración_de_datos.ipynb
├── F3/
│   ├── notebooks/
│   │   └── S2_F3_NucleoAlgoritmico.ipynb
│   └── src/
├── F4/
├── src/
│   └── procesamiento.py
├── requirements.txt
└── README.md

La carpeta src de la raíz contiene funciones compartidas de procesamiento. La carpeta F3/src contiene módulos específicos de la Fase 3.

Los archivos procesados se generan durante la ejecución y pueden no estar incluidos en GitHub.

4. ## Requisitos del entorno

Entorno utilizado para el desarrollo:

Python 3.13

pandas 3.1.0

NumPy 2.5.4

scikit-learn 1.9.1

Matplotlib 3.11.2

JupyterLab 4.6.4

gdown 6.5.1

Las dependencias principales están declaradas en requirements.txt.

5. ## Instalación

# Clonar el repositorio:

git clone https://github.com/IgnacioCardenass/proyecto-grupo_1-mcdi500.git
cd proyecto-grupo_1-mcdi500

# Crear y activar un entorno virtual en Windows:

python -m venv .venv
.venv\Scripts\activate

# Crear y activar un entorno virtual en Windows:

python -m venv .venv
.venv\Scripts\activate

# Instalar las dependencias:

python -m pip install -r requirements.txt

# Verificar compatibilidad:

python -m pip check

6. ## Orden de ejecución

F1 — Definición del problema: revisar el planteamiento, alcance y objetivos del proyecto.

F2 — Obtención y preparación: ejecutar F2/notebooks/Exploración_de_datos.ipynb desde el inicio.

F3 — Núcleo algorítmico: ejecutar una vez verificadas sus dependencias y su integración con los datos preparados.

Para F2, seleccionar el intérprete del entorno configurado y utilizar Restart Kernel → Run All.

El archivo original debe encontrarse en la ruta especificada en la sección 2.

7. ## Procesamiento de Fase 2

La Fase 2 incluye:

Validación estructural del CSV comprimido.

Lectura de datos por bloques.

Consolidación de registros por identificador de licitación.

Diagnóstico y tratamiento de valores faltantes.

Normalización de montos y fechas.

Revisión de diferencias entre registros de una misma licitación.

Codificación de variables categóricas.

Escalamiento demostrativo de variables numéricas.

Separación de registros que requieren revisión.

Exportación y validación de resultados.

Funciones reutilizables

El archivo src/procesamiento.py contiene:

normalizar_montos() Convertir montos a valores numéricos

consolidar_por_licitacion() Obtener una fila por código de licitación

comparar_imputaciones() Comparar estrategias para tratar valores faltantes

leer_bloques_zip() Leer el dataset comprimido por bloques

validar_estructura_zip() Separar filas con estructura incorrecta

separar_registros_sospechosos() Apartar licitaciones que requieren revisión

8. ## Archivos generados

La ejecución de F2 genera archivos en:

F2/data/processed/

Entre ellos:

licitaciones_estructura_valida.zip

licitaciones_analiticas.csv.gz

licitaciones_filtradas_provisional.csv.gz

matriz_codificada.csv.gz

matriz_filtrada_provisional.csv.gz

matriz_escalada_demostracion.csv.gz

registros_pendientes_revision.csv

Los archivos filtrados provisionales excluyen los registros apartados por las reglas de revisión implementadas.

Las matrices escaladas son demostraciones de preprocesamiento. Para evaluar modelos predictivos, las transformaciones que aprenden parámetros deben ajustarse únicamente con los datos de entrenamiento.

9. ## Fase 3 — Núcleo algorítmico

Objetivo

La Fase 3 tiene como objetivo reorganizar el procesamiento desarrollado en F2 mediante programación estructurada y orientada a objetos, aplicando modularidad, reutilización de código, validación automatizada y análisis de eficiencia computacional.

Se utiliza el mismo conjunto de licitaciones de Fase 2, sin modificar el problema de investigación.

# Estructura de Fase 3

F3/
├── docs/
│   └── bitacora.md
├── notebooks/
│   ├── Revision_imputacion.ipynb
│   └── S2_F3_NucleoAlgoritmico.ipynb
├── src/
│   ├── carga.py
│   ├── preparacion.py
│   ├── transformadores.py
│   ├── pipeline.py
│   ├── fabrica.py
│   └── medicion.py
└── tests/
    ├── conftest.py
    ├── test_carga.py
    ├── test_transformadores.py
    └── test_pipeline_factory.py

# Arquitectura del sistema

carga.py: Carga y comprobación de archivos de datos

preparacion.py: Construcción de variables derivadas y variable objetivo

transformadores.py: Clases de transformación, imputación y codificación

pipeline.py: Ejecución secuencial de transformaciones

fabrica.py: Creación de objetos mediante el patrón Factory

medicion.py: Medición y comparación de eficiencia

La arquitectura se basa en una clase Transformador, de la cual heredan ImputadorMediana y CodificadorNominal.

El objeto Pipeline coordina las transformaciones mediante una interfaz común de ajuste y transformación.

Esta organización permite separar responsabilidades y reutilizar componentes sin concentrar todo el procesamiento dentro del notebook.

# Principios de programación orientada a objetos

Se aplican los siguientes principios:

Abstracción: interfaz común de los transformadores.

Encapsulamiento: almacenamiento interno de parámetros y estado de ajuste.

Herencia: clases especializadas que derivan de Transformador.

Polimorfismo: ejecución de transformadores distintos mediante los mismos métodos.

Composición: el pipeline contiene y coordina una secuencia de transformadores.

Se utiliza el patrón Factory para centralizar la creación de transformadores según su propósito.

El proyecto emplea división funcional e iteración. No se incorpora recursividad artificial porque el pipeline procesa pasos de profundidad conocida.

# Datos de entrada de F3

Antes de ejecutar F3, debe haberse ejecutado F2.

El notebook principal utiliza los archivos generados en:

F2/data/processed/

Los archivos principales son:

licitaciones_filtradas_provisional.csv.gz

matriz_filtrada_provisional.csv.gz

registros_pendientes_revision.csv

resumen_final_f2.csv

Estos resultados son provisionales y conservan la trazabilidad de los registros apartados durante F2.

# Validación automatizada

La validación técnica utiliza pytest.

Desde la raíz del repositorio, ejecutar:

python -m pytest F3/tests -v

Las pruebas incluyen carga de archivos, imputación, manejo de excepciones, creación de transformadores con Factory y comportamiento del Pipeline.

En el entorno local MCDI500 se ejecutaron satisfactoriamente 12 pruebas, sin fallos. Este resultado debe reproducirse en los demás entornos de trabajo y después de integrar todas las ramas.

La dependencia pytest debe encontrarse declarada con versión fija en requirements.txt.

# Eficiencia y optimización

Se compararon dos implementaciones para construir la variable EsDesierta:

1. Series.apply().

2. Operaciones vectorizadas de pandas.

Se utilizaron muestras de 1.000, 5.000, 10.000, 20.000 y 40.000 registros.

Las mediciones consideran tiempo de ejecución mediante timeit y memoria asignada registrada mediante tracemalloc.

En una ejecución local, para 40.000 registros se obtuvieron los siguientes resultados:

apply(): 14.012 ms, 3.13 MB

Vectorizada: 1.258 ms, 0.46 MB

La versión vectorizada presentó una ventaja temporal aproximada de 11.1 veces para ese tamaño.

Ambas implementaciones presentan un comportamiento compatible con complejidad temporal O(n) y generan una salida de tamaño proporcional a n.

La diferencia de rendimiento se relaciona principalmente con la eficiencia de las operaciones internas utilizadas por cada implementación.

Las cifras son mediciones empíricas del entorno evaluado, no garantías universales de rendimiento. tracemalloc no representa necesariamente el consumo total de memoria del proceso.


# Documentación y trazabilidad

Los principales documentos de referencia son:

F3/notebooks/S2_F3_NucleoAlgoritmico.ipynb: implementación, comparaciones y validaciones.

F3/notebooks/Revision_imputacion.ipynb: revisión de faltantes por resultado de licitación.

F3/docs/bitacora.md: registro de decisiones técnicas.

F3/tests/: pruebas automatizadas.

El historial de GitHub permite identificar las contribuciones técnicas individuales y las integraciones realizadas mediante Pull Requests.

# Limitaciones

La equivalencia con F2 se verifica utilizando los datos de referencia preparados para esta etapa.

Las transformaciones que aprenden parámetros deberán ajustarse exclusivamente sobre los datos de entrenamiento cuando se realice una evaluación predictiva, para evitar fuga de información.

Queda pendiente confirmar y documentar definitivamente la procedencia oficial del conjunto de datos, así como realizar la prueba final desde un clon limpio con todas las ramas integradas.

10. ## Integrantes y responsabilidades

Pendiente de confirmar los nombres completos y responsabilidades de los cuatro integrantes.


11. ## Fase 4 — Visualización y comunicación de resultados

# Objetivo

La Fase 4 integra los resultados de las fases anteriores
para caracterizar y comparar las licitaciones públicas
adjudicadas y desiertas del primer semestre de 2026.

Se desarrollan tres visualizaciones analíticas relacionadas
con los objetivos establecidos en F1, utilizando los datos
preparados y validados durante F2 y F3.

# Archivos principales

```text
F4/
├── F4_Analisis_Visualizaciones.ipynb
└── resultados/
    ├── grafico_1_estados.png
    ├── grafico_2_tipos.png
    └── grafico_3_plazos.png
```

# Datos utilizados

El notebook utiliza:

`F2/data/processed/licitaciones_filtradas_provisional.csv.gz`

Se emplea el conjunto interpretable, que conserva nombres
de categorías y unidades originales, en lugar de graficar
directamente las variables codificadas de la matriz One-Hot.

La base contiene 41.607 licitaciones y 18 columnas.

Las observaciones corresponden al conjunto analítico
conservado tras los filtros de F2. Los resultados no
representan necesariamente todas las licitaciones públicas
del país.

# Visualizaciones desarrolladas

**Gráfico 1: distribución por estado**

De 41.607 licitaciones analizadas:
- 35.622 fueron adjudicadas (85,6 %).
- 5.985 fueron declaradas desiertas (14,4 %).

La figura caracteriza la distribución general de los
resultados observados.

**Gráfico 2: porcentaje de desiertas por tipo**

Se calculó la tasa de licitaciones desiertas dentro de
cada tipo de procedimiento.

Entre los tipos con al menos 30 registros:
- E2: 40,54 % (74 licitaciones).
- B2: 32,43 % (222 licitaciones).
- CO: 29,97 % (654 licitaciones).
- LP: 12,29 % (8.218 licitaciones).

Los tipos con menos de 30 registros se excluyeron solo
de la figura principal, no del conjunto de datos.

La comparación es descriptiva y no permite atribuir
causalidad al tipo de procedimiento.

**Gráfico 3: plazos de publicación y cierre**

Se comparó la duración de las licitaciones adjudicadas
y desiertas utilizando diagramas de caja y puntos de
una muestra reproducible.

Ambos grupos presentan una mediana de 12 días.

Las medias observadas fueron:
- Adjudicadas: 13,98 días.
- Desiertas: 14,60 días.

Las distribuciones presentan una superposición importante.
Por ello, estas diferencias descriptivas no permiten
afirmar que el plazo determine el resultado del proceso.

# Ejecución

1. Clonar el repositorio.
2. Crear y activar un entorno Python compatible.
3. Instalar las dependencias:

   `python -m pip install -r requirements.txt`

4. Abrir el notebook:

   `F4/F4_Analisis_Visualizaciones.ipynb`

5. Seleccionar el kernel del entorno instalado.
6. Ejecutar `Restart Kernel → Run All`.

El notebook localiza automáticamente la raíz del proyecto,
carga los datos procesados de F2 y ejecuta las validaciones
y visualizaciones.

# Resultados exportados

Durante la ejecución se generan tres imágenes PNG en:

`F4/resultados/`

Los gráficos se exportan a 300 DPI para facilitar su uso
en el informe y en la presentación audiovisual.

# Validaciones y reproducibilidad

Se comprueba:
- La existencia de las columnas necesarias.
- La coherencia de la variable objetivo.
- La correspondencia entre totales y agrupaciones.
- La consistencia de los plazos de publicación.
- La existencia de los tres archivos PNG generados.

El notebook de F4 se ejecutó localmente desde el inicio
sin errores. La comprobación final debe repetirse sobre
un clon limpio de la versión integrada en `main`.

# Limitaciones

- El estudio comprende enero-junio de 2026.
- Solo se analizan los estados y registros conservados
  tras el preprocesamiento de F2.
- No se establecen relaciones causales.
- Las comparaciones entre tipos no controlan
  simultáneamente otras características.
- La procedencia y trazabilidad de la descarga original
  de ChileCompra deben documentarse definitivamente.

# Trazabilidad

El archivo `changelog.md` registra la evolución del proyecto
entre F1 y F4, incluyendo fechas, mejoras y referencias
a commits verificables.

El historial de GitHub documenta las contribuciones
individuales y su integración mediante ramas y Pull Requests.



12. ## Limitaciones y trabajo pendiente

13. ## Validación de reproducibilidad

El 17 de noviembre de 2026 se realizó una prueba de reproducción local del proyecto utilizando un clon independiente del repositorio y un entorno Conda nuevo denominado `MCDI500_PRUEBA`, configurado con Python 3.13.

Se instalaron las dependencias declaradas en `requirements.txt` y se comprobó su consistencia mediante `python -m pip check`, sin detectar conflictos.

Para la ejecución se utilizó una copia local del dataset original, ubicada en `F1/data/raw/licitaciones_enero_junio_2026.zip`, debido a que la procedencia y el procedimiento de descarga oficial se encuentran pendientes de confirmación.

Se verificó la ejecución del notebook F2 desde el entorno independiente. La prueba incluye la generación de archivos procesados en `F2/data/processed/`.

**Resultados de referencia de F2:**
- 853.499 registros estructuralmente válidos.
- 46.567 licitaciones únicas.
- 42 registros apartados para revisión.
- 41.607 licitaciones conservadas provisionalmente.

La reproducción en un entorno nuevo permite comprobar la instalación y ejecución local del proyecto, pero no sustituye la validación de procedencia oficial ni la prueba adicional en otro computador.

14. ## Referencias

Mercado Público

ChileCompra
