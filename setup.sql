CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS meta (
    key VARCHAR(255) PRIMARY KEY,
    value VARCHAR(255) NOT NULL
);
INSERT INTO meta (key, value) VALUES ('version', '1.0');
INSERT INTO meta (key, value) VALUES ('configured', 'true');