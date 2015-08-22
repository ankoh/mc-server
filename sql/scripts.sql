# Query Fields and the number of publications that belong to it
SELECT f.id, f.title, c.cnt
FROM cache_field f, (
	SELECT f.id as id, count(*) as cnt
	FROM cache_field f, cache_document_has_cache_field dhf, cache_document d
	WHERE f.id = dhf.cache_document_id
	AND dhf.cache_document_id = d.id
	GROUP BY f.id
) c
WHERE f.id = c.id;

# Query Profiles by either profile id or field id
SELECT p, c.cnt
FROM 
	cache_profile p,
	(
		(
			# Query Profiles by profile id
			SELECT p.id as p_id, count(*) as cnt
			FROM
				cache_profile p,
				cache_document d,
				cache_profile_has_cache_document phd,
				cache_document_has_cache_field dhf,
				cache_field f
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
			# Query profiles by field id
			SELECT p.id as p_id, count(*) as cnt
			FROM
				cache_profile p,
				cache_document d,
				cache_profile_has_cache_document phd,
				cache_document_has_cache_field dhf,
				cache_field f
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
WHERE o_p.id = c.id


# Query publications by research_field AND profile id
