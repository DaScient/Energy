# Privacy and Safety

PHIAK is designed for aggregated public health analytics. It is not a patient data system.

## Non-negotiable rules

PHIAK must not ingest:
- individual-level records
- direct identifiers (name, MRN, phone, email)
- quasi-identifiers that enable re-identification in small cells (exact DOB, exact address)
- free text clinical notes
- precise coordinates

PHIAK should ingest only:
- counts, rates, and pre-aggregated summaries
- jurisdiction-level geography (county, health district, service area)
- time buckets (day or week)

## Minimum cell count suppression

Small numbers can re-identify individuals.
PHIAK supports suppression and flagging:
- If count < k, suppress the value and emit a suppression flag.
- k is configurable. Defaults are conservative.

This is a reference approach, not legal advice.

## Auditability

Every metric should be:
- defined in documentation
- traceable to inputs
- accompanied by limitations

## Security and operational guidance

- Do not store reports containing sensitive small cell counts on public hosts.
- Keep data in a controlled environment.
- Prefer air-gapped dashboard hosting where needed.

Contact: {subject}@dascient.com
