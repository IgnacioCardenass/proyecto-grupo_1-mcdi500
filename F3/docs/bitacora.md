# Bitácora de decisiones, Fase 3

## Revisión de la imputación del monto

- Problema detectado: el monto se compara entre licitaciones desiertas y adjudicadas. Imputarlo con la mediana podría diluir esa diferencia si los faltantes se concentraran en un grupo.
- Alternativa considerada: excluir del análisis de monto las licitaciones sin dato.
- Decisión: mantener la imputación con la mediana en pesos chilenos.
- Efecto en cifras: faltan 7 montos de 41.607 (0,017 %). Adjudicadas: 6 de 35.622. Desiertas: 1 de 5.985. El porcentaje es el mismo en ambos grupos (0,017 %).
- Evidencia: notebook F3/notebooks/Revision_imputacion.ipynb

## Pruebas automáticas

- Problema detectado: no había pruebas para la imputación ni para la carga de datos.
- Alternativa considerada: comprobar los resultados solo mirando el notebook.
- Decisión: pruebas con pytest sobre tablas pequeñas hechas a mano (caso normal, caso límite y excepciones).
- Efecto: 6 pruebas aprobadas con pytest F3/tests -v.
- Evidencia: carpeta F3/tests