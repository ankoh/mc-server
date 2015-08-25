-- noinspection SqlResolve
REPLACE
INTO cache_documents
  (
    document_mid,
    unified_title,
    title
  )
VALUES
  :cache_documents