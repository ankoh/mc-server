-- noinspection SqlResolve
SELECT
   mp,
   c.cnt
FROM
   cache_profile p,
   mendeley_profile mp,
   (
     SELECT id, MAX(cnt) as cnt
     FROM
     (
       (
        SELECT p.id as id , count(*) as cnt
        FROM
           cache_profile p,
           cache_document d,
           cache_profile_has_cache_document phd
        WHERE p.id = phd.cache_profile_id
        AND phd.cache_document_id = d.id
        AND p.id IN :profile_ids
        GROUP BY p.id
       )
       UNION ALL
       (
        SELECT p.id as id, count(*) as cnt
         FROM
           cache_profile p,
           cache_document d,
           cache_field f,
           cache_profile_has_cache_document phd,
           cache_document_has_cache_field dhf
        WHERE p.id = phd.cache_profile_id
        AND phd.cache_document_id = d.id
        AND d.id = dhf.cache_document_id
        AND dhf.cache_field_id = f.id
        AND f.id IN :field_ids
        GROUP BY p.id
       )
     )
     GROUP BY id
   ) c
WHERE p.id = c.id
AND p.id = mp.cache_profile_id