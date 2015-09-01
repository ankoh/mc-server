-- noinspection SqlResolve
SELECT DISTINCT
  cd.id             AS id,
  d.mendeley_id     AS mendeley_id,
  d.title           AS title,
  d.doc_type        AS doc_type,
  d.last_modified   AS last_modified,
  d.abstract        AS abstract,
  d.source          AS source,
  d.pub_year        AS pub_year,
  d.authors         AS authors,
  d.keywords        AS keywords,
  d.tags            AS tags,
  d.derived_bibtex  AS derived_bibtex
FROM
  document d,
  cache_document cd,
  cache_field cf,
  cache_document_has_cache_field cdhcf
WHERE d.id = cd.document_id
AND cd.id = cdhcf.cache_document_id
AND cdhcf.cache_field_id = cf.id
AND cf.id IN :field_ids
ORDER BY :order_by
LIMIT :query_limit