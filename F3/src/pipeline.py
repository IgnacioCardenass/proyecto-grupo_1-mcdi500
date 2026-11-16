class Pipeline:
    """Ejecuta las transformaciones de datos en orden."""

    def __init__(self, pasos):
        self._pasos = list(pasos)
        self._ajustado = False

    def ajustar(self, datos):
        """Ajusta cada transformador en el orden definido."""

        intermedio = datos.copy()

        for paso in self._pasos:
            intermedio = (
                paso.ajustar(intermedio)
                .transformar(intermedio)
            )

        self._ajustado = True

        return self

    def transformar(self, datos):
        """Aplica todas las transformaciones del pipeline."""

        if not self._ajustado:
            raise RuntimeError(
                "Primero debe ejecutar ajustar()"
            )

        resultado = datos.copy()

        for paso in self._pasos:
            resultado = paso.transformar(resultado)

        return resultado