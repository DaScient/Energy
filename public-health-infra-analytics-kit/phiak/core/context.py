from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class PluginContext:
    config: Dict[str, Any]
    allow_side_effects: bool = False
    plugin_timeout_s: int = 10
    cache: Dict[str, Any] = field(default_factory=dict)
    runtime_metadata: Dict[str, Any] = field(default_factory=dict)

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        return self.config.get(key, default)
