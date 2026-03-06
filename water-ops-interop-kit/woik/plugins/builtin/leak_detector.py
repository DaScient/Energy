from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from woik.core.context import PluginContext
from woik.core.plugin_manager import BasePlugin, PluginResult
from woik.metrics.core import leak_likelihood_heuristic


@dataclass
class LeakDetectorPlugin(BasePlugin):
    def __init__(self, name: str = "leak_detector"):
        super().__init__(name=name)

    def initialize(self, context: PluginContext) -> None:
        return

    def execute(self, payload: Dict[str, Any], context: PluginContext) -> PluginResult:
        score = leak_likelihood_heuristic(payload)
        flag = None if score["value"] is None else bool(score["value"] >= 0.75)
        return PluginResult(
            name=self.name,
            ok=True,
            data={"lls": score, "alarm": flag},
            metadata={"threshold": 0.75, "method": "reference_heuristic"},
        )
