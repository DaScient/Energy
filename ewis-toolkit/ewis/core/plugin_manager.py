from __future__ import annotations

import importlib
import pkgutil
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Type

from rich.console import Console

from ewis.core.context import PluginContext
from ewis.core.errors import PluginExecutionError


console = Console()


@dataclass(frozen=True)
class PluginResult:
    name: str
    ok: bool
    data: Dict[str, Any]
    metadata: Dict[str, Any]


class BasePlugin(ABC):
    """Base class for EWIS plugins."""

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


def discover_local_plugins(package_name: str = "plugins") -> List[str]:
    """Discover local drop-in plugin modules from a top-level `plugins/` folder.

    Returns import paths like `plugins.my_plugin_module`.
    """
    modules: List[str] = []
    try:
        pkg = importlib.import_module(package_name)
    except Exception:
        return modules

    for m in pkgutil.iter_modules(getattr(pkg, "__path__", [])):
        if m.ispkg:
            continue
        modules.append(f"{package_name}.{m.name}")
    return modules


def import_symbol(dotted: str) -> Any:
    module, _, sym = dotted.rpartition(":")
    if not module or not sym:
        raise ValueError(f"Invalid dotted path: {dotted}. Expected module:Symbol")
    mod = importlib.import_module(module)
    return getattr(mod, sym)


class PluginManager:
    """Registers and executes plugins."""

    def __init__(self, context: PluginContext):
        self.context = context
        self.plugins: Dict[str, BasePlugin] = {}

    def register(self, plugin: BasePlugin) -> None:
        if plugin.name in self.plugins:
            raise ValueError(f"Plugin already registered: {plugin.name}")
        plugin.initialize(self.context)
        self.plugins[plugin.name] = plugin

    def register_from_dotted(self, dotted: str, init_kwargs: Optional[Dict[str, Any]] = None) -> None:
        init_kwargs = init_kwargs or {}
        cls = import_symbol(dotted)
        plugin = cls(**init_kwargs)  # type: ignore[misc]
        if not isinstance(plugin, BasePlugin):
            raise TypeError("Plugin must inherit from BasePlugin")
        self.register(plugin)

    def run_all(self, payload: Dict[str, Any]) -> List[PluginResult]:
        results: List[PluginResult] = []
        for name, plugin in self.plugins.items():
            try:
                results.append(plugin.execute(payload, self.context))
            except Exception as e:
                raise PluginExecutionError(f"Plugin failed: {name}: {e}") from e
        return results

