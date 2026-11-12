from pathlib import Path
import pandas as pd

def cargar_datos(ruta):
    """Carga un archivo CSV y devuelve un DataFrame."""

    try:
        datos = pd.read_csv(ruta)

    except FileNotFoundError:
        print("No se encontró el archivo:", ruta)
        raise

    print("Cargado:", datos.shape[0], "filas y",
          datos.shape[1], "columnas")

    return datos