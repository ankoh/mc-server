-- noinspection SqlResolve
SELECT
   d.id,
   d.title
FROM
   document d,
   cache_document cd,
   cache_profile cp,
   cache_field cf,
   cache_document_has_cache_field cdhcf,
   cache_profile_has_cache_document cphcd
WHERE d.cache_document_id = cd.id
AND cd.id = cdhcf.cache_document_id
AND cdhcf.cache_field_id = cf.id
AND cd.id = cphcd.cache_document_id
AND cphcd.cache_profile_id = cp.id
AND cf.id IN :field_ids
AND cp.id IN :profile_ids