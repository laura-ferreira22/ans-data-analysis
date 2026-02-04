
-- Query 1: 
WITH limites AS (
  SELECT
    registro_ans,
    MIN((ano * 10 + trimestre)) AS periodo_ini,
    MAX((ano * 10 + trimestre)) AS periodo_fim
  FROM despesas
  GROUP BY registro_ans
),
valores AS (
  SELECT
    l.registro_ans,
    d_ini.valor_despesas AS valor_inicial,
    d_fim.valor_despesas AS valor_final
  FROM limites l
  JOIN despesas d_ini
    ON d_ini.registro_ans = l.registro_ans
   AND (d_ini.ano * 10 + d_ini.trimestre) = l.periodo_ini
  JOIN despesas d_fim
    ON d_fim.registro_ans = l.registro_ans
   AND (d_fim.ano * 10 + d_fim.trimestre) = l.periodo_fim
)
SELECT
  o.razao_social,
  v.registro_ans,
  ((v.valor_final - v.valor_inicial) / NULLIF(v.valor_inicial, 0)) * 100 AS crescimento_percentual
FROM valores v
JOIN operadoras o ON o.registro_ans = v.registro_ans
WHERE v.valor_inicial > 0
ORDER BY crescimento_percentual DESC
LIMIT 5;



-- Query 2
WITH por_uf_operadora AS (
  SELECT
    o.uf,
    d.registro_ans,
    SUM(d.valor_despesas) AS total_operadora
  FROM despesas d
  JOIN operadoras o ON o.registro_ans = d.registro_ans
  GROUP BY o.uf, d.registro_ans
),
por_uf AS (
  SELECT
    uf,
    SUM(total_operadora) AS total_despesas_uf,
    AVG(total_operadora) AS media_por_operadora_uf
  FROM por_uf_operadora
  GROUP BY uf
)
SELECT *
FROM por_uf
ORDER BY total_despesas_uf DESC
LIMIT 5;



-- Query 3
WITH media_geral AS (
  SELECT AVG(valor_despesas) AS media
  FROM despesas
),
acima_media AS (
  SELECT
    registro_ans,
    ano,
    trimestre
  FROM despesas, media_geral
  WHERE valor_despesas > media_geral.media
)
SELECT COUNT(*) AS qtd_operadoras
FROM (
  SELECT registro_ans
  FROM acima_media
  GROUP BY registro_ans
  HAVING COUNT(*) >= 2
) t;
