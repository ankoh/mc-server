-- noinspection SqlResolve
REPLACE
INTO profile
  (
    mid,
    unified_name,
    first_name,
    last_name,
    display_name,
    link
  )
VALUES
  :profiles;