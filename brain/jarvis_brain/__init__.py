"""Jarvis brain: the conversation agent and STT service behind Home Assistant.

Runs on the i5 LXC, CPU only, fully offline. Nothing in this package may call out to a
network service other than Home Assistant and the local Wyoming containers.

The governing rule, from ARCHITECTURE_REVIEW.md: embeddings retrieve, deterministic code
decides. No module here may dispatch an action on a similarity score.
"""

__version__ = "0.1.0"
