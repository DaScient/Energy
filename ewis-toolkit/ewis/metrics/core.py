from __future__ import annotations

from typing import Any, Dict, Optional

EPS = 1e-9


def _get(d: Dict[str, Any], key: str, default: Optional[float] = None) -> Optional[float]:
    v = d.get(key, default)
    if v is None:
        return None
    try:
        return float(v)
    except Exception:
        return default


def grid_stress_index(payload: Dict[str, Any], alpha: float = 1.0, beta: float = 0.25) -> Dict[str, Any]:
    """Compute a reference Grid Stress Index (GSI).

    Requires: power_mw.
    Optional: grid_capacity_mw, base_grid_load_mw, plus weather fields for severity.

    Returns a dict with fields: value, components, notes.
    """
    p_dc = _get(payload, "power_mw", 0.0) or 0.0
    c_grid = _get(payload, "grid_capacity_mw")
    l_base = _get(payload, "base_grid_load_mw")

    # Weather severity: simple normalization based on temp/humidity/precip. Plugins can override.
    temp = _get(payload, "ambient_temp_c")
    hum = _get(payload, "humidity_pct")
    precip = _get(payload, "precip_mm")

    severity = 0.0
    if temp is not None:
        # 0 at <= 15C, 1 at >= 40C
        severity += min(1.0, max(0.0, (temp - 15.0) / 25.0)) * 0.6
    if hum is not None:
        severity += min(1.0, max(0.0, hum / 100.0)) * 0.25
    if precip is not None:
        severity += min(1.0, max(0.0, precip / 50.0)) * 0.15

    if c_grid is None or l_base is None:
        return {
            "value": None,
            "components": {"P_dc": p_dc, "alpha": alpha, "beta": beta, "W_severity": severity},
            "notes": "grid_capacity_mw and base_grid_load_mw required for absolute GSI; returned None",
        }

    denom = max(EPS, (c_grid - l_base))
    value = (p_dc * max(0.0, min(1.0, alpha))) / denom + beta * max(0.0, min(1.0, severity))
    return {
        "value": float(value),
        "components": {
            "P_dc": p_dc,
            "alpha": alpha,
            "C_grid": c_grid,
            "L_base": l_base,
            "beta": beta,
            "W_severity": severity,
        },
        "notes": None,
    }


def energy_per_token(payload: Dict[str, Any]) -> Dict[str, Any]:
    workload = payload.get("workload") or {}
    energy_kwh = _get(workload, "energy_kwh")
    tokens = _get(workload, "tokens")
    if energy_kwh is None or tokens is None:
        return {"value": None, "notes": "workload.energy_kwh and workload.tokens required"}
    return {"value": float(energy_kwh) / max(EPS, float(tokens)), "notes": None}


def carbon_per_token(payload: Dict[str, Any]) -> Dict[str, Any]:
    workload = payload.get("workload") or {}
    energy_kwh = _get(workload, "energy_kwh")
    tokens = _get(workload, "tokens")
    ci = _get(payload, "carbon_intensity_kgco2_per_mwh")
    if energy_kwh is None or tokens is None or ci is None:
        return {"value": None, "notes": "carbon_intensity_kgco2_per_mwh, workload.energy_kwh, workload.tokens required"}
    kg = (ci * float(energy_kwh) / 1000.0)
    return {"value": float(kg) / max(EPS, float(tokens)), "notes": None}

