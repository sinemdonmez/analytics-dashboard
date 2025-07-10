CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE sessions (
  id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(id),
  start_time TIMESTAMP,
  end_time TIMESTAMP,
  device TEXT
);

CREATE TABLE events (
  id SERIAL PRIMARY KEY,
  session_id INT REFERENCES sessions(id),
  event_type TEXT,
  event_time TIMESTAMP,
  level INT,
  purchase_amount NUMERIC
);

