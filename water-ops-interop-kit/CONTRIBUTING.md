# Contributing

WOIK welcomes contributions from utilities, vendors, researchers, and operators.

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
- new plug-ins (built-in or third-party)
- improvements to payload schema and documentation
- new reference metrics with clear math and tests
- dashboard and export improvements

## Style
- Black formatting
- Ruff linting
- Type hints for public APIs

## Security
Do not include secrets or credentials. See SECURITY.md.
