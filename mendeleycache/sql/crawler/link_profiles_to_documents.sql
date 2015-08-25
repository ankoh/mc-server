-- Create temporary table
-- noinspection SqlResolve
CREATE TEMPORARY TABLE IF NOT EXISTS temp_profile_to_documents (
  unified_profile_name VARCHAR(255) NOT NULL,
  unified_document_title VARCHAR(255) NOT NULL,
  PRIMARY KEY(unified_profile_name, unified_document_title));


-- Spool data into temporary table
-- noinspection SqlResolve
INSERT
INTO temp_profile_to_documents
(
  unified_profile_name,
  unified_document_title
)
VALUES
  :profiles_to_documents;

-- Delete existing links
-- noinspection SqlResolve
DELETE FROM cache_profile_has_cache_document;


-- Create associations via join
-- noinspection SqlResolve
INSERT
INTO cache_profile_has_cache_document
(
  cache_profile_id,
  cache_document_id
)
SELECT
  cp.id,
  cd.id
FROM
  cache_profile cp,
  cache_document cd,
  temp_profile_to_documents ptd
WHERE cp.unified_name = ptd.unified_profile_name
AND cd.unified_title = ptd.unified_document_title;


-- Drop temporary table
-- noinspection SqlResolve
DROP TABLE IF EXISTS temp_profile_to_documents;