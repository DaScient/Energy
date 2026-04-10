"""
Audit event-detection pipelines against raw electrophysiology benchmarks.

Spike sorting translates analog voltage traces into discrete event timestamps.
This script validates the quality of that translation by:
  1. Generating a synthetic extracellular trace with known ground-truth spike
     positions injected into Gaussian noise.
  2. Running a threshold-based detector that mirrors the Sum of Squared
     Differences logic implemented in template_matching.rs.
  3. Asserting that every detected event falls within an acceptable temporal
     tolerance of a ground-truth spike, and that no ground-truth spike is
     silently missed (false-negative rate is bounded).

Reference: template_matching.rs — RealTimeSpikeSorter.detect_events
"""

import sys
import logging
import numpy as np

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# ---------------------------------------------------------------------------
# Quality thresholds
# ---------------------------------------------------------------------------
DETECTION_TOLERANCE_FRAMES = 30   # ±30 frames (±1 ms at 30 kHz)
MAX_FALSE_NEGATIVE_RATE    = 0.10  # at most 10 % of ground-truth spikes missed
MAX_FALSE_POSITIVE_RATE    = 0.10  # at most 10 % of detections are spurious

SAMPLING_RATE_HZ = 30_000

# Benchmark timing constants (in frames at SAMPLING_RATE_HZ)
BENCHMARK_DURATION_FRAMES  = 30_000  # 1 second
BENCHMARK_SPIKE_INTERVAL_FRAMES = 3_000  # 100 ms between spikes


# ---------------------------------------------------------------------------
# Synthetic data generation
# ---------------------------------------------------------------------------

def _make_synthetic_trace(
    duration_frames: int,
    spike_positions: list[int],
    noise_std: float = 0.1,
    rng: np.random.Generator | None = None,
) -> np.ndarray:
    """Return a noisy trace with a canonical waveform injected at each position."""
    if rng is None:
        rng = np.random.default_rng(seed=42)

    trace = rng.normal(0.0, noise_std, duration_frames)
    waveform = np.array([0.1, 0.5, 1.2, -0.8, -0.2, 0.05])

    for pos in spike_positions:
        end = pos + len(waveform)
        if end <= duration_frames:
            trace[pos:end] += waveform

    return trace


# ---------------------------------------------------------------------------
# Threshold-based spike detector
# ---------------------------------------------------------------------------

def detect_threshold_crossings(
    trace: np.ndarray,
    threshold: float,
    refractory_frames: int = 30,
) -> list[int]:
    """
    Detect positive threshold crossings with a refractory period.

    Returns a list of frame indices at which a spike was detected.
    This mirrors the SSD logic in RealTimeSpikeSorter: when the signal
    exceeds the threshold the window is flagged as an event.
    """
    detections: list[int] = []
    last_detection = -refractory_frames  # allow detection from frame 0

    for i, val in enumerate(trace):
        if val >= threshold and (i - last_detection) >= refractory_frames:
            detections.append(i)
            last_detection = i

    return detections


# ---------------------------------------------------------------------------
# Benchmark evaluation
# ---------------------------------------------------------------------------

def evaluate_detection(
    ground_truth: list[int],
    detections: list[int],
    tolerance: int = DETECTION_TOLERANCE_FRAMES,
) -> tuple[int, int, int]:
    """
    Match detections to ground-truth spikes within ±tolerance frames.

    Returns (true_positives, false_negatives, false_positives).
    """
    matched_gt:  set[int] = set()
    matched_det: set[int] = set()

    for det_idx, det in enumerate(detections):
        for gt_idx, gt in enumerate(ground_truth):
            if gt_idx in matched_gt:
                continue
            if abs(det - gt) <= tolerance:
                matched_gt.add(gt_idx)
                matched_det.add(det_idx)
                break

    tp = len(matched_gt)
    fn = len(ground_truth) - tp
    fp = len(detections) - len(matched_det)
    return tp, fn, fp


def run_benchmark(
    name: str,
    spike_positions: list[int],
    duration_frames: int = 30_000,
    noise_std: float = 0.1,
    threshold: float = 0.9,
) -> bool:
    """
    Execute one benchmark scenario and return True if it passes quality gates.
    """
    trace = _make_synthetic_trace(duration_frames, spike_positions, noise_std)
    detections = detect_threshold_crossings(trace, threshold)

    tp, fn, fp = evaluate_detection(spike_positions, detections)
    total_gt  = len(spike_positions)
    total_det = len(detections)

    fn_rate = fn / total_gt  if total_gt  > 0 else 0.0
    fp_rate = fp / total_det if total_det > 0 else 0.0

    passed = fn_rate <= MAX_FALSE_NEGATIVE_RATE and fp_rate <= MAX_FALSE_POSITIVE_RATE

    status = "PASS" if passed else "FAIL"
    logging.info(
        f"{status}  {name}: "
        f"TP={tp}, FN={fn} (rate={fn_rate:.2%}), FP={fp} (rate={fp_rate:.2%})"
    )
    if not passed:
        if fn_rate > MAX_FALSE_NEGATIVE_RATE:
            logging.error(
                f"      False-negative rate {fn_rate:.2%} exceeds limit "
                f"{MAX_FALSE_NEGATIVE_RATE:.2%}"
            )
        if fp_rate > MAX_FALSE_POSITIVE_RATE:
            logging.error(
                f"      False-positive rate {fp_rate:.2%} exceeds limit "
                f"{MAX_FALSE_POSITIVE_RATE:.2%}"
            )

    return passed


# ---------------------------------------------------------------------------
# Benchmark scenarios
# Each tuple: (label, spike_positions, duration_frames, noise_std, threshold)
# ---------------------------------------------------------------------------
BENCHMARKS = [
    ("Single spike — low noise",    [15_000],                    30_000, 0.05, 0.9),
    ("Multiple spikes — low noise", [5_000, 12_000, 20_000, 27_000], 30_000, 0.05, 0.9),
    ("Single spike — high noise",   [15_000],                    30_000, 0.20, 0.9),
    ("Dense spikes — medium noise", list(range(BENCHMARK_SPIKE_INTERVAL_FRAMES, BENCHMARK_DURATION_FRAMES, BENCHMARK_SPIKE_INTERVAL_FRAMES)), BENCHMARK_DURATION_FRAMES, 0.10, 0.9),
]


def main() -> int:
    """Run all benchmarks and return 0 on success, 1 if any benchmark fails."""
    logging.info("=== Spike-Sorting Quality Audit ===")
    logging.info(
        f"Tolerance: ±{DETECTION_TOLERANCE_FRAMES} frames  |  "
        f"Max FN rate: {MAX_FALSE_NEGATIVE_RATE:.0%}  |  "
        f"Max FP rate: {MAX_FALSE_POSITIVE_RATE:.0%}"
    )

    results = [
        run_benchmark(name, spikes, duration, noise, threshold)
        for name, spikes, duration, noise, threshold in BENCHMARKS
    ]

    passed = sum(results)
    total  = len(results)
    logging.info(f"=== Results: {passed}/{total} benchmarks passed ===")

    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
