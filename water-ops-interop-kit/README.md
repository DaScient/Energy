# Water Ops Interoperability Kit (WOIK)

[![CI](https://github.com/DaScient/water-ops-interop-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/DaScient/water-ops-interop-kit/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

WOIK is a plug-in oriented toolkit for water and wastewater operators, utilities, and researchers.

It standardizes telemetry, events, and operational metrics across:
- treatment plants
- distribution networks
- lift stations and pumping
- storage tanks
- water quality sensing
- energy and carbon accounting for pumping and treatment

WOIK ships with:
- a strict payload schema (Pydantic)
- a deterministic engine that runs plug-ins
- reference metrics (leak likelihood, pump specific energy, water quality risk)
- a CLI for batch runs
- an interactive local dashboard (HTML + JS) that reads report JSON

Contact: {subject}@dascient.com

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e ".[dev,vis]"
```

## Quick start

1) Run a diagnostic using the shipped config:

```bash
woik diagnose --config examples/configs/minimal.yml --out reports/latest_report.json
```

2) Open the dashboard:

```bash
python -m http.server 8080
# then open http://localhost:8080/webapp/
```

The dashboard reads `reports/latest_report.json` and renders:
- summary KPIs
- metric table and plug-in outputs
- event table
- gauge charts

## What WOIK is solving

Water systems are operationally complex and often data-fragmented:
- SCADA and historian exports vary by vendor
- telemetry naming conventions drift
- field sensors are noisy and intermittently missing
- reliability decisions are made without coherent attribution

WOIK provides a stable foundation:
- consistent payloads
- auditable metrics
- interop surfaces for vendors and utilities
- reproducible examples and notebooks

## Repository map

- `woik/`: installable Python library
- `woik/core/`: engine, payload, plug-in manager
- `woik/metrics/`: reference metrics
- `woik/plugins/builtin/`: example plug-ins
- `examples/`: configs and sample data
- `webapp/`: static dashboard (HTML + JS + CSS)
- `notebooks/`: starter notebook
- `docs/`: mkdocs site scaffold

## Plug-in model

WOIK supports:
- built-in plug-ins under `woik.plugins.builtin`
- local drop-in plug-ins under `plugins/`
- third-party plug-ins distributed as pip packages via entry points:
  - `woik.plugins` group in `pyproject.toml`

See `docs/plugins.md`.

## License

MIT. See `LICENSE`.
