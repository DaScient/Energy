from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, field_validator


class TelemetryPayload(BaseModel):
    datacenter_id: str = Field(..., min_length=1)
    region: str = Field(..., min_length=1)
    timestamp_utc: str = Field(..., min_length=1)

    power_mw: float = Field(..., ge=0.0)
    it_load_mw: float = Field(..., ge=0.0)
    pue: float = Field(..., ge=1.0)

    base_grid_load_mw: Optional[float] = Field(default=None, ge=0.0)
    grid_capacity_mw: Optional[float] = Field(default=None, ge=0.0)
    price_usd_per_mwh: Optional[float] = Field(default=None, ge=0.0)
    carbon_intensity_kgco2_per_mwh: Optional[float] = Field(default=None, ge=0.0)

    ambient_temp_c: Optional[float] = None
    humidity_pct: Optional[float] = Field(default=None, ge=0.0, le=100.0)
    wind_m_s: Optional[float] = Field(default=None, ge=0.0)
    precip_mm: Optional[float] = Field(default=None, ge=0.0)

    workload: Optional[Dict[str, Any]] = None

    @field_validator("it_load_mw")
    @classmethod
    def it_load_not_exceed_power(cls, v: float, info):  # type: ignore[override]
        # Pydantic v2 supplies context in info.data
        data = getattr(info, "data", {}) or {}
        power = data.get("power_mw")
        if power is not None and v > float(power) + 1e-9:
            raise ValueError("it_load_mw must be <= power_mw")
        return v

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(mode="python", exclude_none=True)

