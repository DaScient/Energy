## Dashboard

The dashboard is a static web app under `webapp/`.

It reads `reports/latest_report.json` and renders:
- KPIs
- metric table and plug-in outputs
- event table
- gauge charts

This supports air-gapped environments. Serve via any static file server.
