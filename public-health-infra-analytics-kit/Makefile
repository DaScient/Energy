setup:
	python -m pip install -U pip
	pip install -e ".[dev,vis]"

lint:
	ruff check .

fmt:
	black .

type:
	mypy phiak

test:
	pytest -q

run:
	phiak diagnose --config examples/configs/minimal.yml --out reports/latest_report.json
