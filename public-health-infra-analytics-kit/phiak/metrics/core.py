from __future__ import annotations

from typing import Any, Dict, Optional

EPS = 1e-9


def _f(v: Any) -> Optional[float]:
    if v is None:
        return None
    try:
        return float(v)
    except Exception:
        return None


def positivity_rate(positive: Optional[float], tests: Optional[float]) -> Dict[str, Any]:
    if positive is None or tests is None:
        return {"value": None, "notes": "positive and tests required"}
    if tests <= 0:
        return {"value": None, "notes": "tests must be > 0"}
    return {"value": float(positive) / float(tests), "notes": None}


def occupancy_rate(available: Optional[float], total: Optional[float]) -> Dict[str, Any]:
    if available is None or total is None:
        return {"value": None, "notes": "available and total required"}
    if total <= 0:
        return {"value": None, "notes": "total must be > 0"}
    used = float(total) - float(available)
    return {"value": used / max(EPS, float(total)), "notes": None}


def early_warning_index(z_incidence: float, z_syndromic: float, z_wastewater: float, z_capacity: float) -> float:
    return 0.35 * z_incidence + 0.25 * z_syndromic + 0.25 * z_wastewater + 0.15 * z_capacity
