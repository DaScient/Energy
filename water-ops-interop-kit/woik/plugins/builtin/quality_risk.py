from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from woik.core.context import PluginContext
from woik.core.plugin_manager import BasePlugin, PluginResult
from woik.metrics.core import water_quality_risk


@dataclass
class QualityRiskPlugin(BasePlugin):
    def __init__(self, name: str = "quality_risk"):
        super().__init__(name=name)

    def initialize(self, context: PluginContext) -> None:
        return

    def execute(self, payload: Dict[str, Any], context: PluginContext) -> PluginResult:
        wq = water_quality_risk(payload)
        band = None
        if wq["value"] is not None:
            v = float(wq["value"])
            if v < 0.25:
                band = "low"
            elif v < 0.55:
                band = "moderate"
            else:
                band = "high"
        return PluginResult(
            name=self.name,
            ok=True,
            data={"wqri": wq, "band": band},
            metadata={"method": "reference_heuristic"},
        )
