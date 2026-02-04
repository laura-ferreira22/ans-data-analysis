import pandas as pd

CONSOLIDADO_PATH = "data/processed/consolidado_despesas.csv"
CADASTRO_PATH = "data/raw/Relatorio_cadop.csv"
OUTPUT_PATH = "data/final/despesas_enriquecidas.csv"

def main():
    despesas = pd.read_csv(CONSOLIDADO_PATH, dtype=str)

    cadastro = pd.read_csv(
        CADASTRO_PATH,
        sep=';',
        encoding='latin1',
        dtype=str
    )

    
    despesas["RegistroANS"] = despesas["RegistroANS"].astype(str).str.strip()
    cadastro["REGISTRO_OPERADORA"] = cadastro["REGISTRO_OPERADORA"].astype(str).str.strip()

   
    df = despesas.merge(
        cadastro,
        left_on="RegistroANS",
        right_on="REGISTRO_OPERADORA",
        how="left"
    )

    
    nome_padrao = (
        df.groupby('CNPJ')['Razao_Social']
          .agg(lambda x: x.mode().iloc[0] if not x.mode().empty else x.iloc[0])
    )
    df['Razao_Social'] = df['CNPJ'].map(nome_padrao)

    #
    df["ValorDespesas"] = df["ValorDespesas"].astype(float)
    df["ValorSuspeito"] = df["ValorDespesas"] <= 0

    
    df["Trimestre"] = df["Trimestre"].str.upper().str.replace("T", "")
    df["Trimestre"] = "Q" + df["Trimestre"]

    
    df_final = pd.DataFrame({
        "CNPJ": df["CNPJ"],
        "RazaoSocial": df["Razao_Social"],
        "RegistroANS": df["REGISTRO_OPERADORA"],
        "Modalidade": df["Modalidade"],
        "UF": df["UF"],
        "Ano": df["Ano"],
        "Trimestre": df["Trimestre"],
        "ValorDespesas": df["ValorDespesas"],
        "ValorSuspeito": df["ValorSuspeito"]
    })

    df_final.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")
    print("despesas_enriquecidas.csv gerado com sucesso!")

if __name__ == "__main__":
    main()
