-- noinspection SqlResolve
INSERT
INTO cache_profile_has_cache_document
(
  cache_profile_id,
  cache_document_id
)
SELECT
  p.id,
  d.id
FROM
  cache_profile p,
  cache_document d
WHERE (p.unified_name, d.unified_title)
IN :profile_has_document