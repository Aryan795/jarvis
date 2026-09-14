#!/usr/bin/env python3
"""Render the clip bank to FLAC with the same Piper voice the server uses.

Run at build time, before `esphome run`. Output goes next to this file and is gitignored —
the phrases are the source, the audio is a build artefact.

Fails if a clip comes out longer than the ceiling, rather than shipping a long deaf spell:
the wake word detector is gated during playback on this hardware.
"""

from __future__ import annotations

import argparse
import sys

MAX_CLIP_SECONDS = 1.5


def render(text: str, voice: str, out_path: str) -> float:
    """Render one phrase and return its duration in seconds."""
    raise NotImplementedError("build order step 3")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phrases", default="satellite/clips/phrases.yaml")
    parser.add_argument("--out", default="satellite/clips")
    parser.add_argument("--max-seconds", type=float, default=MAX_CLIP_SECONDS)
    args = parser.parse_args(argv)
    raise NotImplementedError("build order step 3")


if __name__ == "__main__":
    sys.exit(main())
