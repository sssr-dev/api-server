CREATE TABLE github_counter (
    id      INTEGER PRIMARY KEY
                    UNIQUE,
    profile STRING  UNIQUE
                    NOT NULL,
    counter INTEGER DEFAULT (0)
);

CREATE TABLE links (
    id               INTEGER PRIMARY KEY ASC AUTOINCREMENT,
    from_ip          STRING  NOT NULL,
    unix_timestamp   DOUBLE  NOT NULL,
    url_raw          STRING  NOT NULL,
    url_check_banned STRING,
    url_short        STRING  UNIQUE
                             NOT NULL,
    counter          INTEGER DEFAULT (0)
);
