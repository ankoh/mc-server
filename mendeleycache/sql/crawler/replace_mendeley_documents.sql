-- noinspection SqlResolve
REPLACE
INTO document
  (
    mid,
    owner_mid,
    unified_title,
    title,
    type,
    created,
    last_modified,
    abstract,
    source,
    year,
    authors,
    keywords,
    tags,
    derived_bibtex
  )
VALUES
  :documents