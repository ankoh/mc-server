-- noinspection SqlResolve
INSERT
INTO cache_profile_has_cache_document
(
  cache_profile_id,
  cache_document_id
)
SELECT
  cp.id,
  cd.id
FROM
  cache_profile cp,
  cache_document cd
WHERE (cp.unified_name, cd.unified_title)
IN :profile_has_document