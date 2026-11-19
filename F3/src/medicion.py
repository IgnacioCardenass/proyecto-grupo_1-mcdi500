import tracemalloc

def version_con_apply(datos):
    """Crea EsDesierta utilizando apply()."""

    estado_desierta = "Desierta (o art. 3 ó 9 Ley 19.886)"

    resultado = datos["Estado"].apply(
        lambda estado: int(estado == estado_desierta)
    )

    return resultado.rename("EsDesierta")

def version_vectorizada(datos):
    """Crea EsDesierta utilizando operaciones vectorizadas."""

    estado_desierta = "Desierta (o art. 3 ó 9 Ley 19.886)"

    resultado = (
        datos["Estado"] == estado_desierta
    ).astype(int)

    return resultado.rename("EsDesierta")

def medir_memoria(funcion, datos):
    """Mide el máximo de memoria asignada por Python."""

    tracemalloc.start()

    resultado = funcion(datos)

    _, memoria_maxima = tracemalloc.get_traced_memory()

    tracemalloc.stop()

    return memoria_maxima / 1024 / 1024


def comparar_rendimiento_por_tamano(
    datos,
    tamanos=(1000, 5000, 10000, 20000, 40000),
    repeticiones=5
):
    """
    Compara apply y vectorización con tamaños crecientes.

    Mide tiempo y memoria máxima para ambas versiones.
    Comprueba que sus resultados sean equivalentes.
    """
    import timeit
    import pandas as pd

    if repeticiones < 1:
        raise ValueError(
            "Las repeticiones deben ser al menos 1"
        )

    resultados = []

    for n in tamanos:
        if n <= 0 or n > len(datos):
            raise ValueError(
                f"Tamaño inválido: {n}"
            )

        muestra = datos.iloc[:n].copy()

        # Ambas implementaciones deben ser equivalentes
        salida_apply = version_con_apply(muestra)
        salida_vectorizada = version_vectorizada(muestra)

        pd.testing.assert_series_equal(
            salida_apply,
            salida_vectorizada
        )

        for nombre, funcion in [
            ("apply", version_con_apply),
            ("vectorizada", version_vectorizada)
        ]:

            # Medición de tiempo
            tiempos = timeit.repeat(
                lambda: funcion(muestra),
                repeat=repeticiones,
                number=1
            )

            # Medición de memoria
            memoria_mb = medir_memoria(
                funcion,
                muestra
            )

            resultados.append({
                "Registros": n,
                "Implementacion": nombre,
                "TiempoSegundos": min(tiempos),
                "MemoriaMB": memoria_mb
            })

    return pd.DataFrame(resultados)
