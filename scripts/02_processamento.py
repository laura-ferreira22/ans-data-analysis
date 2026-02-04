import pandas as pd
from pathlib import Path
from utils import extract_year_quarter_from_filename


DESCRICAO_PATTERN = (
    "EVENTO|SINISTRO|ASSISTENCIAL"
)

def process_file(file):
    df = pd.read_csv(file, sep=';', encoding='latin1', dtype=str)


    df = df[df['DESCRICAO'].str.contains(
        DESCRICAO_PATTERN,
        case=False,
        na=False
    )]

    if df.empty:
        print(f"Nenhuma despesa encontrada em {file.name}")
        return None

    ano, trimestre = extract_year_quarter_from_filename(file.name)

    return pd.DataFrame({
        'RegistroANS': df['REG_ANS'],
        'Ano': ano,
        'Trimestre': trimestre,
        'ValorDespesas': df['VL_SALDO_FINAL']
    })

def main():
    dfs = []
    base_path = Path("data/raw")

    for file in base_path.glob("*.csv"):
        print(f"Processando arquivo: {file.name}")
        result = process_file(file)
        if result is not None and not result.empty:
            dfs.append(result)

    if not dfs:
        raise RuntimeError(
            "Nenhum arquivo válido foi processado. "
            "Verifique o filtro de DESCRICAO."
        )

    final_df = pd.concat(dfs, ignore_index=True)


    final_df['ValorDespesas'] = (
        final_df['ValorDespesas']
        .astype(str)
        .str.replace('.', '', regex=False)
        .str.replace(',', '.', regex=False)
        .astype(float)
    )

    final_df.to_csv(
        'data/processed/consolidado_despesas.csv',
        index=False
    )

    print("consolidado_despesas.csv gerado com sucesso!")

if __name__ == "__main__":
    main()
