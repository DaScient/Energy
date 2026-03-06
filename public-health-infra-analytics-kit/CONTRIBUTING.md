# Contributing

PHIAK welcomes contributions from public health agencies, researchers, and vendors.

## Development setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e ".[dev,vis]"
pre-commit install
pytest
```

## Contribution types
- new schemas and documentation for common aggregate feeds
- new early warning metrics with clear limitations
- plugins for local export formats
- dashboard improvements that preserve air-gapped operation

## Guardrails
- do not add individual-level data support
- do not add features that enable re-identification
- document limitations and uncertainty

## Security
Do not include secrets or credentials. See SECURITY.md.
