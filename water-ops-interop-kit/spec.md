# WOIK Technical Specification

Version: 1.0.0  
Status: Draft (publish-ready)  
Last updated: 2026-03-05

## 1. Scope

WOIK defines interoperable interfaces for water and wastewater operational analytics:
- telemetry normalization
- event and alarm annotation
- water quality and process signals
- pumping and treatment energy accounting
- reliability and risk scoring

WOIK is not a SCADA replacement. It is a portable analytics and interoperability layer.

## 2. Architecture

WOIK uses a hub-and-spoke design:

- Hub: `WOIKEngine`
  - validates payload schema
  - executes plug-ins in deterministic order
  - aggregates results into a single report object

- Spokes: Plug-ins
  - adapters for SCADA exports, historian APIs, AMI, lab data
  - metric enrichers and risk scorers
  - export connectors (CSV, JSON, HTML, message bus)

WOIK does not treat plug-in execution as a security boundary.

## 3. Payload Schema

WOIK operates on a minimal required schema, plus optional extensions.

### 3.1 Required fields

- `asset_id` (string)  
- `asset_type` (string)  
- `system_id` (string)  
- `timestamp_utc` (ISO-8601 string)  

- `flow_m3_s` (float, >= 0)  
- `pressure_kpa` (float, >= 0)  
- `level_m` (float, >= 0)  

### 3.2 Optional fields

Hydraulics and operations:
- `valve_position_pct` (float 0..100)
- `pump_speed_rpm` (float >= 0)
- `pump_power_kw` (float >= 0)
- `zone_id` (string)
- `dma_id` (string)

Water quality:
- `turbidity_ntu` (float >= 0)
- `chlorine_mg_l` (float >= 0)
- `ph` (float 0..14)
- `conductivity_us_cm` (float >= 0)
- `temperature_c` (float)
- `lab_results` (object)

Energy and carbon:
- `electricity_price_usd_kwh` (float >= 0)
- `carbon_intensity_kgco2_kwh` (float >= 0)

Events:
- `events` (list of objects)
  - `type` (string)
  - `severity` (string)
  - `message` (string)
  - `source` (string)

Work orders and maintenance:
- `maintenance` (object)
  - `last_service_utc` (string)
  - `mtbf_days` (float)

## 4. Reference Metrics

WOIK ships reference metrics that are small, auditable, and easy to override.

### 4.1 Leak Likelihood Score (LLS)

LLS estimates the probability that abnormal pressure-flow behavior indicates a leak.

A reference formulation:

LLS = sigmoid( a1 * z(flow) - a2 * z(pressure) + a3 * z(dflow_dt) + a4 * z(dpressure_dt) )

Where `z(.)` is a robust z-score over a rolling window. Plug-ins can implement domain-specific features.

### 4.2 Pump Specific Energy (PSE)

PSE estimates energy per unit volume moved:

PSE = pump_power_kw / max(epsilon, flow_m3_s)

This yields kJ per m3 since kW = kJ per second. When pump power is missing, WOIK returns None with notes.

### 4.3 Water Quality Risk Index (WQRI)

WQRI is a compositional risk score from turbidity, chlorine residual, and pH deviation:

WQRI = w1 * norm(turbidity) + w2 * norm(chlorine_low) + w3 * norm(|pH - 7|)

This is a reference heuristic. Utilities should map to their own regulatory thresholds.

## 5. Plug-in Contract

Plug-ins implement:

- `name: str`
- `initialize(context: PluginContext) -> None`
- `execute(payload: dict, context: PluginContext) -> PluginResult`
- `teardown(context: PluginContext) -> None`

Plug-ins should:
- expose request metadata when calling external APIs
- support timeouts and caching
- avoid side effects unless explicitly enabled by config

## 6. Report Artifacts

WOIK generates:
- JSON report for machines
- optional CSV tables
- optional HTML dashboard compatible JSON schema

## 7. Compatibility

- Python 3.10+
- Linux, macOS, Windows
- optional Docker support
- GitHub Actions CI
