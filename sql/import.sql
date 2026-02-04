
COPY operadoras(registro_ans, cnpj, razao_social, uf, modalidade)
FROM 'data/raw/Relatorio_cadop.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'UTF8';


COPY despesas(registro_ans, ano, trimestre, valor_despesas)
FROM 'data/processed/consolidado_despesas.csv'
DELIMITER ','
CSV HEADER
ENCODING 'UTF8';


COPY despesas_agregadas(razao_social, uf, total_despesas, media_por_trimestre, desvio_padrao)
FROM 'data/final/despesas_agregadas.csv'
DELIMITER ','
CSV HEADER
ENCODING 'UTF8';
