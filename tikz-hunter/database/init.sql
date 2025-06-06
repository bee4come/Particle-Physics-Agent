-- tikz-hunter/database/init.sql

CREATE TABLE IF NOT EXISTS tikz_snippets (
  uid         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  hash        CHAR(64) UNIQUE NOT NULL,
  snippet     JSONB NOT NULL,
  status      TEXT DEFAULT 'validated' CHECK (status IN ('validated', 'needs_review', 'rejected')),
  source_url  TEXT,
  created_at  TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at  TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create an index on the hash for quick lookups to prevent duplicates
CREATE UNIQUE INDEX IF NOT EXISTS idx_tikz_snippets_hash ON tikz_snippets(hash);

-- Create a GIN index on the JSONB column for better search performance on snippet fields
CREATE INDEX IF NOT EXISTS idx_tikz_snippets_snippet_gin ON tikz_snippets USING GIN(snippet);

-- A trigger to automatically update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_tikz_snippets_modtime
BEFORE UPDATE ON tikz_snippets
FOR EACH ROW
EXECUTE FUNCTION update_modified_column();

-- Optional: Create a table for harvest jobs logging
CREATE TABLE IF NOT EXISTS harvest_log (
    id SERIAL PRIMARY KEY,
    harvester TEXT NOT NULL,
    query TEXT,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    finished_at TIMESTAMP WITH TIME ZONE,
    status TEXT DEFAULT 'running' CHECK (status IN ('running', 'completed', 'failed')),
    snippets_found INT DEFAULT 0,
    error_message TEXT
);