-- noinspection SqlResolve
REPLACE
INTO mendeley_profiles
  (
    cache_profile_id,
    m_id,
    m_first_name,
    m_last_name,
    m_display_name,
    m_link
  )
VALUES
  :mendeley_profiles