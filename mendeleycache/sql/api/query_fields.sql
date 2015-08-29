-- noinspection SqlResolve
SELECT
   cf.id      AS id,
   cf.title   AS title,
   agg.cnt    AS cnt
FROM 
   cache_field cf,
   ( 
      SELECT cf.id AS id, COUNT(*) AS cnt
      FROM 
        cache_field cf,
        cache_document cd,
        cache_document_has_cache_field cdhcf
      WHERE cf.id = cdhcf.cache_field_id
      AND cdhcf.cache_document_id = cd.id
      GROUP BY cf.id
   ) agg
WHERE cf.id = agg.id