from __future__ import annotations

import re
from urllib.parse import urlparse

from bs4 import BeautifulSoup


IMAGE_HOST_MARKERS = ("alicdn.com", "aliimg.com")
VIDEO_EXTENSIONS = (".mp4", ".m3u8", ".mov")
PLACEHOLDER_MARKERS = ("lazyload", "placeholder", "loading.gif", "blank.gif", "transparent")


def safe_urlparse(url: str):
    try:
        return urlparse(url)
    except ValueError:
        return None


def normalize_url(url: str) -> str | None:
    url = url.strip().strip("'\"").rstrip("),.;]}")
    if not url or url.startswith("data:"):
        return None
    if url.startswith("//"):
        url = f"https:{url}"
    if url.startswith("http://"):
        url = "https://" + url[len("http://") :]
    if not url.startswith("https://"):
        return None
    lowered = url.lower()
    if any(marker in lowered for marker in PLACEHOLDER_MARKERS):
        return None
    parsed = safe_urlparse(url)
    if not parsed or not parsed.netloc:
        return None
    if any(char in parsed.netloc for char in "[]*"):
        return None
    return url


def dedupe_urls(urls: list[str]) -> list[str]:
    seen: set[str] = set()
    deduped: list[str] = []
    for url in urls:
        normalized = normalize_url(url)
        if normalized and normalized not in seen:
            seen.add(normalized)
            deduped.append(normalized)
    return deduped


def extract_urls_from_text(text: str) -> tuple[list[str], list[str]]:
    candidates = re.findall(r"(?:https?:)?//[^'\"\s<>\\]+", text)
    images: list[str] = []
    videos: list[str] = []
    for candidate in candidates:
        normalized = normalize_url(candidate)
        if not normalized:
            continue
        lowered = normalized.lower()
        parsed = safe_urlparse(lowered)
        if not parsed:
            continue
        if any(lowered.split("?")[0].endswith(ext) for ext in VIDEO_EXTENSIONS) or "video" in parsed.netloc:
            videos.append(normalized)
        elif any(host in lowered for host in IMAGE_HOST_MARKERS) or re.search(r"\.(jpe?g|png|webp|gif)(?:\?|$)", lowered):
            images.append(normalized)
    return dedupe_urls(images), dedupe_urls(videos)


def extract_assets(soup: BeautifulSoup, html: str) -> dict[str, list[str]]:
    main: list[str] = []
    detail: list[str] = []
    option: list[str] = []
    videos: list[str] = []

    for img in soup.find_all("img"):
        raw_url = img.get("data-src") or img.get("data-original") or img.get("src")
        if not raw_url:
            continue
        url = normalize_url(str(raw_url))
        if not url:
            continue
        asset_type = " ".join(str(v) for v in [img.get("data-asset-type"), img.get("class"), img.get("id")] if v).lower()
        if "option" in asset_type or "sku" in asset_type or "color" in asset_type:
            option.append(url)
        elif "detail" in asset_type or "desc" in asset_type:
            detail.append(url)
        else:
            main.append(url)

    for element in soup.find_all(style=True):
        style_images, _ = extract_urls_from_text(str(element.get("style") or ""))
        detail.extend(style_images)

    for video in soup.find_all(["video", "source"]):
        raw_url = video.get("src") or video.get("data-src")
        if raw_url and (url := normalize_url(str(raw_url))):
            videos.append(url)

    script_images, script_videos = extract_urls_from_text(html)
    for url in script_images:
        if url not in main and url not in detail and url not in option:
            detail.append(url)
    videos.extend(script_videos)

    return {
        "main_images": dedupe_urls(main),
        "detail_images": dedupe_urls(detail),
        "option_images": dedupe_urls(option),
        "videos": dedupe_urls(videos),
    }
