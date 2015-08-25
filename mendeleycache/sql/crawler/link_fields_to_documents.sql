-- Create temporary table
-- noinspection SqlResolve
CREATE TEMPORARY TABLE IF NOT EXISTS temp_fields_to_documents (
  unified_field_title VARCHAR(255) NOT NULL,
  unified_document_title VARCHAR(255) NOT NULL,
  PRIMARY KEY(unified_field_title, unified_document_title));


-- Spool data into temporary table
-- noinspection SqlResolve
INSERT
INTO temp_fields_to_documents
(
  unified_field_title,
  unified_document_title
)
VALUES
  :fields_to_documents;

-- Delete existing links
-- noinspection SqlResolve
DELETE FROM cache_document_has_cache_field;

-- Create associations via join
-- noinspection SqlResolve
INSERT
INTO cache_document_has_cache_field
(
  cache_document_id,
  cache_field_id
)
SELECT
  cd.id,
  cf.id
FROM
  cache_document cd,
  cache_field cf,
  temp_fields_to_documents ftd
WHERE cd.unified_title = ftd.unified_document_title
AND cf.unified_title = ftd.unified_field_title;


-- Drop temporary table
-- noinspection SqlResolve
DROP TABLE IF EXISTS temp_fields_to_documents;