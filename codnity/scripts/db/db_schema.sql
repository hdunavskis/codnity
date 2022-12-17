CREATE DATABASE codnity;
CREATE USER codnity;
ALTER ROLE codnity SET client_encoding TO 'utf8';
ALTER ROLE codnity SET default_transaction_isolation TO 'read committed';
ALTER ROLE codnity SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE codnity TO codnity;