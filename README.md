
# Teste Técnico – ANS (Dados de Operadoras de Saúde)

Este projeto foi desenvolvido como solução para um teste técnico focado em **engenharia de dados, análise, modelagem relacional e construção de API + interface web**.

O objetivo principal foi demonstrar a capacidade de:

* Integrar dados públicos da ANS
* Tratar inconsistências reais
* Tomar decisões técnicas justificadas
* Estruturar um pipeline de dados completo
* Expor os resultados via API e frontend

---

## Visão Geral da Solução

O projeto foi dividido em quatro partes:

| Etapa       | Objetivo                                                |
| ----------- | ------------------------------------------------------- |
| **Teste 1** | Coleta, normalização e consolidação dos dados contábeis |
| **Teste 2** | Validação, enriquecimento com cadastro e agregações     |
| **Teste 3** | Modelagem de banco de dados e queries analíticas        |
| **Teste 4** | Construção de API (FastAPI) e interface web (Vue)       |

---

## Estrutura do Projeto

```
Teste_Laura_Ferreira/
│
├── data/
│   ├── raw/         # arquivos originais da ANS
│   ├── processed/   # dados intermediários
│   └── final/       # datasets finais consolidados
│
├── scripts/         # pipeline de dados (Testes 1 e 2)
│
├── sql/             # modelagem e consultas do banco (Teste 3)
│   ├── ddl.sql
│   ├── import.sql
│   └── queries.sql
│
├── backend/         # API FastAPI
├── frontend/        # Interface Vue
└── README.md
```

---

# TESTE 1 — Integração e Consolidação dos Dados

Os arquivos de demonstrações contábeis foram disponibilizados diretamente em **CSV**, com **um arquivo por trimestre**.

### Decisões Técnicas

* Os arquivos foram armazenados em `data/raw/`
* O **ano e trimestre foram extraídos do nome do arquivo**
* O processamento foi feito **arquivo por arquivo** (abordagem streaming), reduzindo consumo de memória

### 🔍 Identificação de Despesas

As demonstrações contêm diversas contas. Para isolar despesas assistenciais, foi aplicado um **filtro semântico no campo `DESCRICAO`**, mantendo apenas registros com termos como:

* EVENTO
* SINISTRO
* ASSISTENCIAL

Essa abordagem prioriza clareza analítica e alinhamento com o objetivo do teste.

### ⚠️ Inconsistências Tratadas

* **CNPJ duplicado com nomes diferentes** → padronizado usando o nome mais frequente
* **Valores não positivos** → mantidos e marcados como suspeitos
* **Trimestres inconsistentes** → padronizados para o formato `Q1–Q4`

### 📄 Saída

```
data/processed/consolidado_despesas.csv
```

---

# 🔍 TESTE 2 — Validação e Enriquecimento

As demonstrações contábeis **não contêm CNPJ ou Razão Social**, apenas o identificador da operadora (`REG_ANS`).
O enriquecimento foi feito via join com o cadastro **CADOP**:

```
REG_ANS ↔ REGISTRO_OPERADORA
```

### 📌 Validações aplicadas

* CNPJ válido
* Razão Social não vazia
* Valor convertido para número

### 📊 Agregações

Foi gerado um dataset agregado por **Razão Social + UF**, com:

* Total de despesas
* Média por trimestre
* Desvio padrão

Saída:

```
data/final/despesas_agregadas.csv
```

---

# TESTE 3 — Banco de Dados e SQL

##  Modelagem

Foi adotado um **modelo normalizado**, separando:

* `operadoras` → dados cadastrais
* `despesas` → dados financeiros
* `despesas_agregadas` → métricas analíticas

**Justificativa:** reduz redundância e melhora integridade dos dados.

### Tipos de dados

| Campo                 | Tipo             | Motivo                   |
| --------------------- | ---------------- | ------------------------ |
| Valores monetários    | DECIMAL          | precisão financeira      |
| Datas (ano/trimestre) | VARCHAR/SMALLINT | granularidade trimestral |

---

## Importação

Os dados são carregados a partir dos CSVs gerados nos testes anteriores.

Decisões:

* Conversão de strings para números
* Preservação de NULLs
* Padronização de trimestre

---

## Queries Analíticas

**Query 1 — Crescimento percentual**

Operadoras sem dados em todos os trimestres foram avaliadas com base no **primeiro e último trimestre disponível**. Casos com valor inicial zero foram excluídos para evitar distorções.

**Query 2 — Despesas por UF**

Calcula:

* Total por UF
* Média por operadora dentro da UF

**Query 3 — Operadoras acima da média**

CTEs foram utilizadas para separar claramente as etapas, melhorando legibilidade e manutenção.

---

# Execução dos Scripts SQL

```
psql -U usuario -d banco -f sql/ddl.sql
psql -U usuario -d banco -f sql/import.sql
psql -U usuario -d banco -f sql/queries.sql
```

### Observação

Houve instabilidade na inicialização do serviço PostgreSQL no ambiente local.
Mesmo assim, os scripts foram desenvolvidos e organizados para execução direta em qualquer instalação PostgreSQL funcional.

---

# TESTE 4 — API + FRONTEND

## Backend (FastAPI)

Endpoints implementados:

* `/api/operadoras`
* `/api/operadoras/{cnpj}`
* `/api/operadoras/{cnpj}/despesas`
* `/api/estatisticas`

Decisões:

* Paginação no endpoint de listagem
* Dados carregados em memória (cache simples)
* Respostas em JSON estruturado

### Rodar backend

```
cd backend
uvicorn app.main:app --reload --port 8000
```

Swagger:

```
http://127.0.0.1:8000/docs
```

---

## Frontend (Vue)

Interface mínima implementada com:

* Tabela paginada de operadoras
* Filtro por nome ou CNPJ
* Gráfico simples de despesas por UF
* Página de detalhes com despesas trimestrais

### Rodar frontend

```
cd frontend
npm install
npm run dev
```

Acessar:

```
http://localhost:5173
```

---

## Execução simultânea

Backend e frontend devem rodar simultaneamente.

---

#  Limitações Conhecidas

* A análise semântica de despesas depende de palavras-chave e pode não capturar todas as variações contábeis possíveis.
* O cache da API é em memória (não persistente).
* A interface prioriza funcionalidade sobre design visual.


---

Este projeto priorizou **clareza, organização e justificativa técnica das decisões**, conforme os objetivos do teste.
