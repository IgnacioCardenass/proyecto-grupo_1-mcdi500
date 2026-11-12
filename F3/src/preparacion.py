import pandas as pd

def calcular_dias_publicacion_cierre(datos):
    """Calcula los días entre la publicación y el cierre de una licitación."""

    for columna in ["FechaPublicacion", "FechaCierre"]:
        if columna not in datos.columns:
            raise KeyError(f"No se encontró la columna {columna}")

    df = datos.copy()

    for columna in ["FechaPublicacion", "FechaCierre"]:
        df[columna] = pd.to_datetime(
            df[columna],
            errors="coerce"
        )

    # Calculamos los días entre la públicación y el cierre de la licitación
    df["DiasPublicacionCierre"] = (
        df["FechaCierre"]
        - df["FechaPublicacion"]
    ).dt.total_seconds() / 86400

    return df

def crear_variable_objetivo(datos):
    """Creamos la variable EsDesierta a partir del estado de la licitación."""

    if "Estado" not in datos.columns:
        raise KeyError("No se encontró la columna Estado")
        
    df = datos.copy()

    estados_finales = [
        "Adjudicada",
        "Desierta (o art. 3 ó 9 Ley 19.886)"
    ]

    if not df["Estado"].isin(estados_finales).all():
        raise ValueError("Existen estados no reconocidos")

    # Creamos la variable binaria
    df["EsDesierta"] = (
        df["Estado"] == "Desierta (o art. 3 ó 9 Ley 19.886)"
    ).astype(int)

    return df