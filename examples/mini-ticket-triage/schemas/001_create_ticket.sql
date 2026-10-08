CREATE TABLE ticket (
  id TEXT PRIMARY KEY,
  body TEXT NOT NULL,
  state TEXT NOT NULL,
  suggested_category TEXT,
  suggested_priority TEXT,
  confidence NUMERIC,
  final_category TEXT,
  final_priority TEXT,
  confirmed_by TEXT,
  analysis_version TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);
