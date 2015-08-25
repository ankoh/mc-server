-- noinspection SqlResolve
SELECT
   p.*,
   agg.cnt
FROM
   cache_profile cp,
   profile p,
   (
     SELECT id, MAX(cnt) AS cnt
     FROM
     (
      SELECT cp.id AS id , COUNT(*) AS cnt
      FROM
         cache_profile cp,
         cache_document cd,
         cache_profile_has_cache_document cphcd
      WHERE cp.id = cphcd.cache_profile_id
      AND cphcd.cache_document_id = cd.id
      AND cp.id IN :profile_ids
      GROUP BY cp.id

      UNION ALL

      SELECT cp.id AS id, COUNT(DISTINCT(cd.id)) AS cnt
       FROM
         cache_profile cp,
         cache_document cd,
         cache_field cf,
         cache_profile_has_cache_document cphcd,
         cache_document_has_cache_field cdhcf
      WHERE cp.id = cphcd.cache_profile_id
      AND cphcd.cache_document_id = cd.id
      AND cd.id = cdhcf.cache_document_id
      AND cdhcf.cache_field_id = cf.id
      AND cf.id IN :field_ids
      GROUP BY cp.id
     )
     GROUP BY id
   ) agg
WHERE cp.id = agg.id
AND cp.id = p.cache_profile_id