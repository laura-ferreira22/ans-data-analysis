from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[2]  
DATA_FINAL = BASE / "data" / "final"
DATA_RAW = BASE / "data" / "raw"


DESPESAS_ENRIQ = DATA_FINAL / "despesas_enriquecidas.csv"
AGREGADAS = DATA_FINAL / "despesas_agregadas.csv"
CADOP = DATA_RAW / "Relatorio_cadop.csv"

_despesas = None
_agregadas = None
_cadop = None

def load_data():
    global _despesas, _agregadas, _cadop

    if _despesas is None:
        _despesas = pd.read_csv(DESPESAS_ENRIQ, dtype=str)

        _despesas["CNPJ"] = _despesas["CNPJ"].astype(str).str.replace(r"\D", "", regex=True)
        _despesas["ValorDespesas"] = pd.to_numeric(_despesas["ValorDespesas"], errors="coerce").fillna(0.0)
        _despesas["Ano"] = pd.to_numeric(_despesas["Ano"], errors="coerce").fillna(0).astype(int)

        tri = _despesas["Trimestre"].astype(str).str.upper().str.strip()
        tri = tri.str.replace("T", "", regex=False)
        tri = tri.apply(lambda x: x if x.startswith("Q") else f"Q{x}" if x.isdigit() else x)
        _despesas["Trimestre"] = tri

    if _agregadas is None and AGREGADAS.exists():
        _agregadas = pd.read_csv(AGREGADAS, dtype=str)
        for c in ["TotalDespesas", "MediaPorTrimestre", "DesvioPadrao"]:
            if c in _agregadas.columns:
                _agregadas[c] = pd.to_numeric(_agregadas[c], errors="coerce").fillna(0.0)

    if _cadop is None and CADOP.exists():
        _cadop = pd.read_csv(CADOP, sep=";", encoding="latin1", dtype=str)

def despesas_df():
    load_data()
    return _despesas

def agregadas_df():
    load_data()
    return _agregadas

def cadop_df():
    load_data()
    return _cadop
