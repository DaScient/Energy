from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

import typer
import yaml
from rich.console import Console
from rich.pretty import Pretty

from phiak.core.engine import EngineConfig, PHIAKEngine
from phiak.core.plugin_manager import import_symbol

app = typer.Typer(add_completion=False, help="PHIAK CLI")
console = Console()


def _load_yaml(path: Path) -> Dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


@app.command()
def diagnose(
    config: Path = typer.Option(..., exists=True, file_okay=True, dir_okay=False, help="YAML config path"),
    out: Optional[Path] = typer.Option(None, help="Write report JSON to this path"),
) -> None:
    cfg = _load_yaml(config)

    engine_cfg = cfg.get("engine", {}) or {}
    engine = PHIAKEngine(
        EngineConfig(
            allow_side_effects=bool(engine_cfg.get("allow_side_effects", False)),
            plugin_timeout_s=int(engine_cfg.get("plugin_timeout_s", 10)),
            suppression_k=int(engine_cfg.get("suppression_k", 11)),
            extra=cfg.get("context", {}) or {},
        )
    )

    plugin_cfg = (cfg.get("plugins", {}) or {}).get("builtins", []) or []
    for dotted in plugin_cfg:
        cls = import_symbol(dotted)
        engine.register(cls())  # type: ignore[misc]

    inputs = cfg.get("inputs", {}) or {}
    report = engine.run_from_paths(
        incidence_path=str(inputs["incidence_path"]),
        capacity_path=str(inputs["capacity_path"]),
        wastewater_path=str(inputs["wastewater_path"]),
    ).to_json_dict()

    console.print(Pretty(report))

    if out is not None:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2), encoding="utf-8")
        console.print(f"Wrote: {out}")


if __name__ == "__main__":
    app()
