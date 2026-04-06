# EWIS Toolkit — Notebooks

This directory contains Jupyter notebooks that demonstrate the **EWIS Toolkit**
(Energy, Weather, and Interoperability Suite). They range from quick exploratory
demos to detailed training manuals.

> **Prerequisites** — install the toolkit in editable mode before running any
> notebook:
>
> ```bash
> cd ewis-toolkit
> pip install -e ".[dev,vis]"
> ```

## Notebook Index

| # | Notebook | Description | Level |
|---|---------|-------------|-------|
| 01 | [Grid Stress EDA](01_grid_stress_eda.ipynb) | Load a sample payload and compute the Grid Stress Index (GSI) | Starter |
| 02 | [GenAI Metrics](02_genai_metrics.ipynb) | Compute energy-per-token and carbon-per-token for AI workloads | Starter |
| 03 | [Cooling Optimizer Demo](03_cooling_optimizer_demo.ipynb) | Run the CoolingOptimizerPlugin across environmental scenarios and visualize recommendations | Demo |
| 04 | [Engine Pipeline Walkthrough](04_engine_pipeline_walkthrough.ipynb) | End-to-end training manual: payload → engine → plugins → report | Training |
| 05 | [Payload Validation Guide](05_payload_validation_guide.ipynb) | Deep dive into TelemetryPayload schema, field constraints, and error handling | Training |
| 06 | [Plugin Development Tutorial](06_plugin_development_tutorial.ipynb) | Step-by-step guide to building, registering, and testing a custom EWIS plugin | Training |
| 07 | [Multi-Datacenter Comparison](07_multi_datacenter_comparison.ipynb) | Compare GSI, efficiency, and carbon metrics across a fleet of data centers | Demo |

## Data

Notebooks load sample data from `../examples/data/sample_payload.json`. The
schema is defined in `ewis.core.payloads.TelemetryPayload`.

## Tips

* Run notebooks from the `notebooks/` directory so relative paths resolve
  correctly.
* All notebooks are designed to work **offline** — no network calls are required.
* Visualizations use the Python standard library and pandas where available;
  Plotly or Matplotlib are used only when the `vis` extras are installed.
