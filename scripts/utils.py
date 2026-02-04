import unicodedata
from pathlib import Path
import re


def normalize_column(col):
    col = col.lower().strip()
    col = unicodedata.normalize('NFKD', col).encode('ascii', 'ignore').decode('ascii')
    return col.replace(' ', '_')

def extract_year_quarter(path):
    parts = Path(path).parts
    ano = next(p for p in parts if p.isdigit() and len(p) == 4)
    trimestre = next(p for p in parts if 't' in p.lower())
    return ano, trimestre

def extract_year_quarter_from_filename(filename):
    match = re.search(r'(\d)T(\d{4})', filename)
    if not match:
        raise ValueError(f"Nome de arquivo inválido: {filename}")

    trimestre = f"{match.group(1)}T"
    ano = match.group(2)
    return ano, trimestre