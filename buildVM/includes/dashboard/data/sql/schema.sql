CREATE TABLE aip (id BIGINT AUTO_INCREMENT, identifier VARCHAR(255), dateaccepted DATETIME NOT NULL, location VARCHAR(255), dip_location VARCHAR(255), PRIMARY KEY(id)) ENGINE = INNODB;
CREATE TABLE aip_status (id BIGINT AUTO_INCREMENT, name VARCHAR(255) NOT NULL UNIQUE, icon VARCHAR(255), PRIMARY KEY(id)) ENGINE = INNODB;
CREATE TABLE aip_status_log (id BIGINT AUTO_INCREMENT, aip_id BIGINT NOT NULL, aip_status_id BIGINT NOT NULL, opened_at DATETIME NOT NULL, closed_at DATETIME, INDEX aip_id_idx (aip_id), INDEX aip_status_id_idx (aip_status_id), PRIMARY KEY(id)) ENGINE = INNODB;
CREATE TABLE file (id BIGINT AUTO_INCREMENT, sip_id BIGINT NOT NULL, aip_id BIGINT, identifier VARCHAR(255), title VARCHAR(255), original_filename VARCHAR(255), clean_filename VARCHAR(255), filepath VARCHAR(255), date DATE, checksum VARCHAR(255), checksum_type VARCHAR(255), INDEX sip_id_idx (sip_id), INDEX aip_id_idx (aip_id), PRIMARY KEY(id)) ENGINE = INNODB;
CREATE TABLE file_status (id BIGINT AUTO_INCREMENT, name VARCHAR(255) NOT NULL UNIQUE, icon VARCHAR(255), PRIMARY KEY(id)) ENGINE = INNODB;
CREATE TABLE file_status_log (id BIGINT AUTO_INCREMENT, file_id BIGINT NOT NULL, file_status_id BIGINT NOT NULL, opened_at DATETIME NOT NULL, closed_at DATETIME, INDEX file_id_idx (file_id), INDEX file_status_id_idx (file_status_id), PRIMARY KEY(id)) ENGINE = INNODB;
CREATE TABLE format (id BIGINT AUTO_INCREMENT, name VARCHAR(255) NOT NULL UNIQUE, extension VARCHAR(255), mime_type VARCHAR(255), registry_uri VARCHAR(255), PRIMARY KEY(id)) ENGINE = INNODB;
CREATE TABLE format_role (format_id BIGINT, file_id BIGINT, role VARCHAR(255), PRIMARY KEY(format_id, file_id)) ENGINE = INNODB;
CREATE TABLE sip (id BIGINT AUTO_INCREMENT, identifier VARCHAR(255), title VARCHAR(255) NOT NULL, datereceived DATETIME NOT NULL, provenance VARCHAR(255), partof VARCHAR(255), PRIMARY KEY(id)) ENGINE = INNODB;
CREATE TABLE sip_status (id BIGINT AUTO_INCREMENT, name VARCHAR(255) NOT NULL UNIQUE, icon VARCHAR(255), PRIMARY KEY(id)) ENGINE = INNODB;
CREATE TABLE sip_status_log (id BIGINT AUTO_INCREMENT, sip_id BIGINT NOT NULL, sip_status_id BIGINT NOT NULL, opened_at DATETIME NOT NULL, closed_at DATETIME, INDEX sip_id_idx (sip_id), INDEX sip_status_id_idx (sip_status_id), PRIMARY KEY(id)) ENGINE = INNODB;
ALTER TABLE aip_status_log ADD CONSTRAINT aip_status_log_aip_status_id_aip_status_id FOREIGN KEY (aip_status_id) REFERENCES aip_status(id) ON DELETE CASCADE;
ALTER TABLE aip_status_log ADD CONSTRAINT aip_status_log_aip_id_aip_id FOREIGN KEY (aip_id) REFERENCES aip(id) ON DELETE CASCADE;
ALTER TABLE file ADD CONSTRAINT file_sip_id_sip_id FOREIGN KEY (sip_id) REFERENCES sip(id) ON DELETE CASCADE;
ALTER TABLE file ADD CONSTRAINT file_aip_id_aip_id FOREIGN KEY (aip_id) REFERENCES aip(id) ON DELETE CASCADE;
ALTER TABLE file_status_log ADD CONSTRAINT file_status_log_file_status_id_file_status_id FOREIGN KEY (file_status_id) REFERENCES file_status(id) ON DELETE CASCADE;
ALTER TABLE file_status_log ADD CONSTRAINT file_status_log_file_id_file_id FOREIGN KEY (file_id) REFERENCES file(id) ON DELETE CASCADE;
ALTER TABLE format_role ADD CONSTRAINT format_role_format_id_format_id FOREIGN KEY (format_id) REFERENCES format(id) ON DELETE CASCADE;
ALTER TABLE format_role ADD CONSTRAINT format_role_file_id_file_id FOREIGN KEY (file_id) REFERENCES file(id) ON DELETE CASCADE;
ALTER TABLE sip_status_log ADD CONSTRAINT sip_status_log_sip_status_id_sip_status_id FOREIGN KEY (sip_status_id) REFERENCES sip_status(id) ON DELETE CASCADE;
ALTER TABLE sip_status_log ADD CONSTRAINT sip_status_log_sip_id_sip_id FOREIGN KEY (sip_id) REFERENCES sip(id) ON DELETE CASCADE;
