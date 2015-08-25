-- noinspection SqlResolve
SELECT
   cf.id,
   cf.title,
   agg.cnt
FROM 
   cache_field cf,
   ( 
      SELECT cf.id AS id, count(*) AS cnt
      FROM 
        cache_field cf,
        cache_document cd,
        cache_document_has_cache_field cdhcf
      WHERE cf.id = cdhcf.cache_document_id
      AND cdhcf.cache_document_id = cd.id
      GROUP BY cf.id
   ) agg
WHERE cf.id = agg.id