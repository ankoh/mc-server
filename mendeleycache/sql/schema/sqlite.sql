-- Schema for SQLite

-- -----------------------------------------------------
-- Table profile
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS profile (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  mendeley_id VARCHAR(255) UNIQUE NOT NULL,
  cache_profile_id VARCHAR(255) NOT NULL,
  first_name VARCHAR(35) NOT NULL,
  last_name VARCHAR(35) NOT NULL,
  display_name VARCHAR(80),
  link VARCHAR(255),
  FOREIGN KEY (cache_profile_id)
    REFERENCES cache_profile (id)
    ON DELETE SET NULL
    ON UPDATE CASCADE);

-- Foreign key profile -> cache_profile
CREATE INDEX profile_cache_profile_id ON profile(cache_profile_id);

-- -----------------------------------------------------
-- Table document
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS document (
  id INTEGER PRIMARY KEY AUTOINCREMENT ,
  mendeley_id VARCHAR(255) UNIQUE NOT NULL,
  cache_document_id VARCHAR(255) NOT NULL,
  owner_mendeley_id VARCHAR(255) NOT NULL,
  title VARCHAR(255),
  doc_type VARCHAR(45),
  created DATETIME,
  last_modified DATETIME,
  abstract TEXT,
  source VARCHAR(255),
  pub_year SMALLINT,
  authors TEXT,
  keywords TEXT,
  tags TEXT,
  derived_bibtex TEXT,
  FOREIGN KEY (cache_document_id)
    REFERENCES cache_document (id)
    ON DELETE SET NULL
    ON UPDATE CASCADE);

-- Foreign key document -> cache_document
CREATE INDEX document_cache_document_id ON document(cache_document_id);
CREATE INDEX document_last_modified ON document(last_modified DESC);

-- -----------------------------------------------------
-- Table cache_profile
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS cache_profile (
  id VARCHAR(255) PRIMARY KEY ,
  profile_id INTEGER,
  name VARCHAR(255) NOT NULL,
  FOREIGN KEY (profile_id)
    REFERENCES profile (id)
    ON DELETE SET NULL
    ON UPDATE CASCADE);

-- Foreign key cache_profile -> profile
CREATE INDEX cache_profile_profile_id ON cache_profile(profile_id);

-- -----------------------------------------------------
-- Table cache_document
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS cache_document (
  id VARCHAR(255) PRIMARY KEY,
  document_id INTEGER,
  title VARCHAR(255) NOT NULL,
  FOREIGN KEY (document_id)
    REFERENCES document (id)
    ON DELETE SET NULL
    ON UPDATE CASCADE);

-- Foreign key cache_document -> document
CREATE INDEX cache_document_document_id ON cache_document(document_id);


-- -----------------------------------------------------
-- Table cache_field
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS cache_field (
  id VARCHAR(255) PRIMARY KEY,
  title VARCHAR(255) NOT NULL);

-- -----------------------------------------------------
-- Table cache_profile_has_cache_document
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS cache_profile_has_cache_document (
  cache_profile_id VARCHAR(255) NOT NULL,
  cache_document_id VARCHAR(255) NOT NULL,
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
-- Table cache_document_has_cache_field
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS cache_document_has_cache_field (
  cache_document_id VARCHAR(255) NOT NULL,
  cache_field_id VARCHAR(255) NOT NULL,
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