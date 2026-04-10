"""
Verify Closed-Loop Latency
===========================
Ensures that signal delay τ = L / v remains within training tolerances
for all inter-module routing paths in the distributed organoid network.

The delay model mirrors the Rust implementation in programmable_delay_lines.rs:
    τ (ms) = (L / 1000) / v × 1000

where
    L = path length in mm
    v = conduction velocity in m/s
"""

import sys


def calculate_delay_ms(path_length_mm: float, conduction_velocity_m_s: float) -> float:
    """Return the expected propagation delay in milliseconds.

    Parameters
    ----------
    path_length_mm : float
        Physical (or virtual) routing distance in millimetres.
    conduction_velocity_m_s : float
        Estimated signal conduction velocity in metres per second.

    Returns
    -------
    float
        Delay τ in milliseconds.
    """
    length_m = path_length_mm / 1000.0
    delay_s = length_m / conduction_velocity_m_s
    return delay_s * 1000.0  # convert to ms


def verify_latency_budget(
    paths: list[dict],
    max_latency_ms: float = 10.0,
) -> list[dict]:
    """Check every routing path against the latency budget.

    Parameters
    ----------
    paths : list[dict]
        Each entry must contain ``"name"``, ``"length_mm"``, and
        ``"velocity_m_s"`` keys.
    max_latency_ms : float
        Maximum acceptable one-way delay (default 10 ms).

    Returns
    -------
    list[dict]
        Entries that violate the latency budget.
    """
    violations = []
    for path in paths:
        tau = calculate_delay_ms(path["length_mm"], path["velocity_m_s"])
        status = "OK" if tau <= max_latency_ms else "VIOLATION"
        print(f"  {path['name']:30s}  τ = {tau:8.3f} ms  [{status}]")
        if tau > max_latency_ms:
            violations.append({**path, "delay_ms": tau})
    return violations


# ------------------------------------------------------------------
# Representative inter-module routing paths for CI validation
# ------------------------------------------------------------------
REFERENCE_PATHS: list[dict] = [
    {"name": "Cortical→Hippocampal",   "length_mm": 15.0,  "velocity_m_s": 4.0},
    {"name": "Hippocampal→Cerebellar",  "length_mm": 20.0,  "velocity_m_s": 3.5},
    {"name": "Cortical→Cortical",       "length_mm":  5.0,  "velocity_m_s": 5.0},
    {"name": "Thalamic→Cortical",       "length_mm": 12.0,  "velocity_m_s": 4.5},
]

MAX_ALLOWED_LATENCY_MS = 10.0  # training-tolerance ceiling


def main() -> None:
    print("=" * 60)
    print("Closed-Loop Latency Verification  (τ = L / v)")
    print("=" * 60)
    print(f"  Max allowed latency : {MAX_ALLOWED_LATENCY_MS} ms\n")

    violations = verify_latency_budget(REFERENCE_PATHS, MAX_ALLOWED_LATENCY_MS)

    print()
    if violations:
        print(
            f"FAIL: {len(violations)} path(s) exceed the "
            f"{MAX_ALLOWED_LATENCY_MS} ms latency budget."
        )
        sys.exit(1)
    else:
        print("PASS: All routing paths are within latency tolerances.")


if __name__ == "__main__":
    main()
