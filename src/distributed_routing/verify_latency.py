"""
Verify that closed-loop signal delays τ = L / v remain within training tolerances.

Each routing path is defined by its physical length (mm) and the estimated
conduction velocity (m/s) of the living neural tissue.  The script asserts that
the computed delay falls inside an acceptable window; if any path exceeds the
tolerance the script exits with a non-zero status so the CI step fails loudly.

Reference: programmable_delay_lines.rs — DelayLineManager.calculate_delay_ms
"""

import sys
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# ---------------------------------------------------------------------------
# Tolerance bounds derived from the experimental training protocol
# ---------------------------------------------------------------------------
MIN_DELAY_MS = 0.5   # Below this the signal arrives before the network is ready
MAX_DELAY_MS = 20.0  # Above this the inter-organoid coupling window is missed


def calculate_delay_ms(path_length_mm: float, conduction_velocity_m_s: float) -> float:
    """Return the expected propagation delay τ = L / v in milliseconds."""
    if conduction_velocity_m_s <= 0:
        raise ValueError("Conduction velocity must be positive.")
    length_m = path_length_mm / 1000.0
    delay_s = length_m / conduction_velocity_m_s
    return delay_s * 1000.0


def verify_path(name: str, path_length_mm: float, conduction_velocity_m_s: float) -> bool:
    """
    Compute the delay for one routing path and check it against the tolerance
    window.  Returns True if the path passes, False otherwise.
    """
    delay_ms = calculate_delay_ms(path_length_mm, conduction_velocity_m_s)
    if MIN_DELAY_MS <= delay_ms <= MAX_DELAY_MS:
        logging.info(
            f"PASS  {name}: τ = {delay_ms:.3f} ms "
            f"(L={path_length_mm} mm, v={conduction_velocity_m_s} m/s)"
        )
        return True
    else:
        logging.error(
            f"FAIL  {name}: τ = {delay_ms:.3f} ms is outside "
            f"[{MIN_DELAY_MS}, {MAX_DELAY_MS}] ms  "
            f"(L={path_length_mm} mm, v={conduction_velocity_m_s} m/s)"
        )
        return False


# ---------------------------------------------------------------------------
# Routing paths under test
# Each tuple: (label, path_length_mm, conduction_velocity_m_s)
# Velocities are representative of cultured cortical networks (~0.1–1 m/s).
# ---------------------------------------------------------------------------
ROUTING_PATHS = [
    ("Module-A → Module-B",  5.0,  0.5),
    ("Module-B → Module-C", 10.0,  0.8),
    ("Module-C → Module-A",  8.0,  0.6),
    ("Module-A → Module-D", 15.0,  1.0),
    ("Module-D → Module-B",  3.0,  0.4),
]


def main() -> int:
    """Run all path checks and return 0 on success, 1 if any path fails."""
    logging.info("=== Closed-Loop Latency Verification ===")
    logging.info(f"Tolerance window: [{MIN_DELAY_MS}, {MAX_DELAY_MS}] ms")

    results = [
        verify_path(name, length, velocity)
        for name, length, velocity in ROUTING_PATHS
    ]

    passed = sum(results)
    total = len(results)
    logging.info(f"=== Results: {passed}/{total} paths within tolerance ===")

    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
