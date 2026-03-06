# PHIAK Technical Specification

Version: 1.0.0  
Status: Draft (publish-ready)  
Last updated: 2026-03-05

## 1. Scope

PHIAK defines interoperable, privacy-aware analytics interfaces for:
- aggregate incidence and burden signals
- healthcare system capacity signals
- early warning signals from syndromic surveillance and wastewater epidemiology
- reproducible report artifacts and dashboards for local teams

PHIAK is not an EHR system, not a patient record store, and not a de-identification service.
PHIAK assumes data are already aggregated at a safe reporting level.

## 2. Architecture

PHIAK uses a hub-and-spoke design.

- Hub: `PHIAKEngine`
  - validates payload schemas
  - enforces privacy guardrails
  - executes plug-ins in deterministic order
  - aggregates results into a single report

- Spokes: Plug-ins
  - adapters to local systems (lab feeds, syndromic exports, wastewater labs)
  - enrichers and indices
  - export connectors

PHIAK does not treat plug-in execution as a security boundary.

## 3. Payload families

PHIAK defines three primary payload families:
1) IncidencePayload: aggregate cases, tests, positivity, syndrome counts
2) CapacityPayload: beds, staffing, supplies, constraints
3) WastewaterPayload: gene copies, flow normalization, lab QC flags

All payloads are:
- date keyed (day or week)
- geo keyed at a jurisdiction safe level (county, health district, service area)
- category keyed (pathogen, syndrome, facility type)

## 4. Privacy guardrails

Required by design:
- No person-level fields
- No free text fields
- No precise lat/long
- No addresses
- No record identifiers

Optional enforcement:
- minimum cell count suppression (k-anonymity by count threshold)
- rounding or noise addition policies (documented)

See: `docs/privacy.md`.

## 5. Reference metrics and signals

PHIAK includes small, auditable reference metrics:
- rolling incidence per 100k
- positivity rate and confidence flags
- ED ILI proportion and trend
- bed occupancy and staffing strain
- wastewater trend index
- composite Early Warning Index (EWI)

EWI is a weighted blend of standardized trends, with guardrails against overconfidence.

## 6. Report artifacts

PHIAK outputs:
- JSON report (machines and dashboard)
- optional CSV tables

The dashboard is static and reads the JSON report.

## 7. Compatibility

- Python 3.10+
- Linux, macOS, Windows
- GitHub Actions CI
- optional Docker
