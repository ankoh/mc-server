-- noinspection SqlResolve
INSERT
INTO update_log
  (
    ip,
    profiles,
    documents,
    unified_profiles,
    unified_documents,
    fields,
    field_links
  )
VALUES
  :log_entry