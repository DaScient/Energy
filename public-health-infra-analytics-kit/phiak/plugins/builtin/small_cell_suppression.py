from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from phiak.core.context import PluginContext
from phiak.core.plugin_manager import BasePlugin, PluginResult


@dataclass
class SmallCellSuppressionPlugin(BasePlugin):
    def __init__(self, name: str = "small_cell_suppression"):
        super().__init__(name=name)

    def initialize(self, context: PluginContext) -> None:
        return

    def _suppress_counts(self, rows: List[Dict[str, Any]], keys: List[str], k: int) -> Dict[str, Any]:
        suppressed = 0
        total = 0
        for r in rows:
            for key in keys:
                if key in r and r[key] is not None:
                    total += 1
                    v = int(r[key])
                    if v < k:
                        r[key] = None
                        suppressed += 1
        return {"suppressed_cells": suppressed, "total_cells": total, "k": k}

    def execute(self, payload: Dict[str, Any], context: PluginContext) -> PluginResult:
        k = int(payload.get("suppression_k", 11))
        incidence = payload.get("incidence", [])
        capacity = payload.get("capacity", [])

        inc_stats = self._suppress_counts(incidence, ["cases", "tests", "positive", "ed_ili_visits"], k)
        cap_stats = self._suppress_counts(capacity, ["ed_beds_available", "icu_beds_available"], k)

        return PluginResult(
            name=self.name,
            ok=True,
            data={"incidence": inc_stats, "capacity": cap_stats},
            metadata={"note": "suppression by minimum cell count; reference policy"},
        )
