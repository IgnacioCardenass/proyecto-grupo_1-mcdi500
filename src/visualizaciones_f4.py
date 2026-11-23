"""Visualizaciones analíticas de licitaciones públicas - Fase 4."""

import matplotlib.pyplot as plt
import numpy as np


def graficar_tasas_por_grupo(resumen, columna, titulo, tasa_global):
    """Grafica tasas por grupo con intervalos de Wilson al 95%."""

    datos = resumen.sort_values("tasa_desierta").copy()

    tasas = datos["tasa_desierta"].to_numpy() * 100
    inferiores = datos["ic_inferior"].to_numpy() * 100
    superiores = datos["ic_superior"].to_numpy() * 100

    errores = np.vstack([
        tasas - inferiores,
        superiores - tasas
    ])

    posiciones = np.arange(len(datos))

    altura = max(5, len(datos) * 0.48)
    fig, ax = plt.subplots(figsize=(11, altura))

    colores = [
        "#AC212E" if tasa > tasa_global * 100 else "#9FB6C8"
        for tasa in tasas
    ]

    ax.barh(
        posiciones,
        tasas,
        color=colores,
        height=0.65
    )

    ax.errorbar(
        tasas,
        posiciones,
        xerr=errores,
        fmt="none",
        ecolor="#263238",
        capsize=3,
        linewidth=1.2
    )

    ax.axvline(
        tasa_global * 100,
        color="#263238",
        linestyle="--",
        linewidth=1.5,
        label=f"Tasa global: {tasa_global * 100:.2f}%"
    )

    etiquetas = [
        f"{grupo} (n={n:,})"
        for grupo, n in zip(
            datos[columna],
            datos["total_n"]
        )
    ]

    ax.set_yticks(posiciones)
    ax.set_yticklabels(etiquetas, fontsize=9)

    ax.set_xlabel("Licitaciones desiertas (%)")
    ax.set_ylabel("")
    ax.set_title(titulo, fontweight="bold", pad=15)

    ax.set_xlim(0, max(30, superiores.max() * 1.15))
    ax.legend(loc="lower right")
    ax.grid(axis="x", alpha=0.2)
    ax.set_axisbelow(True)

    for posicion, tasa, pocos in zip(
        posiciones,
        tasas,
        datos["baja_frecuencia"]
    ):
        etiqueta = f"{tasa:.1f}%"
        if pocos:
            etiqueta += " *"

        ax.text(
            tasa + 0.35,
            posicion + 0.15,
            etiqueta,
            fontsize=8
        )

    fig.text(
        0.01,
        0.005,
        "Fuente: elaboración propia con datos de "
        "ChileCompra / Mercado Público. "
        "Intervalos de Wilson al 95%. "
        "* Menos de 30 licitaciones.",
        fontsize=8
    )

    fig.tight_layout(rect=[0, 0.04, 1, 1])

    return fig

    

def graficar_montos_por_estado(datos):
    """Compara los montos CLP por estado con escala logarítmica."""

    # Validar las columnas necesarias
    columnas = [
        "EsDesierta",
        "MontoEstimadoNumerico",
        "Moneda Adquisicion"
    ]

    for columna in columnas:
        if columna not in datos.columns:
            raise KeyError(f"Falta la columna: {columna}")

    # Evitar mezclar monedas diferentes
    if not datos["Moneda Adquisicion"].eq("Peso Chileno").all():
        raise ValueError("El gráfico requiere exclusivamente montos CLP.")

    montos = datos["MontoEstimadoNumerico"]

    if montos.isna().any() or (montos <= 0).any():
        raise ValueError("Los montos deben ser positivos y no nulos.")

    # Separar según el estado de la licitación
    adjudicadas = datos.loc[
        datos["EsDesierta"] == 0,
        "MontoEstimadoNumerico"
    ]

    desiertas = datos.loc[
        datos["EsDesierta"] == 1,
        "MontoEstimadoNumerico"
    ]

    if adjudicadas.empty or desiertas.empty:
        raise ValueError("Se necesitan ambos estados para comparar.")

    # Crear gráfico de caja
    fig, ax = plt.subplots(figsize=(10, 5))

    cajas = ax.boxplot(
        [adjudicadas, desiertas],
        vert=False,
        tick_labels=["Adjudicadas", "Desiertas"],
        patch_artist=True,
        showfliers=False,
        medianprops={"color": "#263238", "linewidth": 2}
    )

    # Colores para distinguir ambos estados
    colores = ["#9FB6C8", "#AC212E"]

    for caja, color in zip(cajas["boxes"], colores):
        caja.set_facecolor(color)
        caja.set_edgecolor("#263238")

    # Utilizar escala logarítmica
    ax.set_xscale("log")

    ax.set_title(
        "Las licitaciones desiertas presentan menor "
        "mediana de monto estimado",
        fontweight="bold",
        pad=15
    )

    ax.set_xlabel("Monto estimado (CLP, escala logarítmica)")
    ax.set_ylabel("Estado de la licitación")

    ax.grid(axis="x", alpha=0.25)
    ax.set_axisbelow(True)

    # Fuente y aclaraciones metodológicas
    fig.text(
        0.01,
        0.02,
        "Fuente: elaboración propia con datos de "
        "ChileCompra / Mercado Público. "
        "Solo montos positivos en CLP. "
        "Valores atípicos no dibujados.",
        fontsize=8
    )

    fig.tight_layout(rect=[0, 0.07, 1, 1])

    return fig

def graficar_mapa_tipo_sector(datos, min_casos=30):
    """Grafica tasas de deserción por tipo y sector."""

    import seaborn as sns
    from src.analisis_f4 import matriz_cruce_tipo_sector

    # Crear copia para conservar el conjunto original
    df = datos.copy()

    # Mantener las categorías sin información
    for columna in ["Tipo", "sector"]:
        df[columna] = (
            df[columna]
            .astype("string")
            .fillna("No informado")
            .str.strip()
            .replace("", "No informado")
        )

    # Reutilizar el cálculo estadístico de F4
    tasas, conteos = matriz_cruce_tipo_sector(df)

    # Ordenar según cantidad de licitaciones
    orden_tipos = (
        conteos.sum(axis=1)
        .sort_values(ascending=False)
        .index
    )

    orden_sectores = (
        conteos.sum(axis=0)
        .sort_values(ascending=False)
        .index
    )

    tasas = tasas.loc[orden_tipos, orden_sectores]
    conteos = conteos.loc[orden_tipos, orden_sectores]

    # Preparar etiquetas: porcentaje y tamaño del grupo
    etiquetas = np.empty(tasas.shape, dtype=object)

    for i in range(tasas.shape[0]):
        for j in range(tasas.shape[1]):

            n = conteos.iloc[i, j]
            tasa = tasas.iloc[i, j]

            if n == 0 or np.isnan(tasa):
                etiquetas[i, j] = ""
            else:
                marca = "*" if n < min_casos else ""

                etiquetas[i, j] = (
                    f"{tasa:.1f}%\n"
                    f"n={n}{marca}"
                )

    # Construir mapa de calor
    fig, ax = plt.subplots(figsize=(15, 9))

    sns.heatmap(
        tasas,
        annot=etiquetas,
        fmt="",
        cmap="YlOrRd",
        vmin=0,
        vmax=100,
        mask=conteos.eq(0),
        linewidths=0.5,
        annot_kws={"fontsize": 7},
        cbar_kws={
            "label": "Licitaciones desiertas (%)"
        },
        ax=ax
    )

    ax.set_title(
        "Tasa de deserción según tipo de licitación y sector",
        fontweight="bold",
        pad=15
    )

    ax.set_xlabel("Sector")
    ax.set_ylabel("Tipo de licitación")

    ax.tick_params(axis="x", rotation=35)
    ax.tick_params(axis="y", rotation=0)

    # Fuente y advertencia sobre grupos pequeños
    fig.text(
        0.01,
        0.01,
        "Fuente: elaboración propia con datos de "
        "ChileCompra / Mercado Público. "
        "* Combinación con menos de 30 licitaciones. "
        "Celdas vacías: sin registros.",
        fontsize=8
    )

    fig.tight_layout(rect=[0, 0.05, 1, 1])

    return fig