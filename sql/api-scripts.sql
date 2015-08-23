-- Query Fields and the number of publications that belong to it
-- API call: GET /fields
SELECT
	f.id,
	f.title,
	c.cnt
FROM
	cache_field f,
	(
		SELECT f.id as id, count(*) as cnt
		FROM
			cache_field f,
			cache_document d,
			cache_document_has_cache_field dhf
		WHERE f.id = dhf.cache_document_id
		AND dhf.cache_document_id = d.id
		GROUP BY f.id
	) c
WHERE f.id = c.id;

-- Query Profiles by either profile id or field id
-- API call: GET /profiles
SELECT
	mp,
	c.cnt
FROM 
	cache_profile p,
	mendeley_profile mp,
	(
		(
			-- Query Profiles by profile id
			SELECT p.id as p_id, count(*) as cnt
			FROM
				cache_profile p,
				cache_document d,
				cache_field f,
				cache_profile_has_cache_document phd,
				cache_document_has_cache_field dhf
			WHERE p.id = phd.cache_profile_id
			AND phd.cache_document_id = d.id
			AND d.id = dhf.cache_document_id
			AND dhf.cache_field_id = f.id
			AND p.id IN (
				1234,
			    5678,
			    9101112
			)
			GROUP BY p.id
		)
		UNION
		(
			-- Query profiles by field id
			SELECT p.id as p_id, count(*) as cnt
			FROM
				cache_profile p,
				cache_document d,
				cache_field f,
				cache_profile_has_cache_document phd,
				cache_document_has_cache_field dhf
			WHERE p.id = phd.cache_profile_id
			AND phd.cache_document_id = d.id
			AND d.id = dhf.cache_document_id
			AND dhf.cache_field_id = f.id
			AND f.id IN (
				1234,
			    5678,
			    9101112
			)
			GROUP BY p.id
		)
	) c
WHERE p.id = c.id
AND p.id = mp.cache_profile_id;


-- Query publications by research_field AND profile id
-- API call: GET /publications
SELECT
	d.id,
	d.title
FROM 
	mendeley_document md,
	cache_document d,
	cache_profile p
	cache_field f,
	cache_document_has_cache_field dhf,
	cache_profile_has_cache_document phd
WHERE md.cache_document_id = d.id
AND d.id = dhf.cache_document_id
AND dhf.cache_field_id = f.id
AND d.id = phd.cache_document_id
AND phd.cache_profile_id = p.id
AND f.id IN (
	1234
)
AND p.id IN (
	1234
);