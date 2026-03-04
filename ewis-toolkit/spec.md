# EWIS Technical Specification

Version: 1.0.0  
Status: Draft (publish-ready)  
Last updated: 2026-03-03

## 1. Scope

EWIS defines a reference architecture and interoperable software interfaces for:
- energy systems telemetry and market signals
- data center operational signals (IT load, power, cooling, PUE)
- weather derived signals that influence load, reliability, and cooling demand
- AI workload efficiency metrics (energy per token, throughput per watt)

EWIS is not tied to a single vendor or market. It provides a stable core, plus a plugin surface that allows industry players to integrate their systems rapidly.

## 2. Architectural Overview

EWIS uses a hub-and-spoke model:

- Hub: `EWISEngine`
  - orchestrates state
  - validates payload schemas
  - calls plugins in a deterministic order
  - aggregates results into a single report object

- Spokes: Plugins
  - adapters for weather, grid operator feeds, facility telemetry, cooling control, carbon intensity signals, and workload profiling
  - side-effect free by default
  - may be granted controlled side-effects via explicit configuration (e.g., write to file, emit to Kafka)

### 2.1 Data flow

1. ingest: build a `TelemetryPayload`
2. normalize: validate and standardize fields
3. enrich: run plugins that add derived signals
4. score: compute metrics (GSI, energy per token, carbon intensity, risk)
5. export: generate report artifacts (JSON, CSV, HTML)

## 3. Payload Schema

EWIS operates on a minimal required schema, plus optional fields.

### 3.1 Required fields

- `datacenter_id` (string)
- `region` (string)  
- `timestamp_utc` (ISO-8601 string)
- `power_mw` (float)
- `it_load_mw` (float)
- `pue` (float)

### 3.2 Optional fields

- `base_grid_load_mw` (float)
- `grid_capacity_mw` (float)
- `price_usd_per_mwh` (float)
- `carbon_intensity_kgco2_per_mwh` (float)
- `ambient_temp_c` (float)
- `humidity_pct` (float)
- `wind_m_s` (float)
- `precip_mm` (float)
- `workload` (object)
  - `model_name` (string)
  - `tokens_per_s` (float)
  - `energy_kwh` (float)
  - `tokens` (float)

## 4. Core Metrics

EWIS provides reference metrics. Organizations can override or extend via plugins.

### 4.1 Grid Stress Index (GSI)

The GSI is designed to estimate incremental stress induced by a data center relative to regional headroom and mitigation actions.

GSI = (P_dc * alpha) / max(epsilon, (C_grid - L_base)) + beta * W_severity

Where:
- P_dc: data center power demand (MW)
- alpha: mitigation factor (0..1), derived from demand response posture and workload flexibility
- C_grid: regional grid capacity (MW)
- L_base: regional base load not including the data center (MW)
- beta: weather impact coefficient
- W_severity: normalized weather severity (0..1)
- epsilon: small constant to avoid division by zero

Interpretation guidance:
- 0.0 - 0.5: low stress contribution
- 0.5 - 1.0: moderate stress contribution
- >1.0: high stress contribution, investigate mitigation

### 4.2 Energy per Token (EPT)

Energy per Token = energy_kwh / max(epsilon, tokens)

Derived from workload payload fields. If energy is unavailable, EWIS can estimate using facility power and workload share, but this requires explicit configuration.

### 4.3 Carbon per Token (CPT)

Carbon per Token = (carbon_intensity_kgco2_per_mwh * energy_kwh / 1000) / max(epsilon, tokens)

## 5. Plugin Contract

Plugins implement a strict interface:

- `name: str`
- `initialize(context: PluginContext) -> None`
- `execute(payload: dict, context: PluginContext) -> PluginResult`
- `teardown(context: PluginContext) -> None`

### 5.1 Determinism

By default, EWIS expects plugins to be deterministic given:
- payload
- plugin configuration
- time window assumptions

Plugins that call external APIs must:
- support timeouts
- support caching
- expose request metadata in their results

### 5.2 Side effects

Plugins should avoid side effects unless `allow_side_effects: true` is configured. When enabled, plugins may:
- write exports
- send events to a queue
- call control endpoints

EWIS does not treat plugin execution as a security sandbox.

## 6. Visualization and Reporting

EWIS report artifacts:
- JSON report
- CSV tables (metrics, events)
- optional HTML report with embedded Plotly figures

Visualization guidelines:
- Plotly is preferred for interactive artifacts.
- Matplotlib is used for static exports and environments where Plotly is restricted.

## 7. Compatibility

- Python: 3.10+
- OS: Linux, macOS, Windows
- Container: optional Dockerfile
- CI: GitHub Actions

## 8. Non-goals

- EWIS does not provide an out-of-the-box control-plane for physical infrastructure.
- EWIS is not a SCADA replacement.
- EWIS is not a full market bidding optimizer by default (plugins may implement this).

