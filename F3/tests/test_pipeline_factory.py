
import pandas as pd
import pytest

from fabrica import crear_transformador
from pipeline import Pipeline
from transformadores import ImputadorMediana, CodificadorNominal


def datos_prueba():
    """Datos pequeños con resultados conocidos."""
    return pd.DataFrame({
        "MontoEstimadoNumerico": [100.0, 300.0, None],
        "Moneda Adquisicion": ["Peso Chileno"] * 3,
        "sector": ["Salud", "Educacion", "Salud"]
    })


# PRUEBA 1: Factory crea un imputador
def test_factory_crea_imputador():
    objeto = crear_transformador(
        "monto", "MontoEstimadoNumerico"
    )
    assert isinstance(objeto, ImputadorMediana)


# PRUEBA 2: Factory crea un codificador
def test_factory_crea_codificador():
    objeto = crear_transformador(
        "categorica", "sector"
    )
    assert isinstance(objeto, CodificadorNominal)


# PRUEBA 3: Factory rechaza tipos desconocidos
def test_factory_tipo_invalido():
    with pytest.raises(ValueError):
        crear_transformador("desconocido", "sector")


# PRUEBA 4: Pipeline completo
def test_pipeline_resultado_correcto():
    datos = datos_prueba()

    pasos = [
        crear_transformador("monto", "MontoEstimadoNumerico"),
        crear_transformador("categorica", "sector")
    ]

    pipeline = Pipeline(pasos)
    resultado = pipeline.ajustar(datos).transformar(datos)

    assert resultado["MontoEstimadoImputado"].tolist() == [
        100.0, 300.0, 200.0
    ]
    assert resultado["MontoFueImputado"].tolist() == [0, 0, 1]
    assert resultado["sector_Salud"].tolist() == [1, 0, 1]
    assert "sector" not in resultado.columns

    # Comprobar que no se modificó la entrada
    assert "sector" in datos.columns
    assert pd.isna(datos.loc[2, "MontoEstimadoNumerico"])


# PRUEBA 5: Pipeline sin ajustar
def test_pipeline_sin_ajustar():
    pipeline = Pipeline([
        crear_transformador("categorica", "sector")
    ])

    with pytest.raises(RuntimeError):
        pipeline.transformar(datos_prueba())


# PRUEBA 6: Categoría desconocida
def test_pipeline_categoria_desconocida():
    pipeline = Pipeline([
        crear_transformador("categorica", "sector")
    ])

    pipeline.ajustar(datos_prueba())

    datos_nuevos = pd.DataFrame({
        "sector": ["Mineria"]
    })

    with pytest.raises(ValueError):
        pipeline.transformar(datos_nuevos)
