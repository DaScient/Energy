from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

import numpy as np
import pandas as pd

from phiak.core.context import PluginContext
from phiak.core.plugin_manager import BasePlugin, PluginResult
from phiak.metrics.core import early_warning_index, occupancy_rate, positivity_rate


def robust_z(series: pd.Series) -> float:
    s = series.dropna().astype(float)
    if len(s) < 3:
        return 0.0
    med = float(s.median())
    mad = float((s - med).abs().median())
    if mad <= 1e-9:
        return 0.0
    return float((s.iloc[-1] - med) / (1.4826 * mad))


@dataclass
class EarlyWarningPlugin(BasePlugin):
    def __init__(self, name: str = "early_warning"):
        super().__init__(name=name)

    def initialize(self, context: PluginContext) -> None:
        return

    def execute(self, payload: Dict[str, Any], context: PluginContext) -> PluginResult:
        inc = pd.DataFrame(payload.get("incidence", []))
        cap = pd.DataFrame(payload.get("capacity", []))
        ww = pd.DataFrame(payload.get("wastewater", []))

        z_inc = robust_z(inc["cases"]) if "cases" in inc else 0.0

        if "ed_ili_visits" in inc and "ed_total_visits" in inc:
            prop = inc["ed_ili_visits"].astype(float) / inc["ed_total_visits"].replace(0, np.nan).astype(float)
            z_syn = robust_z(prop)
        else:
            z_syn = 0.0

        if "gene_copies_ml" in ww:
            z_ww = robust_z(pd.to_numeric(ww["gene_copies_ml"], errors="coerce"))
            # baseline ratio as context
            g = pd.to_numeric(ww["gene_copies_ml"], errors="coerce").dropna()
            ww_ratio = None
            if len(g) >= 3:
                ww_ratio = float(g.iloc[-1] / max(1e-9, float(g.median())))
        else:
            z_ww = 0.0
            ww_ratio = None

        if "ed_beds_available" in cap and "ed_beds_total" in cap:
            occ = []
            for _, r in cap.iterrows():
                occ.append(occupancy_rate(r.get("ed_beds_available"), r.get("ed_beds_total"))["value"])
            z_cap = robust_z(pd.Series(occ))
        else:
            z_cap = 0.0

        ewi = float(early_warning_index(z_inc, z_syn, z_ww, z_cap))
        alert = bool(ewi >= 1.25)

        pos = None
        if "positive" in inc and "tests" in inc and len(inc):
            pos = positivity_rate(inc["positive"].iloc[-1], inc["tests"].iloc[-1])["value"]

        return PluginResult(
            name=self.name,
            ok=True,
            data={
                "z_trends": {"incidence": z_inc, "syndromic": z_syn, "wastewater": z_ww, "capacity": z_cap},
                "wastewater_ratio": ww_ratio,
                "positivity_latest": pos,
                "early_warning_index": ewi,
                "alert": alert,
                "interpretation": "EWI is a conservative trend composite. Treat as triage, not diagnosis.",
            },
            metadata={"alert_threshold": 1.25, "method": "robust_z_composite_v1"},
        )
