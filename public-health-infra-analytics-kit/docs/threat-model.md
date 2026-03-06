# Threat Model (High level)

PHIAK assumes realistic risks:
- accidental inclusion of sensitive fields
- small cell re-identification risk
- overinterpretation of noisy signals
- dashboard screenshots shared outside intended context

Mitigations:
- schema rejects person-level fields
- suppression plugin for small cells
- explicit uncertainty flags and limitations
- documentation that discourages use for individual decision making
