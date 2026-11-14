
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
