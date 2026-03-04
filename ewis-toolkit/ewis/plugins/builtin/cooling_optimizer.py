from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from ewis.core.context import PluginContext
from ewis.core.plugin_manager import BasePlugin, PluginResult


@dataclass
class CoolingOptimizerPlugin(BasePlugin):
    """Reference cooling optimizer.

    This plugin estimates a recommended cooling posture given ambient conditions and PUE.
    It does not control equipment. It returns a suggestion that can be consumed by other systems.
    """

    def __init__(self, name: str = "cooling_optimizer"):
        super().__init__(name=name)

    def initialize(self, context: PluginContext) -> None:
        return

    def execute(self, payload: Dict[str, Any], context: PluginContext) -> PluginResult:
        temp = payload.get("ambient_temp_c")
        hum = payload.get("humidity_pct")
        pue = float(payload.get("pue", 1.2))

        score = 0.0
        if temp is not None:
            score += max(0.0, min(1.0, (float(temp) - 18.0) / 20.0)) * 0.7
        if hum is not None:
            score += max(0.0, min(1.0, float(hum) / 100.0)) * 0.3

        # If PUE is already high, emphasize action.
        score = min(1.0, score + max(0.0, min(0.25, (pue - 1.25) * 0.5)))

        posture = "normal"
        if score > 0.75:
            posture = "aggressive_cooling"
        elif score > 0.45:
            posture = "elevated_cooling"

        return PluginResult(
            name=self.name,
            ok=True,
            data={
                "cooling_score": score,
                "recommended_posture": posture,
                "assumptions": {
                    "control_plane": "none",
                    "note": "reference heuristic only; replace with facility model or control integration",
                },
            },
            metadata={"pue": pue},
        )

