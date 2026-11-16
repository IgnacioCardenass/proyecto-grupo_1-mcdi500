import pandas as pd

class Transformador:
    """Clase base para las transformaciones de datos."""

    def __init__(self, columna):
        self.columna = columna
        self._parametros = {}
        self._ajustado = False

    def ajustar(self, datos):
        """Aprende los parámetros necesarios."""

        if self.columna not in datos.columns:
            raise KeyError(
                f"No existe la columna {self.columna}"
            )

        self._parametros = self.aprender(datos)
        self._ajustado = True

        return self

    def transformar(self, datos):
        """Aplica la transformación a una copia de los datos."""

        if not self._ajustado:
            raise RuntimeError(
                "Primero debe ejecutar ajustar()"
            )

        if self.columna not in datos.columns:
            raise KeyError(
                f"No existe la columna {self.columna}"
            )

        return self.aplicar(datos.copy())

    def aprender(self, datos):
        raise NotImplementedError(
            "La clase hija debe implementar aprender()"
        )

    def aplicar(self, datos):
        raise NotImplementedError(
            "La clase hija debe implementar aplicar()"
        )

class ImputadorMediana(Transformador):
    """Imputa montos faltantes utilizando la mediana en CLP."""

    def aprender(self, datos):
        """Calcula la mediana de los montos en pesos chilenos."""

        if "Moneda Adquisicion" not in datos.columns:
            raise KeyError("No existe la columna de moneda")

        mascara_clp = (
            datos["Moneda Adquisicion"] == "Peso Chileno"
        )

        # Calculamos la mediana la cual fue previamente seleccionada
        mediana = datos.loc[
            mascara_clp, self.columna
        ].median()

        if pd.isna(mediana):
            raise ValueError("No se pudo calcular la mediana")

        return {"mediana": mediana}

    def aplicar(self, datos):
        """Imputa los montos faltantes y registra los cambios."""

        faltantes = datos[self.columna].isna()

        if not (
            datos.loc[faltantes, "Moneda Adquisicion"]
            == "Peso Chileno"
        ).all():
            raise ValueError(
                "Existen montos faltantes en otras monedas"
            )

        datos["MontoEstimadoImputado"] = (
            datos[self.columna].copy()
        )

        # Imputamos los valores faltantes
        datos.loc[
            faltantes, "MontoEstimadoImputado"
        ] = self._parametros["mediana"]

        datos["MontoFueImputado"] = faltantes.astype(int)

        return datos


class CodificadorNominal(Transformador):
    """Codifica variables categóricas mediante One-Hot Encoding."""

    def aprender(self, datos):
        """Identifica las categorías existentes."""

        valores = (
            datos[self.columna]
            .astype("string")
            .str.strip()
            .replace("", pd.NA)
            .fillna("No informado")
        )

        # con esto guardams las categorias
        categorias = sorted(valores.unique())

        return {"categorias": categorias}

    def aplicar(self, datos):
        """Transforma las categorías en columnas binarias."""
        
        valores = (
            datos[self.columna]
            .astype("string")
            .str.strip()
            .replace("", pd.NA)
            .fillna("No informado")
        )

        
        if not valores.isin(
            self._parametros["categorias"]
        ).all():
            raise ValueError(
                "Se encontraron categorías no reconocidas"
            )

        # Aplicamos One-Hot Encoding
        columnas_binarias = pd.get_dummies(
            valores,
            prefix=self.columna,
            dtype=int
        )

        columnas_esperadas = [
            f"{self.columna}_{categoria}"
            for categoria in self._parametros["categorias"]
        ]

        columnas_binarias = columnas_binarias.reindex(
            columns=columnas_esperadas,
            fill_value=0
        )

        datos = datos.drop(columns=[self.columna])

        datos = pd.concat(
            [datos, columnas_binarias],
            axis=1
        )

        return datos