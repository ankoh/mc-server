-- noinspection SqlResolve
SELECT
   cp.id    AS id,
   cp.name  AS name,
   CASE WHEN agg.cnt IS NULL THEN 0 ELSE agg.cnt END AS cnt
FROM
   cache_profile cp
   LEFT OUTER JOIN
   (
     SELECT cp.id AS id, COUNT(*) AS cnt
     FROM
      cache_profile cp,
      cache_document cd,
      cache_profile_has_cache_document cphcd
     WHERE cp.id = cphcd.cache_profile_id
     AND cd.id = cphcd.cache_document_id
     GROUP BY cp.id
   ) agg
   ON cp.id = agg.id