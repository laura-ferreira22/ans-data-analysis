-- Tabela de operadoras 
CREATE TABLE operadoras (
    registro_ans VARCHAR(10) PRIMARY KEY,
    cnpj VARCHAR(14) NOT NULL,
    razao_social VARCHAR(255) NOT NULL,
    uf CHAR(2),
    modalidade VARCHAR(100)
);

--Tabela de despesas consolidadas 
CREATE TABLE despesas (
    registro_ans VARCHAR(10) REFERENCES operadoras(registro_ans),
    ano SMALLINT NOT NULL,
    trimestre SMALLINT NOT NULL,
    valor_despesas DECIMAL(18,2) NOT NULL,
    PRIMARY KEY (registro_ans, ano, trimestre)
);

--Tabela de dados agregados 
CREATE TABLE despesas_agregadas (
    razao_social VARCHAR(255),
    uf CHAR(2),
    total_despesas DECIMAL(18,2),
    media_por_trimestre DECIMAL(18,2),
    desvio_padrao DECIMAL(18,2)
);
