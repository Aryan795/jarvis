#!/usr/bin/env python3
"""Generate the MultiNet command table, refusing anything that is not tier A.

Reads commands.yaml, checks every entity against Home Assistant's exposed-entity list with
its tier label, and runs esp-sr's multinet_g2p.py to produce the phoneme table the firmware
compiles in.

This script is a safety boundary, not a convenience. It exits non-zero rather than emitting
a table containing a lock, a toggle, or a command with no acknowledgement clip. The board
has no guard chain; this is where that job is done.
"""

from __future__ import annotations

import argparse
import sys


class TableError(Exception):
    """A rule was broken. Always fatal — never downgraded to a warning."""


def validate(commands: list[dict], exposed: dict[str, str]) -> None:
    """Check every rule from commands.yaml.

    Raises on: an entity that is not exposed, an entity above tier A, a toggle action, a
    command with no ack clip, or a phrase whose polarity is not part of its id.
    """
    raise NotImplementedError("build order step 4")


def generate(commands: list[dict], out_dir: str) -> None:
    """Run esp-sr's multinet_g2p.py over the validated phrases."""
    raise NotImplementedError("build order step 4")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commands", default="satellite/commands/commands.yaml")
    parser.add_argument("--out", default="satellite/commands/generated")
    parser.add_argument("--ha-url", default="http://homeassistant.local:8123")
    args = parser.parse_args(argv)
    raise NotImplementedError("build order step 4")


if __name__ == "__main__":
    sys.exit(main())
