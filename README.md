Pendiente: incorporar los enlaces específicos de descarga del dataset y la bibliografía efectivamente utilizada en el informe y el curso.

Proyecto Grupo 1 — MCDI500

Magíster en Ciencia de Datos e Inteligencia Artificial

1. Descripción del proyecto

Este proyecto estudia las licitaciones públicas registradas en Chile durante el primer semestre de 2026.

El objetivo es explorar las características de las licitaciones declaradas desiertas y compararlas con aquellas adjudicadas, utilizando técnicas de programación, limpieza de datos y análisis exploratorio.

Pregunta de investigación

¿Qué diferencias se observan entre las licitaciones desiertas y adjudicadas durante el primer semestre de 2026, considerando sus características y variables disponibles?

El análisis es descriptivo y no pretende establecer relaciones causales.

2. Datos utilizados

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

3. Estructura del proyecto

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

4. Requisitos del entorno

Entorno utilizado para el desarrollo:

Python 3.13

pandas 3.1.0

NumPy 2.5.4

scikit-learn 1.9.1

Matplotlib 3.11.2

JupyterLab 4.6.4

gdown 6.5.1

Las dependencias principales están declaradas en requirements.txt.

5. Instalación

Clonar el repositorio:

git clone https://github.com/IgnacioCardenass/proyecto-grupo_1-mcdi500.git
cd proyecto-grupo_1-mcdi500

Crear y activar un entorno virtual en Windows:



Crear y activar un entorno virtual en Windows:

python -m venv .venv
.venv\Scripts\activate



Crear y activar un entorno virtual en Windows:

python -m venv .venv
.venv\Scripts\activate

Instalar las dependencias:

python -m pip install -r requirements.txt

Verificar compatibilidad:

python -m pip check

Para reproducir específicamente los cambios de modularización que todavía no estén integrados a main, utilizar la rama correspondiente:

git switch sergio/correcciones-reproducibilidad

La instalación desde un clon y entorno limpios está pendiente de validación final.

6. Orden de ejecución

F1 — Definición del problema: revisar el planteamiento, alcance y objetivos del proyecto.

F2 — Obtención y preparación: ejecutar F2/notebooks/Exploración_de_datos.ipynb desde el inicio.

F3 — Núcleo algorítmico: ejecutar una vez verificadas sus dependencias y su integración con los datos preparados.

Para F2, seleccionar el intérprete del entorno configurado y utilizar Restart Kernel → Run All.

El archivo original debe encontrarse en la ruta especificada en la sección 2.

7. Procesamiento de Fase 2

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

8. Archivos generados

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

9. Integrantes y responsabilidades

Pendiente de confirmar los nombres completos y responsabilidades de los cuatro integrantes.


10. Limitaciones y trabajo pendiente



11. Referencias

Mercado Público

ChileCompra
