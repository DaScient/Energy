from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Event(BaseModel):
    type: str = Field(..., min_length=1)
    severity: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)
    source: str = Field(..., min_length=1)


class WOIKPayload(BaseModel):
    system_id: str = Field(..., min_length=1)
    asset_id: str = Field(..., min_length=1)
    asset_type: str = Field(..., min_length=1)
    timestamp_utc: str = Field(..., min_length=1)

    flow_m3_s: float = Field(..., ge=0.0)
    pressure_kpa: float = Field(..., ge=0.0)
    level_m: float = Field(..., ge=0.0)

    valve_position_pct: Optional[float] = Field(default=None, ge=0.0, le=100.0)
    pump_speed_rpm: Optional[float] = Field(default=None, ge=0.0)
    pump_power_kw: Optional[float] = Field(default=None, ge=0.0)

    turbidity_ntu: Optional[float] = Field(default=None, ge=0.0)
    chlorine_mg_l: Optional[float] = Field(default=None, ge=0.0)
    ph: Optional[float] = Field(default=None, ge=0.0, le=14.0)
    conductivity_us_cm: Optional[float] = Field(default=None, ge=0.0)
    temperature_c: Optional[float] = None

    lab_results: Optional[Dict[str, Any]] = None

    electricity_price_usd_kwh: Optional[float] = Field(default=None, ge=0.0)
    carbon_intensity_kgco2_kwh: Optional[float] = Field(default=None, ge=0.0)

    events: Optional[List[Event]] = None
    maintenance: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(mode="python", exclude_none=True)
