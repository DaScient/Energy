# Playbooks

## Heat and peak protocol

Triggers:

- forecast cooling stress above threshold
- peak coincidence factor above threshold
- grid operator notice or price spike above threshold

Actions:

- shift batch and training away from peak windows
- raise admission control thresholds for low priority traffic
- validate cooling readiness and alarms
- validate generator fuel and UPS health checks

Rollback:

- revert policy if latency or error crosses guardrails

## Storm protocol

Triggers:

- severe weather alerts in corridor
- forecast wind, flood, snow above thresholds

Actions:

- freeze non-essential maintenance
- stage spares and staffing
- confirm site access plans and vendor readiness
