# Contributing

Thanks for contributing to EWIS.

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
- bug fixes
- new plugins (built-in or third-party)
- docs improvements
- new metrics, provided the math is clearly documented

## Pull request checklist
- tests added or updated
- docs updated (as needed)
- changelog entry added under Unreleased
- lint and format passes locally

## Style
- Black formatting
- Ruff linting
- Type hints required for public APIs
- Avoid network calls in unit tests; use mocking

## Security
Do not include secrets, keys, or credentials in code, examples, or notebooks.
See SECURITY.md for reporting.

