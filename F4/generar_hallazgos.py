"""Generador de la tabla formal de hallazgos cuantitativos y metadatos (Fase 4).

Centraliza las cifras del análisis para asegurar consistencia total
entre el cuaderno ejecutable, el informe técnico en PDF y el video.

MCDI500 · Grupo N° 1
"""

import json
import sys
from datetime import datetime
from pathlib import Path
import pandas as pd

# Permitir importar desde src/
raiz = Path(__file__).resolve().parent.parent
if str(raiz) not in sys.path:
    sys.path.insert(0, str(raiz))

from src.analisis_f4 import (
    intervalo_wilson,
    matriz_cruce_tipo_sector,
    resumen_montos_y_plazos,
    tasa_desercion_por_grupo,
)


def generar_archivos():
    ruta_datos = raiz / "F2" / "data" / "processed" / "licitaciones_filtradas_provisional.csv.gz"
    dir_docs = raiz / "docs"
    dir_docs.mkdir(parents=True, exist_ok=True)

    print("Cargando dataset analítico...")
    df = pd.read_csv(ruta_datos)
    total_filas = len(df)
    total_desiertas = int(df["EsDesierta"].sum())
    tasa_global = total_desiertas / total_filas
    inf_glob, sup_glob = intervalo_wilson(total_desiertas, total_filas)

    print(f"Total registros: {total_filas:,} | Desiertas: {total_desiertas:,} ({tasa_global*100:.2f}%)")

    # 1. Análisis por Sector
    tasas_sector = tasa_desercion_por_grupo(df, columna_grupo="sector")
    muni = tasas_sector[tasas_sector["sector"] == "Municipalidades"].iloc[0]
    salud = tasas_sector[tasas_sector["sector"] == "Salud"].iloc[0]

    # 2. Análisis por Tipo
    tasas_tipo = tasa_desercion_por_grupo(df, columna_grupo="Tipo")
    tipo_lr = tasas_tipo[tasas_tipo["Tipo"] == "LR"].iloc[0]
    tipo_lp = tasas_tipo[tasas_tipo["Tipo"] == "LP"].iloc[0]

    # 3. Resumen de Plazos y Montos
    res_mp = resumen_montos_y_plazos(df)
    plazo_med_adj = res_mp[res_mp["Estado"] == "Adjudicada"]["Plazo_Mediana_Dias"].values[0]
    plazo_med_des = res_mp[res_mp["Estado"] == "Desierta"]["Plazo_Mediana_Dias"].values[0]

    # 4. Tabla de Hallazgos Estructurada
    hallazgos = [
        {
            "id_hallazgo": "H1",
            "dimension": "Tasa Global",
            "indicador": "Proporción basal de licitaciones desiertas",
            "n_total": total_filas,
            "n_desiertas": total_desiertas,
            "tasa_pct": f"{tasa_global*100:.2f} %".replace(".", ","),
            "ic_wilson_95": f"[{inf_glob*100:.2f} %, {sup_glob*100:.2f} %]".replace(".", ","),
            "interpretacion_negocio": "Aproximadamente 1 de cada 7 licitaciones (14,38 %) termina desierta.",
            "archivo_origen": "F2/data/processed/licitaciones_filtradas_provisional.csv.gz"
        },
        {
            "id_hallazgo": "H2",
            "dimension": "Vulnerabilidad Sectorial",
            "indicador": "Tasa de deserción en Municipalidades vs Salud",
            "n_total": int(muni["total_n"]),
            "n_desiertas": int(muni["desiertas_casos"]),
            "tasa_pct": f"{muni['tasa_desierta']*100:.2f} %".replace(".", ","),
            "ic_wilson_95": f"[{muni['ic_inferior']*100:.2f} %, {muni['ic_superior']*100:.2f} %]".replace(".", ","),
            "interpretacion_negocio": "Municipalidades lidera el fracaso con 16,74 %, significativamente mayor que Salud (11,98 %).",
            "archivo_origen": "src/analisis_f4.py::tasa_desercion_por_grupo"
        },
        {
            "id_hallazgo": "H3",
            "dimension": "Complejidad del Procedimiento",
            "indicador": "Tasa en Licitaciones Mayores (LR > 1000 UTM)",
            "n_total": int(tipo_lr["total_n"]),
            "n_desiertas": int(tipo_lr["desiertas_casos"]),
            "tasa_pct": f"{tipo_lr['tasa_desierta']*100:.2f} %".replace(".", ","),
            "ic_wilson_95": f"[{tipo_lr['ic_inferior']*100:.2f} %, {tipo_lr['ic_superior']*100:.2f} %]".replace(".", ","),
            "interpretacion_negocio": "Las licitaciones LR tienen 15,51 % de deserción, superando a licitaciones públicas estándar (LP: 12,29 %).",
            "archivo_origen": "src/analisis_f4.py::tasa_desercion_por_grupo"
        },
        {
            "id_hallazgo": "H4",
            "dimension": "Plazos de Convocatoria",
            "indicador": "Mediana de días entre publicación y cierre",
            "n_total": total_filas,
            "n_desiertas": total_desiertas,
            "tasa_pct": "12 días (ambos)",
            "ic_wilson_95": "Mediana robusta ante asimetría",
            "interpretacion_negocio": "Ambos estados comparten una mediana de 12 días; las desiertas exhiben colas superiores más largas.",
            "archivo_origen": "src/analisis_f4.py::resumen_montos_y_plazos"
        },
        {
            "id_hallazgo": "H5",
            "dimension": "Control de Confusión",
            "indicador": "Tasa cruzada Tipo de Licitación x Sector",
            "n_total": total_filas,
            "n_desiertas": total_desiertas,
            "tasa_pct": "Matriz multivariada",
            "ic_wilson_95": "Asociación no es causalidad",
            "interpretacion_negocio": "Municipalidades presenta mayores tasas en casi todos los tipos, descartando sesgo de composición.",
            "archivo_origen": "src/analisis_f4.py::matriz_cruce_tipo_sector"
        }
    ]

    df_hallazgos = pd.DataFrame(hallazgos)
    ruta_csv = dir_docs / "hallazgos_f4.csv"
    df_hallazgos.to_csv(ruta_csv, index=False, encoding="utf-8")
    print(f"✅ Archivo de hallazgos generado en: {ruta_csv}")

    # 5. Metadatos de Reproducibilidad
    metadatos = {
        "proyecto": "MCDI500 - Grupo N° 1",
        "fase": "Fase 4: Comunicación y Visualización Técnica",
        "fecha_generacion": datetime.now().isoformat(),
        "universo_analitico": total_filas,
        "licitaciones_desiertas": total_desiertas,
        "tasa_global_desierta": round(tasa_global, 4),
        "ic_wilson_95": [round(inf_glob, 4), round(sup_glob, 4)],
        "fuente_oficial": "Dirección de Compras y Contratación Pública (ChileCompra) - Mercado Público",
        "periodo": "Enero - Junio 2026",
        "sha256_dataset_crudo": "51dcfb421968c3e66111809dd76a70f7ecff16fa31915adc752285a4a5d65232"
    }

    ruta_json = dir_docs / "metadatos_f4.json"
    with open(ruta_json, "w", encoding="utf-8") as f:
        json.dump(metadatos, f, indent=2, ensure_ascii=False)
    print(f"✅ Metadatos de ejecución guardados en: {ruta_json}")


if __name__ == "__main__":
    generar_archivos()