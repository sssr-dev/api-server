-- noinspection SqlResolveForFile
DROP TABLE IF EXISTS links;
DROP TABLE IF EXISTS github_counter;
DROP TABLE IF EXISTS tokens;

CREATE TABLE links (
    id                  INTEGER PRIMARY KEY ASC AUTOINCREMENT,
    from_ip             STRING  NOT NULL,
    unix_timestamp      DOUBLE  NOT NULL,
    url_raw             STRING  NOT NULL,
    url_check_banned    STRING,
    url_short           STRING  UNIQUE NOT NULL,
    counter             INTEGER DEFAULT (1)
);

CREATE TABLE github_counter (
    id                  INTEGER PRIMARY KEY ASC AUTOINCREMENT,
    count_type STRING   UNIQUE DEFAULT "profile",
    count_object STRING UNIQUE NOT NULL,
    counter             INTEGER DEFAULT (0)
);

CREATE TABLE tokens (
    id                  INTEGER PRIMARY KEY ASC AUTOINCREMENT,
    from_ip             STRING  NOT NULL,
    username            STRING  NOT NULL,
    token               STRING  NOT NULL,
    expires_in          INTEGER NOT NULL,
    unix_timestamp      DOUBLE  NOT NULL
);

INSERT INTO links (from_ip, unix_timestamp, url_raw, url_check_banned, url_short) VALUES ("127.0.0.1", 0, "https://t.me/SantaSpeen", "https://t.me/SantaSpeen", "admin");
INSERT INTO links (from_ip, unix_timestamp, url_raw, url_check_banned, url_short) VALUES ("127.0.0.1", 0, "https://t.me/SantaSpeen", "https://t.me/SantaSpeen", "ADMIN");
