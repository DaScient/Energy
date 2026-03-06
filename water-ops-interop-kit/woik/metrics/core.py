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


def sigmoid(x: float) -> float:
    import math
    if x >= 0:
        z = math.exp(-x)
        return 1.0 / (1.0 + z)
    z = math.exp(x)
    return z / (1.0 + z)


def leak_likelihood_heuristic(payload: Dict[str, Any]) -> Dict[str, Any]:
    flow = _f(payload.get("flow_m3_s"))
    pressure = _f(payload.get("pressure_kpa"))
    if flow is None or pressure is None:
        return {"value": None, "notes": "flow_m3_s and pressure_kpa required"}

    x = 2.2 * (flow - 0.4) - 0.006 * (pressure - 450)
    return {"value": float(sigmoid(x)), "notes": "reference heuristic only"}


def pump_specific_energy(payload: Dict[str, Any]) -> Dict[str, Any]:
    power_kw = _f(payload.get("pump_power_kw"))
    flow = _f(payload.get("flow_m3_s"))
    if power_kw is None or flow is None:
        return {"value": None, "notes": "pump_power_kw and flow_m3_s required"}
    kj_per_m3 = float(power_kw) / max(EPS, float(flow))
    return {"value": kj_per_m3, "notes": "kJ per m3 (since kW = kJ/s)"}


def water_quality_risk(payload: Dict[str, Any]) -> Dict[str, Any]:
    turb = _f(payload.get("turbidity_ntu"))
    chl = _f(payload.get("chlorine_mg_l"))
    ph = _f(payload.get("ph"))

    if turb is None and chl is None and ph is None:
        return {"value": None, "notes": "at least one of turbidity_ntu, chlorine_mg_l, ph required"}

    turb_n = 0.0 if turb is None else min(1.0, max(0.0, (turb - 0.1) / 1.0))
    chl_low = 0.0 if chl is None else min(1.0, max(0.0, (0.6 - chl) / 0.6))
    ph_dev = 0.0 if ph is None else min(1.0, max(0.0, abs(ph - 7.0) / 2.0))

    value = 0.45 * turb_n + 0.35 * chl_low + 0.20 * ph_dev
    return {"value": float(value), "notes": "reference heuristic only; map to local thresholds"}
