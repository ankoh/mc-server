-- noinspection SqlResolve
DELETE FROM document;

-- noinspection SqlResolve
REPLACE
INTO document
  (
    mendeley_id,
    cache_document_id,
    owner_mendeley_id,
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
    website,
    derived_bibtex
  )
VALUES
  :documents;

-- noinspection SqlResolve
CREATE TEMPORARY TABLE IF NOT EXISTS temp_cache_document_ids (
  id VARCHAR(255) NOT NULL,
  document_id INTEGER
);

-- noinspection SqlResolve
INSERT INTO temp_cache_document_ids (id, document_id)
SELECT
  d.cache_document_id   AS id,
  d.id                  AS document_id
FROM
  document d,
  (
    SELECT
      d.cache_document_id AS id,
      MAX(d.last_modified) AS date
    FROM document d
    GROUP BY d.cache_document_id
  ) agg
WHERE d.cache_document_id = agg.id
AND d.last_modified = agg.date;

-- noinspection SqlResolve
UPDATE
  cache_document
SET
  document_id = (SELECT temp_cache_document_ids.document_id
                 FROM temp_cache_document_ids
                 WHERE temp_cache_document_ids.id = cache_document.id
                 LIMIT 1);

-- noinspection SqlResolve
DROP TABLE IF EXISTS temp_cache_document_ids;