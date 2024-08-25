CREATE DATABASE short_url;
CREATE USER short_url_user WITH PASSWORD 'shorturlpassword';
ALTER ROLE short_url_user SET client_encoding TO 'utf8';
ALTER ROLE short_url_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE short_url_user SET timezone TO 'UTC';
ALTER DATABASE short_url OWNER TO short_url_user;
