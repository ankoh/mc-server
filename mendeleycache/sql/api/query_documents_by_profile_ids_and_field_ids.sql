-- noinspection SqlResolve
SELECT :select_attributes
FROM
  document d,
  cache_document cd,
  cache_profile cp,
  cache_field cf,
  cache_document_has_cache_field cdhcf,
  cache_profile_has_cache_document cphcd
WHERE d.id = cd.document_id
AND cd.id = cdhcf.cache_document_id
AND cdhcf.cache_field_id = cf.id
AND cd.id = cphcd.cache_document_id
AND cphcd.cache_profile_id = cp.id
AND cf.id IN :field_ids
AND cp.id IN :profile_ids
ORDER BY :order_by
LIMIT :query_limit