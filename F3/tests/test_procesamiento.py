import pandas as pd
import pytest
from src.procesamiento import normalizar_montos


# CASO PROFESOR: prueba con tabla pequeña construida a mano (Paso 9 de correcciones)
def test_normalizar_montos_caso_profesor():
    prueba = pd.Series(["1.234,5", "2.000", None])
    resultado = normalizar_montos(prueba)
    assert resultado.iloc[0] == 1234.5
    assert pd.isna(resultado.iloc[2])


# CASO NORMAL: notación científica con coma frecuente en ChileCompra
def test_normalizar_montos_notacion_cientifica():
    prueba = pd.Series(["1,04e+09", "6,7e+07"])
    resultado = normalizar_montos(prueba)
    assert resultado.iloc[0] == 1.04e9
    assert resultado.iloc[1] == 6.7e7


# EXCEPCIÓN: debe fallar con TypeError si no se pasa una Serie de pandas
def test_normalizar_montos_tipo_invalido():
    with pytest.raises(TypeError):
        normalizar_montos([100, 200])