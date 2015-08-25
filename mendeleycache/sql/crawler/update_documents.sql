-- noinspection SqlResolve
REPLACE
INTO document
  (
    mid,
    owner_mid,
    unified_title,
    title,
    doc_type,
    created,
    last_modified,
    abstract,
    source,
    pub_year,
    authors,
    keywords,
    tags,
    derived_bibtex
  )
VALUES
  :documents