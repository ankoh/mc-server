-- noinspection SqlResolve
SELECT *
FROM
  profile p
WHERE p.first_name = :firstname
AND p.last_name = :lastname
