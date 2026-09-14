.PHONY: help install test lint clips commands firmware brain

help:
	@echo "install   - install the brain in a venv with dev extras"
	@echo "test      - run the brain's tests"
	@echo "lint      - ruff check the brain"
	@echo "clips     - render the phrase bank to FLAC with Piper"
	@echo "commands  - generate the MultiNet command table from exposed entities"
	@echo "firmware  - compile and upload the Stage A satellite firmware"
	@echo "brain     - run the brain locally on :8099"

install:
	cd brain && python3 -m venv .venv && .venv/bin/pip install -e '.[dev]'

test:
	cd brain && .venv/bin/pytest -q

lint:
	cd brain && .venv/bin/ruff check jarvis_brain tests

clips:
	python3 satellite/clips/render_clips.py --phrases satellite/clips/phrases.yaml --out satellite/clips

commands:
	python3 satellite/commands/generate_table.py --out satellite/commands/generated

firmware:
	esphome run satellite/jarvis-satellite.yaml

brain:
	cd brain && .venv/bin/uvicorn jarvis_brain.main:app --host 0.0.0.0 --port 8099
