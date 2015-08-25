-- noinspection SqlResolve
INSERT
INTO cache_document_has_cache_field
(
  cache_document_id,
  cache_field_id
)
SELECT
  cd.id,
  cf.id
FROM
  cache_document cd,
  cache_field cf
WHERE (cd.unified_title, cf.unified_title)
IN :document_has_field