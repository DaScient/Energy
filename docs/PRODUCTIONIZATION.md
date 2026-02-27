# Productionization Notes

## Minimal scheduled jobs

- 30-60 min: weather forecasts and alerts
- daily: city ranking and clipping board
- weekly: threshold tuning from recent baselines

## Storage

- JSONL for RSS and alert evidence streams
- parquet for hourly weather and derived metrics
- keep raw payloads for auditability

## Governance

Every automated action should be reversible and logged with inputs, thresholds, and decision outputs.
