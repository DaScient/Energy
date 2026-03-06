from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from woik.core.context import PluginContext
from woik.core.plugin_manager import BasePlugin, PluginResult
from woik.metrics.core import pump_specific_energy


@dataclass
class PumpEfficiencyPlugin(BasePlugin):
    def __init__(self, name: str = "pump_efficiency"):
        super().__init__(name=name)

    def initialize(self, context: PluginContext) -> None:
        return

    def execute(self, payload: Dict[str, Any], context: PluginContext) -> PluginResult:
        pse = pump_specific_energy(payload)
        category = None
        if pse["value"] is not None:
            v = float(pse["value"])
            if v < 80:
                category = "excellent"
            elif v < 140:
                category = "good"
            elif v < 220:
                category = "fair"
            else:
                category = "poor"
        return PluginResult(
            name=self.name,
            ok=True,
            data={"pump_specific_energy_kj_m3": pse, "category": category},
            metadata={"note": "reference bands only; calibrate to station context"},
        )
