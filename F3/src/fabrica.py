from transformadores import ImputadorMediana, CodificadorNominal


def crear_transformador(tipo, columna):
    """Crea un transformador según el tipo de operación."""

    if tipo == "monto":
        return ImputadorMediana(columna)

    elif tipo == "categorica":
        return CodificadorNominal(columna)

    else:
        raise ValueError(
            f"Tipo de transformación no reconocido: {tipo}"
        )