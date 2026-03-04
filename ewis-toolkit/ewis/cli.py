from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

import typer
import yaml
from rich.console import Console
from rich.pretty import Pretty

from ewis.core.engine import EWISEngine, EngineConfig
from ewis.core.plugin_manager import discover_local_plugins, import_symbol

app = typer.Typer(add_completion=False, help="EWIS Toolkit CLI")
console = Console()


def _load_yaml(path: Path) -> Dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


@app.command()
def diagnose(
    config: Path = typer.Option(..., exists=True, file_okay=True, dir_okay=False, help="YAML config path"),
    payload_json: Optional[Path] = typer.Option(
        None, exists=True, file_okay=True, dir_okay=False, help="Optional JSON payload override"
    ),
    out: Optional[Path] = typer.Option(None, help="Write report JSON to this path"),
) -> None:
    """Run an EWIS diagnostic with configured plugins."""
    cfg = _load_yaml(config)

    engine_cfg = cfg.get("engine", {}) or {}
    engine = EWISEngine(
        EngineConfig(
            allow_side_effects=bool(engine_cfg.get("allow_side_effects", False)),
            plugin_timeout_s=int(engine_cfg.get("plugin_timeout_s", 10)),
            extra=cfg,
        )
    )

    # Register builtins by dotted paths
    plugin_cfg = (cfg.get("plugins", {}) or {}).get("builtins", []) or []
    for dotted in plugin_cfg:
        cls = import_symbol(dotted)
        plugin = cls()  # type: ignore[misc]
        engine.register(plugin)

    # Register local drop-ins if present
    for module in discover_local_plugins():
        try:
            console.print(f"[dim]Discovered local plugin module:[/dim] {module}")
        except Exception:
            pass

    if payload_json is not None:
        payload = json.loads(payload_json.read_text(encoding="utf-8"))
    else:
        payload = (cfg.get("telemetry", {}) or {})

    report = engine.run(payload).to_json_dict()

    console.print(Pretty(report))

    if out is not None:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2), encoding="utf-8")
        console.print(f"Wrote: {out}")


@app.command()
def schema() -> None:
    """Print the minimal payload schema."""
    from ewis.core.payloads import TelemetryPayload

    console.print(TelemetryPayload.model_json_schema())


if __name__ == "__main__":
    app()
