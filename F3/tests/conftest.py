import sys
from pathlib import Path

# Permitir importar desde F3/src y desde la raíz del proyecto (src/)
raiz_f3 = Path(__file__).resolve().parent.parent / "src"
raiz_proyecto = Path(__file__).resolve().parent.parent.parent

sys.path.insert(0, str(raiz_f3))
sys.path.insert(0, str(raiz_proyecto))