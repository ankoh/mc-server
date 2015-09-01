-- noinspection SqlResolve
SELECT :select_attributes
FROM
  document d,
  cache_document cd
WHERE d.id = cd.document_id
ORDER BY :order_by
LIMIT :query_limit