-- noinspection SqlResolve
SELECT :select_attributes
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