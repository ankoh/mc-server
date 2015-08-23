-- noinspection SqlResolve
SELECT
   d.id,
   d.title
FROM
   mendeley_document md,
   cache_documendt d,
   cache_profile p,
   cache_field f,
   cache_document_has_cache_field dhf,
   cache_profile_has_cache_document phd
WHERE md.cache_document_id = d.id
AND d.id = dhf.cache_document_id
AND dhf.cache_field_id = f.id
AND d.id = phd.cache_document_id
AND phd.cache_profile_id = p.id
AND f.id in :fiel_ids
AND p.id in :profile_ids