-- noinspection SqlResolve
REPLACE
INTO mendeley_documents
  (
    unified_title,
    m_core_id,
    m_core_profile_id,
    m_core_title,
    m_core_type,
    m_core_created,
    m_core_last_modified,
    m_core_abstract,
    m_core_source,
    m_core_year,
    m_core_authors,
    m_core_keywords,
    m_tags_tags,
    derived_bibtex
  )
VALUES
  :mendeley_documents