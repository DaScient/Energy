from __future__ import annotations

from typing import Dict, Optional

from pydantic import BaseModel, Field


class IncidencePayload(BaseModel):
    date: str = Field(..., min_length=1)
    geo_id: str = Field(..., min_length=1)
    geo_level: str = Field(..., min_length=1)
    pathogen: str = Field(..., min_length=1)

    cases: int = Field(..., ge=0)
    tests: Optional[int] = Field(default=None, ge=0)
    positive: Optional[int] = Field(default=None, ge=0)

    ed_ili_visits: Optional[int] = Field(default=None, ge=0)
    ed_total_visits: Optional[int] = Field(default=None, ge=0)

    def to_dict(self) -> Dict:
        return self.model_dump(mode="python", exclude_none=True)


class CapacityPayload(BaseModel):
    date: str = Field(..., min_length=1)
    geo_id: str = Field(..., min_length=1)
    facility_type: str = Field(..., min_length=1)

    ed_beds_total: int = Field(..., ge=0)
    ed_beds_available: int = Field(..., ge=0)

    icu_beds_total: Optional[int] = Field(default=None, ge=0)
    icu_beds_available: Optional[int] = Field(default=None, ge=0)

    staffing_gap_pct: Optional[float] = Field(default=None, ge=0.0, le=1.0)

    def to_dict(self) -> Dict:
        return self.model_dump(mode="python", exclude_none=True)


class WastewaterPayload(BaseModel):
    date: str = Field(..., min_length=1)
    geo_id: str = Field(..., min_length=1)
    site_id: str = Field(..., min_length=1)
    target: str = Field(..., min_length=1)

    gene_copies_ml: float = Field(..., ge=0.0)
    flow_m3_d: Optional[float] = Field(default=None, ge=0.0)
    lab_qc_flag: Optional[str] = None

    def to_dict(self) -> Dict:
        return self.model_dump(mode="python", exclude_none=True)
