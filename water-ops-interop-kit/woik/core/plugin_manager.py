from __future__ import annotations

import importlib
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from woik.core.context import PluginContext
from woik.core.errors import PluginExecutionError


@dataclass(frozen=True)
class PluginResult:
    name: str
    ok: bool
    data: Dict[str, Any]
    metadata: Dict[str, Any]


class BasePlugin(ABC):
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def initialize(self, context: PluginContext) -> None:
        ...

    @abstractmethod
    def execute(self, payload: Dict[str, Any], context: PluginContext) -> PluginResult:
        ...

    def teardown(self, context: PluginContext) -> None:
        return


def import_symbol(dotted: str) -> Any:
    module, _, sym = dotted.rpartition(":")
    if not module or not sym:
        raise ValueError(f"Invalid dotted path: {dotted}. Expected module:Symbol")
    mod = importlib.import_module(module)
    return getattr(mod, sym)


class PluginManager:
    def __init__(self, context: PluginContext):
        self.context = context
        self.plugins: Dict[str, BasePlugin] = {}

    def register(self, plugin: BasePlugin) -> None:
        if plugin.name in self.plugins:
            raise ValueError(f"Plugin already registered: {plugin.name}")
        plugin.initialize(self.context)
        self.plugins[plugin.name] = plugin

    def run_all(self, payload: Dict[str, Any]) -> List[PluginResult]:
        results: List[PluginResult] = []
        for name, plugin in self.plugins.items():
            try:
                results.append(plugin.execute(payload, self.context))
            except Exception as e:
                raise PluginExecutionError(f"Plugin failed: {name}: {e}") from e
        return results
