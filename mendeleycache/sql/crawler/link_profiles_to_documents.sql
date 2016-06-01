-- noinspection SqlResolve
DELETE FROM cache_profile_has_cache_document;

-- noinspection SqlResolve
REPLACE
INTO cache_profile_has_cache_document
(
  cache_profile_id,
  cache_document_id
)
VALUES
  (?,?);
