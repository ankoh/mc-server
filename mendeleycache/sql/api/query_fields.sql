-- noinspection SqlResolve
SELECT
   f.id, 
   f.title, 
   c.cnt 
FROM 
   cache_field f, 
   ( 
      SELECT f.id as id, count(*) as cnt 
      FROM 
        cache_field f, 
        cache_document d, 
        cache_document_has_cache_field dhf 
      WHERE f.id = dhf.cache_document_id 
      AND dhf.cache_document_id = d.id 
      GROUP BY f.id 
   ) c 
WHERE f.id = c.id 