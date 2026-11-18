import pandas as pd
import pytest
from transformadores import ImputadorMediana


def _tabla():
    """Tabla pequeña hecha a mano: la mediana de 100 y 300 es 200."""
    return pd.DataFrame({
        "Moneda Adquisicion": ["Peso Chileno"] * 3,
        "Monto": [100.0, 300.0, None],
    })


# CASO NORMAL: datos típicos, resultado esperado conocido
def test_caso_normal_imputa_con_la_mediana():
    imp = ImputadorMediana("Monto").ajustar(_tabla())
    salida = imp.transformar(_tabla())
    assert salida["MontoEstimadoImputado"].tolist() == [100.0, 300.0, 200.0]
    assert salida["MontoFueImputado"].tolist() == [0, 0, 1]


# CASO LÍMITE: columna sin faltantes, no debe imputar nada
def test_caso_limite_sin_faltantes():
    datos = _tabla().fillna(500.0)
    imp = ImputadorMediana("Monto").ajustar(datos)
    assert imp.transformar(datos)["MontoFueImputado"].sum() == 0


# EXCEPCIONES: deben producir un error claro
def test_excepcion_columna_inexistente():
    with pytest.raises(KeyError):
        ImputadorMediana("NoExiste").ajustar(_tabla())


def test_excepcion_transformar_sin_ajustar():
    with pytest.raises(RuntimeError):
        ImputadorMediana("Monto").transformar(_tabla())


def test_excepcion_faltante_en_otra_moneda():
    datos = _tabla()
    datos.loc[2, "Moneda Adquisicion"] = "Dólar"
    imp = ImputadorMediana("Monto").ajustar(_tabla())
    with pytest.raises(ValueError):
        imp.transformar(datos)