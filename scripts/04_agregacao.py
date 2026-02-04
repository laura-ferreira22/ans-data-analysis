import pandas as pd

INPUT_PATH = "data/final/despesas_enriquecidas.csv"
OUTPUT_PATH = "data/final/despesas_agregadas.csv"

def main():
    df = pd.read_csv(INPUT_PATH, dtype={"CNPJ": str})

    df["ValorDespesas"] = pd.to_numeric(df["ValorDespesas"], errors="coerce")

    
    df = df[df["ValorDespesas"].notna()]
    df = df[df["ValorDespesas"] > 0]

    agg = (
        df.groupby(["RazaoSocial", "UF"], as_index=False)
          .agg(
              TotalDespesas=("ValorDespesas", "sum"),
              MediaPorTrimestre=("ValorDespesas", "mean"),
              DesvioPadrao=("ValorDespesas", "std"),
              QtdRegistros=("ValorDespesas", "count")
          )
    )
    agg = agg.sort_values("TotalDespesas", ascending=False)

    agg.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")
    print("despesas_agregadas.csv gerado com sucesso!")

if __name__ == "__main__":
    main()
