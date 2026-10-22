-- quality.sqlite: structured data only, no free text (D-004). Safe to commit.
CREATE TABLE IF NOT EXISTS issues (
  key TEXT PRIMARY KEY,
  project TEXT, issuetype TEXT,
  created TEXT, resolved TEXT,
  status TEXT, status_category TEXT, resolution TEXT, priority TEXT,
  rnd_vp TEXT, team TEXT, bug_type TEXT,
  incidents INTEGER, impact_rank REAL,
  sf_association_count INTEGER, is_cfb INTEGER,
  ai_implemented TEXT,
  ai_label INTEGER,
  labels TEXT,
  rca_state TEXT,
  ria_state TEXT,
  first_pulled_at TEXT, last_pulled_at TEXT
);
CREATE TABLE IF NOT EXISTS issue_links (
  key TEXT, link_type TEXT, direction TEXT, other_key TEXT,
  PRIMARY KEY (key, link_type, direction, other_key)
);
CREATE TABLE IF NOT EXISTS causal_links (
  cfb_key TEXT, causing_key TEXT, source TEXT, extracted_by TEXT, extracted_at TEXT,
  PRIMARY KEY (cfb_key, causing_key)
);
CREATE TABLE IF NOT EXISTS rca_class (
  key TEXT, round TEXT, rater TEXT,
  escape_cause TEXT, introduced_by TEXT, regression TEXT,
  legacy_mentioned TEXT, ai_mentioned TEXT, prevention_action_type TEXT,
  PRIMARY KEY (key, round, rater)
);
CREATE TABLE IF NOT EXISTS jql_counts (
  run_at TEXT, purpose TEXT, label TEXT, jql TEXT, count INTEGER,
  PRIMARY KEY (purpose, label)
);
CREATE TABLE IF NOT EXISTS query_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  run_at TEXT, purpose TEXT, source TEXT, jql TEXT, dump_file TEXT, issues_loaded INTEGER
);
