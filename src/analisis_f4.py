"""Módulo de análisis y soporte estadístico para la Fase 4.

MCDI500 · Programación para la Ciencia de Datos
Grupo N° 1
"""

import math
from pathlib import Path
import pandas as pd


def intervalo_wilson(exitos, total, z=1.96):
    """Calcula el intervalo de confianza de Wilson al 95% para una proporción."""
    if total <= 0:
        raise ValueError("El total debe ser mayor a 0.")
    if exitos < 0 or exitos > total:
        raise ValueError("Los éxitos deben estar entre 0 y el total.")

    p = exitos / total
    denominador = 1.0 + (z**2) / total
    centro = (p + (z**2) / (2.0 * total)) / denominador
    margen = (
        z * math.sqrt((p * (1.0 - p) / total) + ((z**2) / (4.0 * (total**2))))
    ) / denominador

    inferior = 0.0 if exitos == 0 else max(0.0, centro - margen)
    superior = 1.0 if exitos == total else min(1.0, centro + margen)

    return inferior, superior


def tasa_desercion_por_grupo(df, columna_grupo, objetivo="EsDesierta", min_casos_estables=30, z=1.96):
    """Calcula la tasa de desiertas por grupo y marca las categorías con baja frecuencia."""
    if columna_grupo not in df.columns:
        raise KeyError(f"La columna '{columna_grupo}' no existe en el DataFrame.")
    if objetivo not in df.columns:
        raise KeyError(f"La columna objetivo '{objetivo}' no existe en el DataFrame.")

    filas = []
    for valor, sub in df.groupby(columna_grupo, observed=True):
        n = len(sub)
        casos = int(sub[objetivo].sum())
        inf, sup = intervalo_wilson(casos, n, z=z)

        filas.append({
            columna_grupo: valor,
            "total_n": n,
            "desiertas_casos": casos,
            "tasa_desierta": casos / n if n > 0 else 0.0,
            "ic_inferior": inf,
            "ic_superior": sup,
            "baja_frecuencia": bool(n < min_casos_estables)
        })

    resumen = pd.DataFrame(filas)
    if not resumen.empty:
        resumen = resumen.sort_values("tasa_desierta", ascending=False).reset_index(drop=True)
    return resumen


def resumen_montos_y_plazos(df):
    """Calcula medianas y rangos intercuartílicos (IQR) para plazos y montos por estado."""
    resumen = []
    for estado, sub in df.groupby("EsDesierta", observed=True):
        nombre_estado = "Desierta" if estado == 1 else "Adjudicada"

        # Plazos en días
        q25_p = sub["DiasPublicacionCierre"].quantile(0.25)
        med_p = sub["DiasPublicacionCierre"].median()
        q75_p = sub["DiasPublicacionCierre"].quantile(0.75)
        iqr_p = q75_p - q25_p

        # Montos en pesos
        q25_m = sub["MontoEstimadoNumerico"].quantile(0.25)
        med_m = sub["MontoEstimadoNumerico"].median()
        q75_m = sub["MontoEstimadoNumerico"].quantile(0.75)
        iqr_m = q75_m - q25_m

        resumen.append({
            "Estado": nombre_estado,
            "Total_n": len(sub),
            "Plazo_Mediana_Dias": med_p,
            "Plazo_IQR_Dias": iqr_p,
            "Monto_Mediana_CLP": med_m,
            "Monto_IQR_CLP": iqr_m
        })

    return pd.DataFrame(resumen)


def matriz_cruce_tipo_sector(df, col_tipo="Tipo", col_sector="sector", objetivo="EsDesierta"):
    """Genera las tablas de tasas (%) y conteos (n) para el mapa de calor Tipo x Sector."""
    tasas = df.pivot_table(
        index=col_tipo,
        columns=col_sector,
        values=objetivo,
        aggfunc="mean",
        observed=True
    ) * 100

    conteos = df.pivot_table(
        index=col_tipo,
        columns=col_sector,
        values=objetivo,
        aggfunc="count",
        observed=True
    ).fillna(0).astype(int)

    return tasas, conteos


def guardar_figura(figura, carpeta, nombre, dpi=200):
    """Guarda la figura en PNG a 200 dpi con fondo blanco y sin recortes."""
    dir_salida = Path(carpeta)
    dir_salida.mkdir(parents=True, exist_ok=True)
    nombre_archivo = f"{nombre}.png" if not nombre.endswith(".png") else nombre
    ruta = dir_salida / nombre_archivo

    figura.savefig(ruta, dpi=dpi, bbox_inches="tight", facecolor="white", edgecolor="none")
    return ruta