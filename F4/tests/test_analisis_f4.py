"""Pruebas unitarias para el módulo de análisis de Fase 4."""

import tempfile
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import pytest
from src.analisis_f4 import (
    guardar_figura,
    intervalo_wilson,
    matriz_cruce_tipo_sector,
    resumen_montos_y_plazos,
    tasa_desercion_por_grupo,
)


def test_intervalo_wilson_calculo_manual():
    """Valida que 10 éxitos de 100 (10%) quede entre 5.5% y 17.4%."""
    inf, sup = intervalo_wilson(exitos=10, total=100)
    
    assert 0.0 < inf < sup < 1.0
    assert pytest.approx(inf, abs=0.01) == 0.055
    assert pytest.approx(sup, abs=0.01) == 0.174


def test_intervalo_wilson_casos_limite():
    """Verifica el comportamiento cuando hay 0% o 100% de éxitos."""
    inf_cero, sup_cero = intervalo_wilson(exitos=0, total=50)
    assert inf_cero == 0.0
    assert sup_cero > 0.0

    inf_todos, sup_todos = intervalo_wilson(exitos=50, total=50)
    assert inf_todos < 1.0
    assert sup_todos == 1.0


def test_intervalo_wilson_excepciones():
    """Verifica que el código rechace datos imposibles (total 0 o negativos)."""
    with pytest.raises(ValueError):
        intervalo_wilson(exitos=5, total=0)

    with pytest.raises(ValueError):
        intervalo_wilson(exitos=15, total=10)


def test_tasa_desercion_tabla_pequena_a_mano():
    """Prueba pedida por el docente: tabla pequeña de 6 filas construida a mano."""
    df_pequeno = pd.DataFrame({
        "sector": ["Salud", "Salud", "Salud", "Salud", "Educación", "Educación"],
        "EsDesierta": [0, 1, 0, 0, 1, 0]
    })

    resumen = tasa_desercion_por_grupo(
        df_pequeno,
        columna_grupo="sector",
        objetivo="EsDesierta",
        min_casos_estables=3
    )

    assert len(resumen) == 2
    assert resumen["total_n"].sum() == 6
    assert resumen["desiertas_casos"].sum() == 2

    fila_edu = resumen[resumen["sector"] == "Educación"].iloc[0]
    assert fila_edu["total_n"] == 2
    assert fila_edu["tasa_desierta"] == 0.50
    assert fila_edu["baja_frecuencia"] == True

    fila_salud = resumen[resumen["sector"] == "Salud"].iloc[0]
    assert fila_salud["total_n"] == 4
    assert fila_salud["tasa_desierta"] == 0.25
    assert fila_salud["baja_frecuencia"] == False


def test_resumen_montos_y_plazos():
    """Verifica que el cálculo de medianas e IQR funcione correctamente."""
    df_dummy = pd.DataFrame({
        "EsDesierta": [0, 0, 0, 1, 1, 1],
        "DiasPublicacionCierre": [10, 12, 14, 10, 20, 30],
        "MontoEstimadoNumerico": [100.0, 200.0, 300.0, 500.0, 1000.0, 1500.0]
    })

    res = resumen_montos_y_plazos(df_dummy)

    assert len(res) == 2
    assert "Plazo_Mediana_Dias" in res.columns
    assert "Monto_IQR_CLP" in res.columns

    fila_adj = res[res["Estado"] == "Adjudicada"].iloc[0]
    assert fila_adj["Plazo_Mediana_Dias"] == 12
    assert fila_adj["Monto_Mediana_CLP"] == 200.0

    fila_des = res[res["Estado"] == "Desierta"].iloc[0]
    assert fila_des["Plazo_Mediana_Dias"] == 20
    assert fila_des["Monto_Mediana_CLP"] == 1000.0


def test_matriz_cruce_tipo_sector():
    """Verifica que se generen las dos matrices (tasas y conteos)."""
    df_cruce = pd.DataFrame({
        "Tipo": ["L1", "L1", "LP", "LP"],
        "sector": ["Salud", "Salud", "Educación", "Educación"],
        "EsDesierta": [0, 1, 1, 1]
    })

    tasas, conteos = matriz_cruce_tipo_sector(df_cruce)

    assert tasas.shape == (2, 2)
    assert conteos.shape == (2, 2)
    # L1 en Salud tiene 1 de 2 = 50%
    assert tasas.loc["L1", "Salud"] == 50.0
    assert conteos.loc["L1", "Salud"] == 2


def test_guardar_figura():
    """Valida que la función guarde un archivo PNG a 200 dpi."""
    fig, ax = plt.subplots()
    ax.plot([1, 2], [3, 4])

    with tempfile.TemporaryDirectory() as tmpdir:
        ruta = guardar_figura(fig, tmpdir, "grafico_prueba", dpi=200)
        assert Path(ruta).exists()
        assert Path(ruta).suffix == ".png"

    plt.close(fig)