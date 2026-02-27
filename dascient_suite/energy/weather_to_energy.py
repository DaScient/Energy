from typing import Tuple
import numpy as np
import pandas as pd

def estimate_cooling_kw(it_kw: float, cdh: pd.Series, rh_pct: pd.Series, k_cdh: float = 0.010, k_humid: float = 0.002) -> pd.Series:
    humid_penalty = np.maximum((rh_pct - 60.0) / 40.0, 0.0)
    return it_kw * (k_cdh * cdh + k_humid * humid_penalty)

def estimate_facility_kw(it_kw: float, cooling_kw: pd.Series, pue_floor: float = 1.08) -> pd.Series:
    return it_kw * pue_floor + cooling_kw

def peak_coincidence_factor(times_utc: pd.Series, facility_kw: pd.Series, peak_hours_utc: Tuple[int, int] = (16, 20)) -> float:
    start_h, end_h = peak_hours_utc
    mask = (times_utc.dt.hour >= start_h) & (times_utc.dt.hour <= end_h)
    if int(mask.sum()) == 0:
        return float("nan")
    return float(np.mean(facility_kw[mask]) / max(float(np.mean(facility_kw)), 1e-9))
