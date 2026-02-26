PY=python

.PHONY: venv install lab test

venv:
	$(PY) -m venv .venv

install:
	. .venv/bin/activate && pip install -U pip && pip install -r requirements.txt && pip install -e .

lab:
	. .venv/bin/activate && jupyter lab

test:
	. .venv/bin/activate && $(PY) -m pytest -q
