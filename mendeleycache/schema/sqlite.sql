-- Schema for SQLite

-- -----------------------------------------------------
-- Table mendeley_profile
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS mendeley_profile (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  cache_profile_id INTEGER NOT NULL,
  m_id VARCHAR(255) NOT NULL UNIQUE,
  m_first_name VARCHAR(35) NOT NULL,
  m_last_name VARCHAR(35) NOT NULL,
  m_display_name VARCHAR(80),
  m_link VARCHAR(255),
  FOREIGN KEY (cache_profile_id)
    REFERENCES cache_profile (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

-- -----------------------------------------------------
-- Table mendeley_document
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS mendeley_document (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  mendeley_profile_id INTEGER NOT NULL,
  cache_document_id INTEGER NOT NULL,
  m_core_id VARCHAR(255),
  m_core_title VARCHAR(255),
  m_core_type VARCHAR(45),
  m_core_created DATETIME,
  m_core_last_modified DATETIME,
  m_core_abstract TEXT,
  m_core_source VARCHAR(255),
  m_core_year SMALLINT,
  m_core_authors TEXT,
  m_core_keywords TEXT,
  m_tags_tags TEXT,
  derived_bibtex TEXT,
  FOREIGN KEY (cache_document_id)
    REFERENCES cache_document (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  FOREIGN KEY (mendeley_profile_id)
    REFERENCES mendeley_profile (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

CREATE INDEX mendeley_document_cache_document_id on mendeley_document(cache_document_id);
CREATE INDEX mendeley_document_mendeley_profile_id on mendeley_document(mendeley_profile_id);

-- -----------------------------------------------------
-- Table cache_profile
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS cache_profile (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  unified_name VARCHAR(255) NOT NULL UNIQUE,
  mendeley_profile_id INTEGER UNIQUE,
  FOREIGN KEY (mendeley_profile_id)
    REFERENCES mendeley_profile (id)
    ON DELETE SET NULL
    ON UPDATE CASCADE);

-- -----------------------------------------------------
-- Table cache_document
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS cache_document (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  unified_title VARCHAR(255) NOT NULL UNIQUE,
  mendeley_document_id INTEGER UNIQUE,
  FOREIGN KEY (mendeley_document_id)
    REFERENCES mendeley_document (id)
    ON DELETE SET NULL
    ON UPDATE CASCADE);

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

CREATE INDEX cache_profile_has_cache_document_profile_id on cache_profile_has_cache_document(cache_profile_id);
CREATE INDEX cache_profile_has_cache_document_document_id on cache_profile_has_cache_document(cache_document_id);

-- -----------------------------------------------------
-- Table document_access_log
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS document_access_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  type VARCHAR(45) NOT NULL DEFAULT 'file',
  date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP);


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

CREATE INDEX document_access_log_has_cache_document_log_id on document_access_log_has_cache_document(document_access_log_id);
CREATE INDEX document_access_log_has_cache_document_document_id on document_access_log_has_cache_document(cache_document_id);


-- -----------------------------------------------------
-- Table field_access_log
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS field_access_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date DATETIME DEFAULT CURRENT_TIMESTAMP);


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

CREATE INDEX field_access_log_has_cache_field_log_id on field_access_log_has_cache_field(field_access_log_id);
CREATE INDEX field_access_log_has_cache_field_field_id on field_access_log_has_cache_field(cache_field_id);