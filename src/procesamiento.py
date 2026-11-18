
import pandas as pd


def normalizar_montos(serie: pd.Series) -> pd.Series:
    """
    Convierte montos de licitaciones a valores numéricos.

    Reconoce números con punto decimal, coma decimal
    y notación científica.

    Los valores no convertibles pasan a NaN.
    """

    if not isinstance(serie, pd.Series):
        raise TypeError("Se esperaba una Serie de pandas")

    montos = serie.astype("string").str.strip()

    # Identificar los montos que utilizan coma decimal
    formato_coma_decimal = montos.str.fullmatch(
        r"[+-]?\d+,\d+([eE][+-]?\d+)?",
        na=False
    )

    # Reemplazar la coma decimal por un punto
    montos.loc[formato_coma_decimal] = (
        montos.loc[formato_coma_decimal]
        .str.replace(",", ".", regex=False)
    )

    # Convertir a valores numéricos
    return pd.to_numeric(montos, errors="coerce")


def consolidar_por_licitacion(bloques):
    """
    Consolida registros para obtener una fila por licitación.

    Parámetros
    ----------
    bloques:
        Iterador de DataFrames de pandas.

    Retorna
    -------
    df_licitaciones:
        DataFrame con un registro por CodigoExterno.
    conflictos_estado:
        Diccionario de códigos con distintos estados.
    total_filas:
        Número de filas originales procesadas.
    codigos_sin_id:
        Número de filas sin CodigoExterno.

    Nota:
        Conserva el primer registro de cada código y
        audita las diferencias en Estado. La revisión
        de otras columnas se realiza posteriormente.
    """

    licitaciones = {}
    estados_por_codigo = {}
    total_filas = 0
    codigos_sin_id = 0

    for bloque in bloques:

        if not {"CodigoExterno", "Estado"}.issubset(
            bloque.columns
        ):
            raise KeyError(
                "Faltan las columnas CodigoExterno o Estado"
            )

        total_filas += len(bloque)

        codigos_sin_id += int(
            bloque["CodigoExterno"].isna().sum()
        )

        bloque = bloque.dropna(
            subset=["CodigoExterno"]
        )

        # Conservar el primer registro de cada código
        primeros = bloque.drop_duplicates(
            subset=["CodigoExterno"]
        )

        for codigo, registro in primeros.set_index(
            "CodigoExterno", drop=False
        ).iterrows():
            if codigo not in licitaciones:
                licitaciones[codigo] = registro.to_dict()

        # Registrar todos los estados observados
        for codigo, grupo in bloque.groupby("CodigoExterno"):
            estados = set(
                grupo["Estado"].dropna().astype(str)
            )

            estados_por_codigo.setdefault(
                codigo, set()
            ).update(estados)

    df_licitaciones = pd.DataFrame(
        licitaciones.values()
    ).reset_index(drop=True)

    conflictos_estado = {
        codigo: estados
        for codigo, estados in estados_por_codigo.items()
        if len(estados) > 1
    }

    return (
        df_licitaciones,
        conflictos_estado,
        total_filas,
        codigos_sin_id
    )


def comparar_imputaciones(datos, columna, agrupador=None, n_grupos=4):
    """
    Compara diferentes estrategias de tratamiento
    de valores faltantes en una columna numérica.
    """

    if columna not in datos.columns:
        raise KeyError(f"No existe la columna: {columna}")

    original = datos[columna]

    if original.isna().sum() == 0:
        raise ValueError(
            f"'{columna}' no tiene faltantes que comparar."
        )

    resultados = {
        "sin imputar (referencia)": original.dropna(),
        "eliminar filas": original.dropna(),
        "media": original.fillna(original.mean()),
        "mediana": original.fillna(original.median()),
    }

    if agrupador is not None:
        tramos = pd.qcut(
            datos[agrupador],
            q=n_grupos,
            duplicates="drop"
        )

        resultados["mediana por grupo"] = original.fillna(
            original.groupby(
                tramos,
                observed=True
            ).transform("median")
        )

    filas = []

    for nombre, serie in resultados.items():
        filas.append({
            "estrategia": nombre,
            "n": len(serie.dropna()),
            "media": round(serie.mean(), 2),
            "desv_est": round(serie.std(), 3),
            "asimetria": round(serie.skew(), 3),
        })

    tabla = pd.DataFrame(filas)

    referencia = tabla.iloc[0]["desv_est"]

    tabla["cambio_desv_%"] = (
        (tabla["desv_est"] - referencia)
        / referencia * 100
    ).round(2)

    tabla["filas_perdidas"] = (
        len(datos) - tabla["n"]
    )

    return tabla


def leer_bloques_zip(ruta, columnas=None, tamano_bloque=50000):
    """
    Lee un archivo CSV comprimido en ZIP por bloques.

    Usa el separador y la codificación del dataset
    de licitaciones de ChileCompra.
    """
    from pathlib import Path

    ruta = Path(ruta)

    if not ruta.is_file():
        raise FileNotFoundError(
            f"No se encontró el archivo: {ruta}"
        )

    if not isinstance(tamano_bloque, int) or tamano_bloque <= 0:
        raise ValueError(
            "tamano_bloque debe ser un entero positivo"
        )

    return pd.read_csv(
        ruta,
        compression="zip",
        sep=";",
        encoding="latin-1",
        usecols=columnas,
        dtype={"CodigoExterno": "string"},
        chunksize=tamano_bloque,
        low_memory=False
    )


def validar_estructura_zip(ruta_origen, ruta_destino):
    """
    Crea un ZIP depurado conservando las filas que
    tienen la misma cantidad de columnas que el encabezado.

    No modifica el archivo original.

    Retorna un diccionario con los conteos de validación.
    """
    import csv
    import io
    import zipfile
    from pathlib import Path

    ruta_origen = Path(ruta_origen)
    ruta_destino = Path(ruta_destino)

    if not ruta_origen.is_file():
        raise FileNotFoundError(
            f"No se encontró el archivo: {ruta_origen}"
        )

    if ruta_origen.resolve() == ruta_destino.resolve():
        raise ValueError(
            "El archivo de salida debe ser distinto del original"
        )

    ruta_destino.parent.mkdir(
        parents=True, exist_ok=True
    )

    filas_validas = 0
    filas_incorrectas = 0
    filas_vacias = 0

    with zipfile.ZipFile(ruta_origen, "r") as origen:

        archivos_csv = [
            nombre for nombre in origen.namelist()
            if nombre.lower().endswith(".csv")
        ]

        if len(archivos_csv) != 1:
            raise ValueError(
                "El ZIP debe contener exactamente un archivo CSV"
            )

        nombre_csv = archivos_csv[0]

        with origen.open(nombre_csv) as archivo_original, \
             zipfile.ZipFile(
                 ruta_destino,
                 "w",
                 compression=zipfile.ZIP_DEFLATED
             ) as destino:

            lector_texto = io.TextIOWrapper(
                archivo_original,
                encoding="latin-1",
                newline=""
            )

            lector = csv.reader(
                lector_texto,
                delimiter=";"
            )

            encabezado = next(lector)
            columnas_esperadas = len(encabezado)

            with destino.open(
                "licitaciones_validadas.csv", "w"
            ) as archivo_salida:

                escritor_texto = io.TextIOWrapper(
                    archivo_salida,
                    encoding="latin-1",
                    newline=""
                )

                escritor = csv.writer(
                    escritor_texto,
                    delimiter=";"
                )

                escritor.writerow(encabezado)

                for fila in lector:
                    if len(fila) == columnas_esperadas:
                        escritor.writerow(fila)
                        filas_validas += 1
                    elif len(fila) == 0:
                        filas_vacias += 1
                    else:
                        filas_incorrectas += 1

                escritor_texto.flush()

    return {
        "columnas_esperadas": columnas_esperadas,
        "filas_validas": filas_validas,
        "filas_incorrectas": filas_incorrectas,
        "filas_vacias": filas_vacias
    }


def separar_registros_sospechosos(
    datos,
    valores_por_codigo,
    columnas_verificar,
    sin_estado_reconocido,
    codigos_sospechosos
):
    """
    Identifica y separa licitaciones que requieren revisión.

    Considera discrepancias entre registros del mismo código,
    ausencia de un estado reconocido e identificadores
    sospechosos.

    No modifica el DataFrame original.
    """

    if "CodigoExterno" not in datos.columns:
        raise KeyError("Falta la columna CodigoExterno")

    # Códigos con diferencias en variables auditadas
    codigos_discrepantes = {
        codigo
        for codigo, valores in valores_por_codigo.items()
        if any(
            len(valores[columna]) > 1
            for columna in columnas_verificar
        )
    }

    # Unificar los motivos de revisión
    codigos_revision = (
        codigos_discrepantes
        | set(sin_estado_reconocido)
        | set(codigos_sospechosos)
    )

    mascara_revision = datos[
        "CodigoExterno"
    ].isin(codigos_revision)

    # Separar sin modificar los originales
    pendientes = datos.loc[
        mascara_revision
    ].copy()

    conservados = datos.loc[
        ~mascara_revision
    ].copy()

    return (
        conservados,
        pendientes,
        codigos_discrepantes,
        codigos_revision
    )
