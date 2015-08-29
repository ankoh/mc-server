-- noinspection SqlResolve
DELETE FROM cache_document_has_cache_field;

-- noinspection SqlResolve
REPLACE
INTO cache_document_has_cache_field
(
  cache_document_id,
  cache_field_id
)
VALUES
  :documents_to_fields;
