-- noinspection SqlResolve
SELECT
  cp.id           AS id,
  p.mendeley_id   AS mendeley_id,
  p.first_name    AS first_name,
  p.last_name     AS last_name,
  p.display_name  AS display_name,
  p.link          AS link,
  agg.cnt         AS cnt
FROM
   cache_profile cp,
   profile p,
   (
     SELECT id_cnts.id AS id, MAX(id_cnts.cnt) AS cnt
     FROM
     (
      SELECT
        cp.id as id,
        CASE WHEN cnts.cnt IS NULL THEN 0 ELSE cnts.cnt END AS cnt
      FROM
        cache_profile cp
        LEFT OUTER JOIN
        (
          SELECT
            cp.id    AS id,
            COUNT(*) AS cnt
          FROM
            cache_profile cp,
            cache_document cd,
            cache_profile_has_cache_document cphcd
          WHERE cp.id = cphcd.cache_profile_id
          AND cphcd.cache_document_id = cd.id
          GROUP BY cp.id
        ) AS cnts
        ON cp.id = cnts.id
      WHERE cp.id IN :profile_ids

      UNION ALL

      SELECT cp.id AS id, COUNT(DISTINCT(cd.id)) AS cnt
       FROM
         cache_profile cp,
         cache_document cd,
         cache_field cf,
         cache_profile_has_cache_document cphcd,
         cache_document_has_cache_field cdhcf
      WHERE cp.id = cphcd.cache_profile_id
      AND cphcd.cache_document_id = cd.id
      AND cd.id = cdhcf.cache_document_id
      AND cdhcf.cache_field_id = cf.id
      AND cf.id IN :field_ids
      GROUP BY cp.id
     ) AS id_cnts
     GROUP BY id_cnts.id
   ) AS agg
WHERE cp.id = agg.id
AND cp.id = p.cache_profile_id