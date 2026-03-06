from __future__ import annotations

from typing import List

import pandas as pd

from phiak.core.payloads import CapacityPayload, IncidencePayload, WastewaterPayload


def read_incidence_csv(path: str) -> List[dict]:
    df = pd.read_csv(path)
    out: List[dict] = []
    for _, r in df.iterrows():
        out.append(IncidencePayload(**r.to_dict()).to_dict())
    return out


def read_capacity_csv(path: str) -> List[dict]:
    df = pd.read_csv(path)
    out: List[dict] = []
    for _, r in df.iterrows():
        out.append(CapacityPayload(**r.to_dict()).to_dict())
    return out


def read_wastewater_csv(path: str) -> List[dict]:
    df = pd.read_csv(path)
    out: List[dict] = []
    for _, r in df.iterrows():
        out.append(WastewaterPayload(**r.to_dict()).to_dict())
    return out
