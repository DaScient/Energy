from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from woik.core.plugin_manager import PluginResult


@dataclass
class WOIKReport:
    payload: Dict[str, Any]
    metrics: Dict[str, Any]
    plugin_results: List[PluginResult]

    def summary(self) -> Dict[str, Any]:
        return {
            "system_id": self.payload.get("system_id"),
            "asset_id": self.payload.get("asset_id"),
            "asset_type": self.payload.get("asset_type"),
            "timestamp_utc": self.payload.get("timestamp_utc"),
            "metrics": self.metrics,
            "plugins": [{"name": r.name, "ok": r.ok, "metadata": r.metadata} for r in self.plugin_results],
        }

    def to_json_dict(self) -> Dict[str, Any]:
        return {
            "payload": self.payload,
            "metrics": self.metrics,
            "plugin_results": [
                {"name": r.name, "ok": r.ok, "data": r.data, "metadata": r.metadata} for r in self.plugin_results
            ],
        }
