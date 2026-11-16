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