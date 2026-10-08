CREATE TABLE source_registry (source_id TEXT PRIMARY KEY, source_type TEXT NOT NULL, usage_note TEXT NOT NULL);
CREATE TABLE raw_item (raw_id TEXT PRIMARY KEY, source_id TEXT NOT NULL REFERENCES source_registry(source_id), captured_at TIMESTAMP NOT NULL, payload_ref TEXT NOT NULL);
CREATE TABLE observation (observation_id TEXT PRIMARY KEY, raw_id TEXT NOT NULL REFERENCES raw_item(raw_id), parser_version TEXT NOT NULL);
CREATE TABLE evidence (evidence_id TEXT PRIMARY KEY, observation_id TEXT NOT NULL REFERENCES observation(observation_id), locator TEXT NOT NULL);
CREATE TABLE canonical_entity (entity_id TEXT PRIMARY KEY, entity_type TEXT NOT NULL, status TEXT NOT NULL);
CREATE TABLE identity_decision (decision_id TEXT PRIMARY KEY, entity_id TEXT NOT NULL REFERENCES canonical_entity(entity_id), decision_type TEXT NOT NULL, evidence_id TEXT REFERENCES evidence(evidence_id));
