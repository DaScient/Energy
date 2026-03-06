from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from phiak.core.context import PluginContext
from phiak.core.io import read_capacity_csv, read_incidence_csv, read_wastewater_csv
from phiak.core.plugin_manager import BasePlugin, PluginManager, PluginResult
from phiak.core.privacy import assert_no_forbidden_fields
from phiak.report import PHIAKReport


@dataclass
class EngineConfig:
    allow_side_effects: bool = False
    plugin_timeout_s: int = 10
    suppression_k: int = 11
    extra: Dict[str, Any] | None = None


class PHIAKEngine:
    def __init__(self, config: Optional[EngineConfig] = None):
        config = config or EngineConfig()
        self.context = PluginContext(
            config=config.extra or {},
            allow_side_effects=config.allow_side_effects,
            plugin_timeout_s=config.plugin_timeout_s,
        )
        self.suppression_k = int(config.suppression_k)
        self.plugins = PluginManager(self.context)

    def register(self, plugin: BasePlugin) -> None:
        self.plugins.register(plugin)

    def run_from_paths(self, incidence_path: str, capacity_path: str, wastewater_path: str) -> PHIAKReport:
        incidence = read_incidence_csv(incidence_path)
        capacity = read_capacity_csv(capacity_path)
        wastewater = read_wastewater_csv(wastewater_path)

        assert_no_forbidden_fields(incidence)
        assert_no_forbidden_fields(capacity)
        assert_no_forbidden_fields(wastewater)

        payload: Dict[str, Any] = {
            "incidence": incidence,
            "capacity": capacity,
            "wastewater": wastewater,
            "suppression_k": self.suppression_k,
        }

        plugin_results: List[PluginResult] = self.plugins.run_all(payload)

        inputs_summary = {
            "incidence_rows": len(incidence),
            "capacity_rows": len(capacity),
            "wastewater_rows": len(wastewater),
            "suppression_k": self.suppression_k,
        }

        return PHIAKReport(
            context=self.context.config,
            inputs_summary=inputs_summary,
            plugin_results=plugin_results,
        )
