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
  d.website         AS website,
  d.derived_bibtex  AS derived_bibtex
FROM
  document d,
  cache_document cd,
  cache_profile cp,
  cache_profile_has_cache_document cphcd
WHERE d.id = cd.document_id
AND cd.id = cphcd.cache_document_id
AND cphcd.cache_profile_id = cp.id
AND cp.id IN :profile_ids
ORDER BY :order_by
LIMIT :query_limit