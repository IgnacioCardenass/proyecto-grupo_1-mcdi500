import pytest
from carga import cargar_datos


def test_excepcion_archivo_inexistente():
    with pytest.raises(FileNotFoundError):
        cargar_datos("no_existe.csv")