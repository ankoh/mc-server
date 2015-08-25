-- noinspection SqlResolve
DELETE FROM profile;

-- noinspection SqlResolve
INSERT
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