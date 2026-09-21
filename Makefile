.PHONY: install test lint run eval docker-up docker-down

install:
	python -m pip install -e '.[dev]'

test:
	pytest -q

lint:
	ruff check .

run:
	uvicorn llmops_control_plane.main:app --reload

eval:
	python scripts/evaluate.py

docker-up:
	docker compose up --build

docker-down:
	docker compose down
