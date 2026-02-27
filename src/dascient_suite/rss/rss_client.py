import json
import hashlib
from typing import Any, Dict, List
import requests
import feedparser

DEFAULT_UA = "DaScient-RSS-Weather-Energy-Suite/0.1"

def stable_hash(obj: Any) -> str:
    blob = json.dumps(obj, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:16]

def fetch_rss(url: str, timeout_s: int = 30, user_agent: str = DEFAULT_UA) -> feedparser.FeedParserDict:
    headers = {"User-Agent": user_agent}
    resp = requests.get(url, headers=headers, timeout=timeout_s)
    resp.raise_for_status()
    return feedparser.parse(resp.content)

def normalize_entry(e: Any) -> Dict[str, str]:
    title = (e.get("title", "") or "").strip()
    link = (e.get("link", "") or "").strip()
    summary = ((e.get("summary", "") or e.get("description", "") or "")).strip()
    published = (e.get("published", "") or e.get("updated", "") or "").strip()
    return {"title": title, "link": link, "summary": summary, "published_raw": published}

def pull_feeds(sources: List[Dict[str, str]], limit_per_feed: int = 40) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for s in sources:
        feed = fetch_rss(s["url"])
        for e in (feed.entries or [])[:limit_per_feed]:
            r = normalize_entry(e)
            r["source"] = s.get("source", "unknown")
            r["feed_url"] = s["url"]
            r["id"] = stable_hash({"t": r["title"], "l": r["link"]})
            rows.append(r)
    seen = set()
    out = []
    for r in rows:
        if r["id"] in seen:
            continue
        seen.add(r["id"])
        out.append(r)
    return out
