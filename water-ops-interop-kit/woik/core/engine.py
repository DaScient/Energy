from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from woik.core.context import PluginContext
from woik.core.payloads import WOIKPayload
from woik.core.plugin_manager import BasePlugin, PluginManager, PluginResult
from woik.metrics.core import leak_likelihood_heuristic, pump_specific_energy, water_quality_risk
from woik.report import WOIKReport


@dataclass
class EngineConfig:
    allow_side_effects: bool = False
    plugin_timeout_s: int = 10
    extra: Dict[str, Any] | None = None


class WOIKEngine:
    def __init__(self, config: Optional[EngineConfig] = None):
        config = config or EngineConfig()
        self.context = PluginContext(
            config=config.extra or {},
            allow_side_effects=config.allow_side_effects,
            plugin_timeout_s=config.plugin_timeout_s,
        )
        self.plugins = PluginManager(self.context)

    def register(self, plugin: BasePlugin) -> None:
        self.plugins.register(plugin)

    def run(self, payload: Dict[str, Any]) -> WOIKReport:
        validated = WOIKPayload(**payload).to_dict()
        plugin_results: List[PluginResult] = self.plugins.run_all(validated)

        metrics: Dict[str, Any] = {}
        metrics["leak_likelihood_score"] = leak_likelihood_heuristic(validated)
        metrics["pump_specific_energy_kj_m3"] = pump_specific_energy(validated)
        metrics["water_quality_risk_index"] = water_quality_risk(validated)

        return WOIKReport(payload=validated, metrics=metrics, plugin_results=plugin_results)
