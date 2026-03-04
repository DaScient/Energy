from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ewis.core.context import PluginContext
from ewis.core.payloads import TelemetryPayload
from ewis.core.plugin_manager import BasePlugin, PluginManager, PluginResult
from ewis.metrics.core import (
    carbon_per_token,
    energy_per_token,
    grid_stress_index,
)
from ewis.report import EWISReport


@dataclass
class EngineConfig:
    allow_side_effects: bool = False
    plugin_timeout_s: int = 10
    extra: Dict[str, Any] | None = None


class EWISEngine:
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

    def run(self, payload: Dict[str, Any]) -> EWISReport:
        validated = TelemetryPayload(**payload).to_dict()

        plugin_results: List[PluginResult] = self.plugins.run_all(validated)

        metrics: Dict[str, Any] = {}
        metrics["grid_stress_index"] = grid_stress_index(validated)
        metrics["energy_per_token"] = energy_per_token(validated)
        metrics["carbon_per_token"] = carbon_per_token(validated)

        return EWISReport(
            payload=validated,
            metrics=metrics,
            plugin_results=plugin_results,
        )

