"""Medición de eficiencia computacional para la Fase 4.

Compara el cálculo de tasas por grupo mediante:
1. Bucle iterativo tradicional (for).
2. Agrupación vectorizada con pandas (groupby).

Mide tiempo (milisegundos) y memoria (MB) para 5 tamaños de muestra
(1.000 a 40.000 registros), con formato numérico chileno.

MCDI500 · Grupo N° 1
"""

import sys
import time
import tracemalloc
from pathlib import Path
import pandas as pd
import numpy as np

# Asegurar que encuentre los módulos
raiz = Path(__file__).resolve().parent.parent
if str(raiz) not in sys.path:
    sys.path.insert(0, str(raiz))


def tasa_con_bucle(df, col_grupo="sector", col_obj="EsDesierta"):
    """Calcula tasas por grupo usando un bucle tradicional."""
    sectores = df[col_grupo].unique()
    resultados = {}
    for s in sectores:
        sub = df[df[col_grupo] == s]
        n = len(sub)
        desiertas = sub[col_obj].sum()
        resultados[s] = desiertas / n if n > 0 else 0.0
    return pd.Series(resultados, name="tasa_bucle")


def tasa_con_groupby(df, col_grupo="sector", col_obj="EsDesierta"):
    """Calcula tasas por grupo usando el groupby optimizado de pandas."""
    return df.groupby(col_grupo, observed=True)[col_obj].mean().rename("tasa_groupby")


def formato_chileno(numero, decimales=2):
    """Convierte un número flotante al formato chileno: 1.234,56."""
    texto = f"{numero:,.{decimales}f}"
    # Invertir comas y puntos
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def ejecutar_benchmark():
    ruta_datos = raiz / "F2" / "data" / "processed" / "licitaciones_filtradas_provisional.csv.gz"
    if not ruta_datos.exists():
        print(f"Error: no se encontró {ruta_datos}")
        return

    print("Cargando dataset analítico...")
    df = pd.read_csv(ruta_datos)[["sector", "EsDesierta"]]
    print(f"Dataset cargado con éxito: {len(df):,} registros.\n")

    # 1. Comprobar equivalencia exacta de resultados antes de medir
    res_bucle = tasa_con_bucle(df.head(100)).sort_index()
    res_group = tasa_con_groupby(df.head(100)).sort_index()
    np.testing.assert_allclose(res_bucle.values, res_group.values)
    print("✅ Verificación técnica: Ambas implementaciones producen exactamente el mismo resultado.\n")

    tamanos = [1000, 5000, 10000, 20000, 40000]
    repeticiones = 5
    filas_tabla = []

    print(f"Ejecutando mediciones ({repeticiones} repeticiones reales por tamaño)...")
    print("-" * 75)

    for n in tamanos:
        muestra = df.iloc[:n].copy()

        # Medición Bucle
        tiempos_bucle = []
        tracemalloc.start()
        for _ in range(repeticiones):
            t0 = time.perf_counter()
            _ = tasa_con_bucle(muestra)
            tiempos_bucle.append((time.perf_counter() - t0) * 1000)  # ms
        _, pico_mem_bucle = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # Medición Groupby
        tiempos_group = []
        tracemalloc.start()
        for _ in range(repeticiones):
            t0 = time.perf_counter()
            _ = tasa_con_groupby(muestra)
            tiempos_group.append((time.perf_counter() - t0) * 1000)  # ms
        _, pico_mem_group = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        t_med_bucle = np.median(tiempos_bucle)
        mem_mb_bucle = pico_mem_bucle / (1024 * 1024)

        t_med_group = np.median(tiempos_group)
        mem_mb_group = pico_mem_group / (1024 * 1024)

        factor_aceleracion = t_med_bucle / t_med_group if t_med_group > 0 else 1.0

        filas_tabla.append({
            "Tamaño (N)": f"{n:,}".replace(",", "."),
            "Tiempo Bucle (ms)": formato_chileno(t_med_bucle, 2),
            "Memoria Bucle (MB)": formato_chileno(mem_mb_bucle, 3),
            "Tiempo Groupby (ms)": formato_chileno(t_med_group, 2),
            "Memoria Groupby (MB)": formato_chileno(mem_mb_group, 3),
            "Aceleración": f"{formato_chileno(factor_aceleracion, 1)}x"
        })

    tabla_resultados = pd.DataFrame(filas_tabla)
    print("\nTABLA DE RESULTADOS DE EFICIENCIA (FORMATO CHILENO PARA EL INFORME):\n")
    print(tabla_resultados.to_string(index=False))
    print("\nNota: Tiempos reportan la mediana de 5 repeticiones reales. Memoria representa pico de tracemalloc.")


if __name__ == "__main__":
    ejecutar_benchmark()