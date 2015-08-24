-- noinspection SqlResolve
INSERT
INTO cache_document_has_cache_field
(
  cache_document_id,
  cache_field_id
)
SELECT
  d.id,
  f.id
FROM
  cache_document d,
  cache_field f
WHERE (d.unified_title, f.unified_title)
IN :document_has_field