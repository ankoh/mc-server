-- noinspection SqlResolve
SELECT
   *
FROM
  (
    SELECT
      'profile' AS table_name,
      COUNT(*) AS cnt
    FROM profile

    UNION ALL

    SELECT
      'document' AS table_name,
      COUNT(*) AS cnt
    FROM document

    UNION ALL

    SELECT
      'cache_profile' AS table_name,
      COUNT(*) AS cnt
    FROM cache_profile

    UNION ALL

    SELECT
      'cache_document' AS table_name,
      COUNT(*) AS cnt
    FROM cache_document

    UNION ALL

    SELECT
      'cache_field' AS table_name,
      COUNT(*) AS cnt
    FROM cache_field

    UNION ALL

    SELECT
      'cache_profile_has_cache_document' AS table_name,
      COUNT(*) AS cnt
    FROM cache_profile_has_cache_document

    UNION ALL

    SELECT
      'cache_document_has_cache_field' as table_name,
      COUNT(*) AS cnt
    FROM cache_document_has_cache_field
  ) table_stats