-- Jarvis memory. One file, one truth.
--
-- v1 had four stores that drifted apart: FAISS #1 for automations, FAISS #2 for commands,
-- a SQLite DB for structured memory, and RAM for short-term plus an episodic store. This
-- replaces all of it. Vectors live beside their rows through sqlite-vec, so a command and
-- its embedding cannot disagree about what they are.

PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

-- Every turn the brain saw, whatever decided it, including on-device decisions relayed
-- from the satellite. Thresholds and calibration are fitted from this table, so a turn
-- that is missing here is a turn the fit cannot see (review 2.4).
CREATE TABLE IF NOT EXISTS turns (
    id                INTEGER PRIMARY KEY,
    ts                TEXT    NOT NULL,
    audio_hash        TEXT,
    transcript        TEXT,
    transcript_alt    TEXT,    -- the second decoder's opinion, when there was one
    decoder_agreed    INTEGER, -- NULL when only one decoder ran
    satellite_id      TEXT,
    area              TEXT,
    source            TEXT NOT NULL,   -- hassil | retriever | classifier | satellite
    bucket            TEXT,            -- hassil only: exact | fuzzy | unmatched_entity
    intent            TEXT,
    entity_id         TEXT,
    slots_json        TEXT,
    tier              TEXT,
    raw_score         REAL,
    calibrated        REAL,
    runner_up         REAL,
    outcome           TEXT NOT NULL,
    refused_by        TEXT,
    verified          INTEGER,         -- did the state actually change
    corrected         INTEGER DEFAULT 0 -- user said "no, actually..." within the window
);

CREATE INDEX IF NOT EXISTS turns_ts      ON turns (ts);
CREATE INDEX IF NOT EXISTS turns_source  ON turns (source, outcome);
CREATE INDEX IF NOT EXISTS turns_entity  ON turns (entity_id);

-- Remembered commands. What the retriever searches.
--
-- The uniqueness constraint is the dedup rule in schema form: a merge requires an identical
-- (intent, polarity, entity, slot) tuple. v1 merged at cosine above 0.92, which would fold
-- the two polarities of one command into a single memory (review 2.7).
CREATE TABLE IF NOT EXISTS commands (
    id            INTEGER PRIMARY KEY,
    phrase        TEXT NOT NULL,
    intent        TEXT NOT NULL,
    polarity      TEXT NOT NULL,
    entity_id     TEXT,
    slots_json    TEXT NOT NULL DEFAULT '{}',
    tier          TEXT NOT NULL,
    hits          INTEGER NOT NULL DEFAULT 0,
    last_used     TEXT,
    confidence    REAL,
    created       TEXT NOT NULL,
    UNIQUE (intent, polarity, entity_id, slots_json)
);

-- Candidate merges for a human to look at. Similarity may propose; it may not merge.
CREATE TABLE IF NOT EXISTS merge_review (
    id            INTEGER PRIMARY KEY,
    left_id       INTEGER NOT NULL REFERENCES commands (id) ON DELETE CASCADE,
    right_id      INTEGER NOT NULL REFERENCES commands (id) ON DELETE CASCADE,
    similarity    REAL NOT NULL,
    resolved      INTEGER NOT NULL DEFAULT 0
);

-- Calibration fits, versioned so a bad fit can be rolled back and a decision can be
-- replayed against the fit that was live when it was made.
CREATE TABLE IF NOT EXISTS calibration (
    id            INTEGER PRIMARY KEY,
    source        TEXT NOT NULL,
    bucket        TEXT,
    fitted_at     TEXT NOT NULL,
    n_samples     INTEGER NOT NULL,
    model_json    TEXT NOT NULL,
    active        INTEGER NOT NULL DEFAULT 0
);

-- The satellite's on-device predictions during shadow, paired against the brain's decision
-- for the same utterance. A command is promoted out of shadow from this table (review 3.5).
CREATE TABLE IF NOT EXISTS satellite_shadow (
    id                INTEGER PRIMARY KEY,
    ts                TEXT NOT NULL,
    satellite_id      TEXT NOT NULL,
    command_id        TEXT NOT NULL,
    p1                REAL NOT NULL,
    p2                REAL NOT NULL,
    brain_turn_id     INTEGER REFERENCES turns (id) ON DELETE SET NULL,
    agreed            INTEGER,
    polarity_agreed   INTEGER
);
