## Dashboard

The dashboard is a static web app under `webapp/`.

It reads `reports/latest_report.json` and renders:
- KPIs and risk indices
- alert flags
- plugin outputs

This supports air-gapped environments. Serve via any static file server.
