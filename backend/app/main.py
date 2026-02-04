from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import pandas as pd

from .data import despesas_df
from .utils import paginate

app = FastAPI(title="Teste 4 - API Operadoras")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/operadoras")
def list_operadoras(
    q: Optional[str] = Query(None, description="Filtro por CNPJ ou Razão Social"),
    page: int = 1,
    page_size: int = 20
):
    df = despesas_df()

    ops = df[["CNPJ", "RazaoSocial", "UF", "Modalidade"]].dropna(subset=["CNPJ"]).drop_duplicates()

    if q:
        qq = q.strip().lower()
        ops = ops[
            ops["CNPJ"].astype(str).str.contains(qq, na=False) |
            ops["RazaoSocial"].astype(str).str.lower().str.contains(qq, na=False)
        ]

    ops = ops.sort_values("RazaoSocial")

    items = [
        {
            "cnpj": r["CNPJ"],
            "razao_social": r["RazaoSocial"],
            "uf": r.get("UF", None),
            "modalidade": r.get("Modalidade", None),
        }
        for _, r in ops.iterrows()
    ]

    return paginate(items, page, page_size)

@app.get("/api/operadoras/{cnpj}")
def get_operadora(cnpj: str):
    df = despesas_df()
    cnpj = "".join([c for c in cnpj if c.isdigit()])

    op = (
        df[df["CNPJ"] == cnpj][["CNPJ", "RazaoSocial", "UF", "Modalidade"]]
        .drop_duplicates()
        .head(1)
    )

    if op.empty:
        raise HTTPException(status_code=404, detail="Operadora não encontrada")

    row = op.iloc[0]
    return {
        "cnpj": row["CNPJ"],
        "razao_social": row["RazaoSocial"],
        "uf": row.get("UF", None),
        "modalidade": row.get("Modalidade", None),
    }

@app.get("/api/operadoras/{cnpj}/despesas")
def get_despesas_operadora(cnpj: str):
    df = despesas_df()
    cnpj = "".join([c for c in cnpj if c.isdigit()])

    sub = df[df["CNPJ"] == cnpj][["Ano", "Trimestre", "ValorDespesas"]].copy()
    if sub.empty:
        raise HTTPException(status_code=404, detail="Sem despesas para este CNPJ")

    g = (
        sub.groupby(["Ano", "Trimestre"], as_index=False)["ValorDespesas"]
        .sum()
        .sort_values(["Ano", "Trimestre"])
    )

    return [
        {"ano": int(r["Ano"]), "trimestre": r["Trimestre"], "valor_despesas": float(r["ValorDespesas"])}
        for _, r in g.iterrows()
    ]

@app.get("/api/estatisticas")
def estatisticas():
    df = despesas_df()


    by_uf_op = (
        df.dropna(subset=["UF", "CNPJ"])
          .groupby(["UF", "CNPJ"], as_index=False)["ValorDespesas"].sum()
    )
    by_uf = by_uf_op.groupby("UF", as_index=False).agg(
        total_despesas=("ValorDespesas", "sum"),
        media_por_operadora=("ValorDespesas", "mean"),
    ).sort_values("total_despesas", ascending=False)


    by_uf = by_uf.head(10)

    return [
        {
            "uf": r["UF"],
            "total_despesas": float(r["total_despesas"]),
            "media_por_operadora": float(r["media_por_operadora"]),
        }
        for _, r in by_uf.iterrows()
    ]
