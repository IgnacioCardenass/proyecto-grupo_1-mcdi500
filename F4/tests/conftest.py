import sys
from pathlib import Path

# Permitir que las pruebas de F4 importen desde la raíz del proyecto (src/)
raiz_proyecto = Path(__file__).resolve().parent.parent.parent
if str(raiz_proyecto) not in sys.path:
    sys.path.insert(0, str(raiz_proyecto))