# EWIS Toolkit
Energy, Weather, and Interoperability Suite for Energy Systems and Data Centers

[![CI](https://github.com/DaScient/ewis-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/DaScient/ewis-toolkit/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

EWIS is a **plug-n-play Python toolkit** for operators and researchers working across:
- grid operations and energy markets
- data center capacity planning and cooling optimization
- weather and climate signals that impact load, pricing, and reliability
- model and workload efficiency for AI and high performance compute

It ships with:
- an extensible plugin framework (Python entry points + local plugin discovery)
- a CLI for diagnostics and batch runs
- reference metrics (grid stress, carbon intensity, energy per token, PUE assisted attribution)
- visualization helpers (Plotly first, Matplotlib fallback)
- notebooks and reproducible examples

## Why this repository exists

The energy and data center industries often share problems but not interfaces. EWIS standardizes:
- **a payload schema** for telemetry, forecasts, and market signals
- **a plugin contract** for hot-swappable “industry adapters”
- **a reproducible workflow** from ingestion to analysis to export

This lets different teams integrate proprietary systems without rewriting the core engine.

## Install

### Option A: pip (recommended)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e ".[dev,vis]"
```

### Option B: Docker
```bash
docker build -t ewis-toolkit .
docker run --rm -it ewis-toolkit ewis --help
```

## Quick start

### 1) Run a baseline diagnostic
```bash
ewis diagnose --config examples/configs/minimal.yml
```

### 2) Use the Python API
```python
from ewis.core.engine import EWISEngine
from ewis.core.payloads import TelemetryPayload
from ewis.plugins.builtin.weather_rss import WeatherRssPlugin

engine = EWISEngine()

engine.register(WeatherRssPlugin(
    name="weather_rss",
    rss_urls=[
        "https://www.noaa.gov/rss.xml",
    ],
))

payload = TelemetryPayload(
    datacenter_id="DC-US-WEST",
    region="CAISO",
    timestamp_utc="2026-03-03T12:00:00Z",
    power_mw=32.5,
    it_load_mw=26.2,
    pue=1.24,
)

report = engine.run(payload.to_dict())
print(report.summary())
```

## Plugin system

EWIS supports:
- **Built-in plugins** under `ewis.plugins.builtin`
- **Local drop-in plugins** (python modules in `plugins/` at repo root)
- **Third-party plugins** distributed as separate pip packages via entry points:
  - `ewis.plugins` group

To create a plugin, implement `BasePlugin` and either:
- place it under `plugins/` for local discovery, or
- publish a separate package that registers an entry point.

See: `docs/plugins.md`.

## Repository map
- `ewis/`: library package
- `plugins/`: local drop-in plugin examples (not installed by default)
- `notebooks/`: EDA and demo notebooks
- `examples/`: configs and sample data
- `docs/`: mkdocs documentation site
- `.github/workflows/`: CI

## Governance and safety

- Please read `SECURITY.md` to report vulnerabilities.
- Please read `CONTRIBUTING.md` before opening PRs.
- The plugin sandbox is **not a security boundary**. Treat plugins as trusted code.

## Citation
If you use EWIS in research or a report, cite the repository and the release tag you used.

## License
MIT. See `LICENSE`.

