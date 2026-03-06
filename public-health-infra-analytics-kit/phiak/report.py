from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from phiak.core.plugin_manager import PluginResult


@dataclass
class PHIAKReport:
    context: Dict[str, Any]
    inputs_summary: Dict[str, Any]
    plugin_results: List[PluginResult]

    def to_json_dict(self) -> Dict[str, Any]:
        return {
            "context": self.context,
            "inputs_summary": self.inputs_summary,
            "plugin_results": [
                {"name": r.name, "ok": r.ok, "data": r.data, "metadata": r.metadata} for r in self.plugin_results
            ],
        }
