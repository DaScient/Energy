setup:
	python -m pip install -U pip
	pip install -e ".[dev,vis]"

lint:
	ruff check .

fmt:
	black .

type:
	mypy ewis

test:
	pytest -q

