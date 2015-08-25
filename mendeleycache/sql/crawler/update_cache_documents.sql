-- noinspection SqlResolve
REPLACE
INTO cache_document
  (
    document_mid,
    unified_title,
    title
  )
VALUES
  :cache_documents