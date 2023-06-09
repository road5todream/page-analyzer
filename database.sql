DROP TABLE IF EXISTS urls;

CREATE TABLE IF NOT EXISTS urls (
  id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  name VARCHAR(255) UNIQUE NOT NULL,
  created_at DATE DEFAULT now()
);

DROP TABLE IF EXISTS url_checks;

CREATE TABLE IF NOT EXISTS url_checks (
  id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  url_id bigint REFERENCES urls(id),
  status_code SMALLINT,
  h1 VARCHAR(255),
  title VARCHAR(255),
  description VARCHAR,
  created_at DATE DEFAULT now()
);
