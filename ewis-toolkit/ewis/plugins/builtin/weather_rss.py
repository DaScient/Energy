from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

import requests
from tenacity import retry, stop_after_attempt, wait_exponential

from ewis.core.context import PluginContext
from ewis.core.plugin_manager import BasePlugin, PluginResult


@dataclass
class WeatherRssPlugin(BasePlugin):
    """Fetch a set of RSS/Atom feeds and return normalized headlines.

    This is a reference plugin. Organizations should replace with their preferred sources and parsers.
    """

    rss_urls: List[str]
    timeout_s: int = 8

    def __init__(self, name: str = "weather_rss", rss_urls: Optional[List[str]] = None, timeout_s: int = 8):
        super().__init__(name=name)
        self.rss_urls = rss_urls or []
        self.timeout_s = timeout_s

    def initialize(self, context: PluginContext) -> None:
        return

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, min=0.5, max=4))
    def _fetch(self, url: str) -> str:
        r = requests.get(url, timeout=self.timeout_s)
        r.raise_for_status()
        return r.text

    def execute(self, payload: Dict[str, Any], context: PluginContext) -> PluginResult:
        items: List[Dict[str, Any]] = []
        for url in self.rss_urls:
            try:
                xml = self._fetch(url)
                # Extremely small XML extraction to avoid adding heavy deps.
                # For production, prefer feedparser or a structured RSS library.
                titles = []
                for line in xml.splitlines():
                    line = line.strip()
                    if line.lower().startswith("<title>") and line.lower().endswith("</title>"):
                        t = line[7:-8].strip()
                        if t:
                            titles.append(t)
                host = urlparse(url).netloc
                for t in titles[:10]:
                    items.append({"source": host, "title": t})
            except Exception as e:
                items.append({"source": url, "error": str(e)})

        return PluginResult(
            name=self.name,
            ok=True,
            data={"headlines": items},
            metadata={"count": len(items), "timeout_s": self.timeout_s},
        )

