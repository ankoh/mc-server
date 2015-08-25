-- Schema for SQLite

-- -----------------------------------------------------
-- Table profile
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS profile (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  mid VARCHAR(255) UNIQUE NOT NULL,
  cache_profile_id INTEGER,
  unified_name VARCHAR(255) NOT NULL,
  first_name VARCHAR(35) NOT NULL,
  last_name VARCHAR(35) NOT NULL,
  display_name VARCHAR(80),
  link VARCHAR(255),
  FOREIGN KEY (cache_profile_id)
    REFERENCES cache_profile (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

-- Foreign key profile -> cache_profile
CREATE INDEX profile_cache_profile_id ON profile(cache_profile_id);
-- The index on unified_name is needed to resolve the right cache_profile(id)
CREATE INDEX profile_unified_name ON profile(unified_name);

-- -----------------------------------------------------
-- Table document
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS document (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  mid VARCHAR(255) UNIQUE NOT NULL,
  cache_document_id INTEGER,
  unified_title VARCHAR(255),
  title VARCHAR(255),
  owner_mid VARCHAR(255) NOT NULL,
  type VARCHAR(45),
  created DATETIME,
  last_modified DATETIME,
  abstract TEXT,
  source VARCHAR(255),
  year SMALLINT,
  authors TEXT,
  keywords TEXT,
  tags TEXT,
  derived_bibtex TEXT,
  FOREIGN KEY (cache_document_id)
    REFERENCES cache_document (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

-- Foreign key document -> cache_document
CREATE INDEX document_cache_document_id ON document(cache_document_id);
-- The index on unified_title is needed to resolve the right cache_document(id)
CREATE INDEX document_unified_title ON document(unified_title);

-- -----------------------------------------------------
-- Table cache_profile
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS cache_profile (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  profile_id INTEGER,
  profile_mid VARCHAR(255),
  name VARCHAR(255) NOT NULL,
  unified_name VARCHAR(255) NOT NULL UNIQUE,
  FOREIGN KEY (profile_id)
    REFERENCES profile (id)
    ON DELETE SET NULL
    ON UPDATE CASCADE);

-- Foreign key cache_profile -> profile
CREATE INDEX cache_profile_profile_id ON cache_profile(profile_id);
-- The index on profile_mid is needed to resolve the right profile
CREATE INDEX cache_profile_profile_mid ON cache_profile(profile_mid);

-- -----------------------------------------------------
-- Table cache_document
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS cache_document (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  document_id INTEGER,
  document_mid VARCHAR(255),
  title VARCHAR(255) NOT NULL,
  unified_title VARCHAR(255) NOT NULL UNIQUE,
  FOREIGN KEY (document_id)
    REFERENCES document (id)
    ON DELETE SET NULL
    ON UPDATE CASCADE);

-- Foreign key cache_document -> document
CREATE INDEX cache_document_document_id ON cache_document(document_id);
-- The index on document_mid is needed to resolve the right document
CREATE INDEX cache_document_document_mid ON cache_document(document_mid);


-- -----------------------------------------------------
-- Table cache_field
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS cache_field (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title VARCHAR(255) NOT NULL,
  unified_title VARCHAR(255) NOT NULL UNIQUE);


-- -----------------------------------------------------
-- Table cache_document_has_cache_field
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS cache_document_has_cache_field (
  cache_document_id INTEGER NOT NULL,
  cache_field_id INTEGER NOT NULL,
  PRIMARY KEY (cache_document_id, cache_field_id),
  FOREIGN KEY (cache_document_id)
    REFERENCES cache_document (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  FOREIGN KEY (cache_field_id)
    REFERENCES cache_field (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

-- Foreign keys for cache_document_has_cache_field -> cache_field
-- and cache_document_has_cache_field -> cache_document
CREATE INDEX cache_document_has_cache_field_field_id on cache_document_has_cache_field(cache_field_id);
CREATE INDEX cache_document_has_cache_field_document_id on cache_document_has_cache_field(cache_document_id);


-- -----------------------------------------------------
-- Table cache_profile_has_cache_document
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS cache_profile_has_cache_document (
  cache_profile_id INTEGER NOT NULL,
  cache_document_id INTEGER NOT NULL,
  PRIMARY KEY (cache_profile_id, cache_document_id),
  FOREIGN KEY (cache_profile_id)
    REFERENCES cache_profile (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  FOREIGN KEY (cache_document_id)
    REFERENCES cache_document (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

-- Foreign keys for cache_profile_has_cache_document -> cache_profile
-- and cache_profile_has_cache_document -> cache_document
CREATE INDEX cache_profile_has_cache_document_profile_id on cache_profile_has_cache_document(cache_profile_id);
CREATE INDEX cache_profile_has_cache_document_document_id on cache_profile_has_cache_document(cache_document_id);

-- -----------------------------------------------------
-- Table document_access_log
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS document_access_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  type VARCHAR(45) NOT NULL DEFAULT 'file',
  date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP);

-- I need to filter for the different document access types
CREATE INDEX document_access_log_type ON document_access_log(type);

-- The document access logs need to be ordered for the query (last 7 weeks)
CREATE INDEX document_access_log_date ON document_access_log(date DESC);

-- -----------------------------------------------------
-- Table document_access_log_has_cache_document
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS document_access_log_has_cache_document (
  document_access_log_id INTEGER NOT NULL,
  cache_document_id INTEGER NOT NULL,
  PRIMARY KEY (document_access_log_id, cache_document_id),
  FOREIGN KEY (document_access_log_id)
    REFERENCES document_access_log (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  FOREIGN KEY (cache_document_id)
    REFERENCES cache_document (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

-- Foreign keys for document_access_log_has_cache_document -> cache_document_access_log
-- and document_access_log_has_cache_document -> cache_document
CREATE INDEX document_access_log_has_cache_document_log_id on document_access_log_has_cache_document(document_access_log_id);
CREATE INDEX document_access_log_has_cache_document_document_id on document_access_log_has_cache_document(cache_document_id);


-- -----------------------------------------------------
-- Table field_access_log
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS field_access_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date DATETIME DEFAULT CURRENT_TIMESTAMP);

-- The field access logs need to be ordered for the query (last 7 weeks)
CREATE INDEX field_access_log_date ON field_access_log(date DESC);


-- -----------------------------------------------------
-- Table field_access_log_has_cache_field
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS field_access_log_has_cache_field (
  field_access_log_id INTEGER NOT NULL,
  cache_field_id INTEGER NOT NULL,
  PRIMARY KEY (field_access_log_id, cache_field_id),
  FOREIGN KEY (field_access_log_id)
    REFERENCES field_access_log (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  FOREIGN KEY (cache_field_id)
    REFERENCES cache_field (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

-- Foreign keys for field_access_log_has_cache_field -> field_access_log
-- and field_access_log_has_cache_field -> cache_field
CREATE INDEX field_access_log_has_cache_field_log_id on field_access_log_has_cache_field(field_access_log_id);
CREATE INDEX field_access_log_has_cache_field_field_id on field_access_log_has_cache_field(cache_field_id);