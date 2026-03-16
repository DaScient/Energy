# ARES-E: Agentic Resilience & Evaluation System for Essential-Infrastructure

### The DaScient Integrated Infrastructure Suite (EWIS, WOIK, PHIAK)

ARES-E is a unified evaluation harness and toolkit designed to standardize telemetry, events, and operational metrics across the "Critical Quad" of national security: **Data/Energy, Water, and Public Health.** This suite provides the deterministic engines, plug-in architectures, and privacy-aware schemas necessary to evaluate AI agents and human-machine teams under real-world operational stress.


## EWIS: Energy, Weather, and Interoperability Suite

**Focus:** Data Center Planning, Grid Operations, and AI Workload Efficiency.

EWIS is a plug-and-play Python toolkit for operators and researchers managing the intersection of high-performance compute (HPC) and energy markets.

### Key Capabilities:

* **Grid & Market Intelligence:** Standardizes payloads for grid stress signals, carbon intensity, and real-time energy pricing.
* **Data Center Optimization:** Tools for capacity planning, PUE (Power Usage Effectiveness) assisted attribution, and cooling optimization.
* **AI Efficiency Metrics:** Benchmarking "Energy per Token" and model workload efficiency to assess the environmental and operational cost of AI deployment.
* **Weather Integration:** Open-source RSS and weather-driven intelligence to forecast impacts on load, pricing, and infrastructure reliability.

### Features:

* **Extensible Plugin Framework:** Support for Python entry points and local plugin discovery for "hot-swappable" industry adapters.
* **CLI Diagnostics:** Command-line interface for rapid batch runs and system diagnostics.
* **Visualization Helpers:** Plotly-first (interactive) and Matplotlib (fallback) support for analytics.


## WOIK: Water Ops Interoperability Kit

**Focus:** Water Treatment, Distribution, and Hydraulic Operational Metrics.

WOIK standardizes telemetry and events across municipal and industrial water infrastructure, providing a "digital twin" logic for agentic evaluation.

### Key Capabilities:

* **Infrastructure Telemetry:** Standardized schemas for treatment plants, distribution networks, lift stations, and storage tanks.
* **Operational Risk Assessment:** Reference metrics for leak likelihood, water quality risk, and pump specific energy.
* **Energy-Water Nexus:** Integrated accounting for carbon and energy consumption associated with water pumping and treatment.
* **Event Standardization:** Normalizes disparate sensor data into a strict Pydantic payload schema.

### Features:

* **Deterministic Engine:** A local execution environment that runs plug-ins without external dependencies.
* **Interactive Local Dashboard:** An air-gapped HTML/JS dashboard that visualizes report JSON for sensitive site operations.
* **Pydantic Schema Enforcement:** Ensures data integrity across heterogeneous sensor networks.


## PHIAK: Public Health Infrastructure Analytics Kit

**Focus:** Privacy-Aware Health Operations and Early Warning Systems.

PHIAK is a plug-in oriented toolkit for aggregated public health operations analytics, designed specifically to avoid the ingestion of PII/PHI.

### Key Capabilities:

* **Capacity Signaling:** Tracks ED beds, ICU occupancy, ventilator availability, and staffing/supply levels.
* **Incidence & Surveillance:** Standardizes signals for cases, test positivity, and syndromic surveillance (wastewater, outbreak indicators).
* **Privacy Guardrails (Non-Negotiable):**
* **Zero Individual Data:** No identifiers, free-text notes, or address-level geolocation.
* **Aggregation by Design:** All metrics are counts, rates, or rolling summaries.
* **Cell Suppression:** Optional minimum cell count suppression to prevent re-identification in small populations.



### Features:

* **Static Dashboard:** Air-gapped HTML + JS + CSS dashboard—perfect for secure, JWICS-level environments.
* **Deterministic Engine:** Provides reproducible early warning indices and report generation.
* **Documentation-First:** Requires specific documentation for every metric and data source to ensure transparency and safety.

## Shared Architecture & Use Cases

### The Plugin Contract

All three kits share a "Plugin Contract," allowing different teams to integrate proprietary systems (SCADA, EHR, Data Center Management) without rewriting the core analytics engine.

### Deployment & Interoperability

* **Notebook-ready:** Designed for Data Scientists and Researchers to iterate in Jupyter/VS Code.
* **Air-Gapped Ready:** All dashboards and reports are generated as static files, requiring zero internet connectivity for visualization.
* **Vendor Agnostic:** Standardizes payload schemas so that any AI model or agent can be evaluated against these metrics via the ARES-E harness.

---

## Contact & Teaming

For inquiries regarding DIU CSO teaming or implementation, contact: `ARES-E@dascient.com`

---

# DaScient Energy, Weather, and Interoperability Suite

A notebook-ready toolkit for:

- Deep and Generative AI analytics and open-source metrics design
- Data center interoperability performance metrics and mitigation protocols under energy and grid stress
- Open-source RSS and weather driven energy intelligence for data center planning

## Included notebooks

- `notebooks/DaScient_DeepGenAI_Analytics_OpenSource_Metrics_Package.ipynb`
- `notebooks/DaScient_DataCenter_Interop_EnergyCrisis_Notebook.ipynb`
- `notebooks/DaScient_Weather_News_Energy_DataCenter_Planning.ipynb`

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install -r requirements.txt
jupyter lab
```

## Repo layout

- `notebooks/` - the main packages
- `src/dascient_suite/` - reusable modules (RSS, weather, energy proxies, reporting I/O)
- `docs/` - playbooks and glossary
- `reports/` - generated exports (optional)
- `data/sample/` - sample schemas

## License

MIT - see `LICENSE`.

## Disclaimer

Planning-grade analytics and operational scaffolding. Not a substitute for facility engineering, safety review, or regulatory compliance.
