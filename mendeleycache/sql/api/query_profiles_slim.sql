-- noinspection SqlResolve
SELECT
   cp.id,
   cp.name,
   agg.cnt
FROM
   cache_profile cp,
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
WHERE cp.id = agg.id