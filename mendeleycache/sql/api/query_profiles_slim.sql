-- noinspection SqlResolve
SELECT
   p.id,
   p.name,
   c.cnt
FROM
   cache_profile p,
   (
     SELECT p.id as id, count(*) as cnt
     FROM
      cache_profile p,
      cache_document d,
      cache_profile_has_cache_document phd
     WHERE p.id = phd.cache_profile_id
     AND d.id = phd.cache_document_id
     GROUP BY p.id
   ) c
WHERE p.id = c.id