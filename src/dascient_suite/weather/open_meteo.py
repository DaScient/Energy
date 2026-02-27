from typing import Dict
import pandas as pd
import numpy as np
import requests

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

def forecast_hourly(lat: float, lon: float, days: int = 10) -> pd.DataFrame:
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,relative_humidity_2m,dew_point_2m,wind_speed_10m,precipitation",
        "timezone": "UTC",
        "forecast_days": int(days),
    }
    r = requests.get(OPEN_METEO_URL, params=params, timeout=30)
    r.raise_for_status()
    j: Dict = r.json()
    h = j.get("hourly", {})
    t = pd.to_datetime(h.get("time", []), utc=True)
    return pd.DataFrame({
        "time_utc": t,
        "temp_c": h.get("temperature_2m", []),
        "rh_pct": h.get("relative_humidity_2m", []),
        "dew_c": h.get("dew_point_2m", []),
        "wind_ms": h.get("wind_speed_10m", []),
        "precip_mm": h.get("precipitation", []),
    })

def cooling_degree_hours(temp_c: pd.Series, base_c: float = 18.0) -> pd.Series:
    return np.maximum(temp_c - base_c, 0.0)

def heating_degree_hours(temp_c: pd.Series, base_c: float = 18.0) -> pd.Series:
    return np.maximum(base_c - temp_c, 0.0)
