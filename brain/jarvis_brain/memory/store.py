"""SQLite access. The only module that writes to the database file."""

from __future__ import annotations

from ..turn import Candidate, Decision, TurnInput


class MemoryStore:
    def open(self, path: str) -> None:
        """Open the database, load sqlite-vec, apply ``schema.sql``."""
        raise NotImplementedError("build order step 3")

    def log_turn(self, turn: TurnInput, decision: Decision, verified: bool | None) -> int:
        """Append one turn. Returns its id. Never updates an existing row except to mark a
        correction — the log is append-only so a replay sees what the brain saw."""
        raise NotImplementedError("build order step 3")

    def remember(self, candidate: Candidate, phrase: str) -> None:
        """Insert or bump a command, subject to the dedup rule in ``dedup``."""
        raise NotImplementedError("build order step 3")
