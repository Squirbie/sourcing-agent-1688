from __future__ import annotations

import json
import re
from typing import Any

from bs4 import BeautifulSoup


def _walk_json(value: Any) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    if isinstance(value, dict):
        if any(key in value for key in ["offerId", "offer_id", "subject", "priceRange", "skuOptions", "monthSold"]):
            found.append(value)
        for child in value.values():
            found.extend(_walk_json(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(_walk_json(child))
    return found


def extract_embedded_json_candidates(soup: BeautifulSoup, html: str) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for script in soup.find_all("script"):
        text = script.string or script.get_text() or ""
        text = text.strip()
        if not text:
            continue
        if script.get("type") == "application/json":
            try:
                candidates.extend(_walk_json(json.loads(text)))
                continue
            except json.JSONDecodeError:
                pass
        for match in re.finditer(r"\{[^{}]*(?:offerId|offer_id|subject|priceRange|skuOptions|monthSold)[\s\S]*?\}", text):
            raw = match.group(0)
            try:
                candidates.extend(_walk_json(json.loads(raw)))
            except json.JSONDecodeError:
                continue
    return candidates


def merge_candidates(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    merged: dict[str, Any] = {}
    for candidate in candidates:
        for key, value in candidate.items():
            if value not in (None, "", [], {}) and key not in merged:
                merged[key] = value
    return merged

