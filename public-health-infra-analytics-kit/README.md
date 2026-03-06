# Public Health Infrastructure Analytics Kit (PHIAK)

[![CI](https://github.com/DaScient/public-health-infra-analytics-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/DaScient/public-health-infra-analytics-kit/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

PHIAK is a plug-in oriented toolkit for privacy-aware, aggregated public health operations analytics.

It helps local and regional teams standardize and analyze:
- capacity signals (ED beds, ICU occupancy, ventilators, staffing, supply)
- incidence signals (cases, tests, positivity, ED ILI, RSV, COVID, norovirus)
- early warning signals (syndromic surveillance, wastewater measurements, outbreak indicators)

PHIAK ships with:
- strict aggregate payload schemas (Pydantic) with privacy checks
- a deterministic engine and plug-in system
- reference metrics and early warning indices
- a CLI for batch runs and report generation
- a static dashboard (HTML + JS + CSS) that reads report JSON and can run air gapped
- example datasets and configs
- documentation focused on privacy, limitations, and safe use

Contact: {subject}@dascient.com

## Guardrails (non-negotiable)

PHIAK is designed to avoid harm:
- No individual-level data, identifiers, free text clinical notes, or address-level geolocation
- Aggregation required by design (counts, rates, rolling summaries)
- Optional minimum cell count suppression for small numbers
- Documentation required for each metric, data source, and reporting limitation

See: `docs/privacy.md` and `spec.md`.

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e ".[dev,vis]"
```

## Quick start

1) Generate a report:
```bash
phiak diagnose --config examples/configs/minimal.yml --out reports/latest_report.json
```

2) Serve the dashboard:
```bash
python -m http.server 8080
# open http://localhost:8080/webapp/
```

The dashboard reads `reports/latest_report.json` and renders:
- inputs summary and suppression policy
- early warning index and alert flag
- robust trend bars (incidence, syndromic, wastewater, capacity)
- plugin outputs table

## Data model overview

PHIAK defines three aggregate payload families:
- IncidencePayload (daily or weekly)
- CapacityPayload (daily or weekly)
- WastewaterPayload (daily or weekly)

These are loaded from CSV in the reference pipeline. Plug-ins can adapt other sources.

## Privacy posture

PHIAK includes:
- schema-level absence of person fields
- best effort forbidden-field scanning to prevent accidental ingestion
- small cell suppression as a configurable policy step

This is not legal advice. Treat your local policies as the source of truth.

## Repository map

- `phiak/`: installable Python library
- `phiak/core/`: engine, schemas, privacy checks, plug-in manager
- `phiak/metrics/`: reference metrics and early warning index math
- `phiak/plugins/builtin/`: built-in plug-ins (suppression, early warning)
- `examples/`: configs and sample CSVs
- `webapp/`: static dashboard
- `docs/`: mkdocs scaffold and privacy documentation

## License

MIT. See `LICENSE`.
