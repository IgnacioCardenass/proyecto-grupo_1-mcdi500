
# Registro de cambios y mejoras — Proyecto MCDI500

## Propósito

Este documento registra la evolución técnica del proyecto
"Análisis de factores asociados a licitaciones públicas
desiertas en Chile", desarrollado durante las fases F1–F4.

Los cambios se vinculan con commits verificables para
mantener trazabilidad de las decisiones, contribuciones
y mejoras implementadas.

Repositorio:
https://github.com/IgnacioCardenass/proyecto-grupo_1-mcdi500

## Fase 1 — Definición del proyecto

### 2026-11-04 — Definición del problema
- Se incorporaron las preguntas de investigación,
  objetivos, limitaciones y alcance del proyecto.
- Justificación: delimitar el estudio a las licitaciones
  del primer semestre de 2026 y evitar conclusiones
  causales que los datos no permiten.
- Commit: `6e19e6c`

### 2026-11-10 — Revisión de F1
- Se incorporó una versión corregida siguiendo la pauta.
- Justificación: mejorar la correspondencia entre
  problemática, objetivos y alcance.
- Commit: `7dda4d6`

## Fase 2 — Preparación y transformación de datos

### 2026-11-17 — Modularización del procesamiento
- Se separaron funciones reutilizables para cargar,
  limpiar y validar datos.
- Justificación: reducir la dependencia del notebook
  y facilitar pruebas y mantenimiento.
- Commit: `e8dc2f3`

### 2026-11-18 — Validación de resultados
- Se incorporaron comprobaciones y exportación
  de resultados del procesamiento.
- Justificación: reforzar integridad, trazabilidad
  y reproducibilidad del conjunto preparado.
- Commit: `44df778`

### 2026-11-18 — Corrección de montos
- Se mejoró la normalización de valores numéricos
  con separadores de miles y decimales.
- Se agregaron pruebas relacionadas.
- Justificación: evitar interpretaciones incorrectas
  de valores monetarios.
- Commits: `77b72c6`, `78bf0b8`

### 2026-11-19 — Datos procesados versionados
- Se incorporaron archivos procesados en
  `F2/data/processed/`.
- Justificación: permitir ejecutar las fases posteriores
  sin reconstruir F2 para cada comprobación.
- Commit: `ccf593f`

## Fase 3 — Arquitectura, eficiencia y pruebas

### 2026-11-16 — Arquitectura y Factory
- Se desarrolló la creación de transformadores
  mediante el patrón Factory.
- Justificación: separar la creación de objetos
  de su utilización en el pipeline.
- Commit: `305048e`

### 2026-11-18 — Comparación de eficiencia
- Se amplió la comparación de implementaciones
  `apply()` y vectorizada a tamaños crecientes.
- Se incorporaron mediciones de tiempo y memoria.
- Justificación: respaldar la elección de implementación
  con evidencia reproducible.
- Commit: `5efadea`

### 2026-11-18 — Validación de arquitectura
- Se documentaron los componentes modulares y
  se incorporaron comprobaciones de herencia,
  Factory, interfaz y composición.
- Justificación: facilitar la comprensión y
  verificación de la arquitectura.
- Commit: `92c2952`

### 2026-11-19 — Pruebas automatizadas adicionales
- Se agregaron pruebas de Factory y Pipeline.
- Se actualizaron las dependencias declaradas.
- Justificación: ampliar la verificación de casos
  normales y excepciones.
- Commit: `9f9fc60`

### 2026-11-19 — Documentación técnica
- Se amplió el README con arquitectura, ejecución,
  pruebas y eficiencia de F3.
- Justificación: facilitar la reproducción y
  comprensión del proyecto.
- Commit: `946783f`

## Fase 4 — Visualización y comunicación

### 2026-11-19 — Visualizaciones finales
- Se creó `F4/F4_Analisis_Visualizaciones.ipynb`.
- Se elaboraron tres visualizaciones:
  1. Distribución de adjudicadas y desiertas.
  2. Tasas de licitaciones desiertas por tipo.
  3. Comparación de plazos de publicación y cierre.
- Se agregaron validaciones, interpretaciones y
  limitaciones de los resultados.
- Se exportaron tres gráficos PNG.
- Justificación: comunicar hallazgos que respondan
  a los objetivos definidos en F1.
- Commit: `760a3aa`

## Verificaciones y limitaciones

- Se comprobó localmente la ejecución de F3
  desde un clon limpio, con sus dependencias.
- Se comprobó localmente la ejecución completa
  del notebook de visualizaciones de F4.
- Las asociaciones observadas no implican causalidad.
- La procedencia oficial del archivo original
  requiere mantener documentación verificable.

## Mejoras pendientes de registrar

- Integración del trabajo de F4 en `main`.
- Revisión y consolidación del informe final.
- Comprobación final del repositorio integrado.
- Presentación audiovisual del equipo.

Estas actividades solo se marcarán como completadas
cuando exista evidencia de ejecución o entrega.
