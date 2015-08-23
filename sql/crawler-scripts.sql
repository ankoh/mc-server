-- Delete all Mendeley data
DELETE FROM mendeley_document;
DELETE FROM mendeley_profile;

-- Delete all associations between profiles, documents and fields
-- They will be set with the new relations
DELETE FROM cache_document_has_cache_field;
DELETE FROM cache_profile_has_cache_document;

