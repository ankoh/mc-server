-- noinspection SqlResolve
DELETE FROM profile;

-- noinspection SqlResolve
INSERT
INTO profile
  (
    mendeley_id,
    cache_profile_id,
    first_name,
    last_name,
    display_name,
    link
  )
VALUES
  (?,?,?,?,?,?);

-- noinspection SqlResolve
CREATE TEMPORARY TABLE IF NOT EXISTS temp_cache_profile_ids (
  id VARCHAR(255) NOT NULL,
  profile_id INTEGER
);

-- noinspection SqlResolve
INSERT INTO temp_cache_profile_ids (id, profile_id)
SELECT
  p.cache_profile_id as id,
  p.id as profile_id
FROM
  profile p,
  (
    SELECT
      p.cache_profile_id as id,
      MAX(LENGTH(p.display_name)) AS length
    FROM profile p
    GROUP BY p.cache_profile_id
  ) agg
WHERE p.cache_profile_id = agg.id
AND LENGTH(p.display_name) = agg.length;

-- noinspection SqlResolve
UPDATE
  cache_profile
SET
  profile_id = (SELECT temp_cache_profile_ids.profile_id
                 FROM temp_cache_profile_ids
                 WHERE temp_cache_profile_ids.id = cache_profile.id
                 LIMIT 1);

-- noinspection SqlResolve
DROP TABLE IF EXISTS temp_cache_profile_ids;
