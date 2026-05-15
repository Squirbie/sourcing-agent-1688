from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from typing import Any


REVIEW_TAG_TERMS = (
    "价格",
    "质量",
    "性价比",
    "发货",
    "物流",
    "服务",
    "好评",
    "差评",
    "实惠",
    "不错",
    "满意",
)


def _as_text(value: Any) -> str:
    return str(value or "").strip()


def _loads(value: str) -> Any:
    try:
        return json.loads(value)
    except Exception:
        return None


def _walk(value: Any):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def _extract_summary_tags(text: str) -> list[dict[str, Any]]:
    tags: list[dict[str, Any]] = []
    seen: set[str] = set()
    for line in text.splitlines():
        clean = re.sub(r"\s+", " ", line).strip()
        if not clean or len(clean) > 50:
            continue
        match = re.search(r"(.{2,24}?)\s+(\d{1,6})$", clean)
        if not match:
            continue
        label = match.group(1).strip(" ：:")
        if not label or label in seen:
            continue
        if not any(term in label for term in REVIEW_TAG_TERMS):
            continue
        seen.add(label)
        tags.append({"label_zh": label, "count": int(match.group(2))})
    return tags


def _extract_review_texts(text: str) -> list[str]:
    reviews: list[str] = []
    for line in text.splitlines():
        clean = re.sub(r"\s+", " ", line).strip()
        if len(clean) < 12 or len(clean) > 240:
            continue
        if any(marker in clean for marker in ["暂无有效评价", "未找到符合您筛选的记录", "买家评价", "累计评价"]):
            continue
        if any(term in clean for term in REVIEW_TAG_TERMS):
            reviews.append(clean)
    return list(dict.fromkeys(reviews))[:20]


def _payload_signal(payload: str) -> dict[str, Any]:
    signal: dict[str, Any] = {
        "service": None,
        "status": None,
        "message": None,
        "review_count": None,
        "video_id_seen": False,
    }
    raw = payload[:4000]
    lowered = raw.lower()
    if "queryitemratedlist" in lowered:
        signal["service"] = "queryItemRatedList"
    elif "querydsrratedata" in lowered:
        signal["service"] = "queryDsrRateData"
    elif "offerdetail" in lowered or "offerwarnservice" in lowered:
        signal["service"] = "offerDetail"
    if "system_error" in lowered:
        signal["status"] = "system_error"
    elif '"success"' in lowered or '"ok"' in lowered or "resultcode" in lowered:
        signal["status"] = "ok_or_success"
    if "videoid" in lowered:
        signal["video_id_seen"] = True

    data = _loads(payload)
    if data is not None:
        for node in _walk(data):
            if signal["message"] is None:
                msg = node.get("message") or node.get("msg") or node.get("errorMessage")
                if msg:
                    signal["message"] = str(msg)
            if signal["review_count"] is None:
                for key in ("total", "totalCount", "rateCount", "count"):
                    value = node.get(key)
                    if isinstance(value, int):
                        signal["review_count"] = value
                        break
    return signal


def parse_review_snapshot(
    *,
    source_url: str,
    body_text: str = "",
    network_payloads: list[str] | None = None,
) -> dict[str, Any]:
    text = _as_text(body_text)
    summary_tags = _extract_summary_tags(text)
    review_texts = _extract_review_texts(text)
    empty_markers = [marker for marker in ["暂无有效评价", "未找到符合您筛选的记录"] if marker in text]
    signals = [_payload_signal(payload) for payload in network_payloads or [] if _as_text(payload)]
    warnings: list[str] = []
    if empty_markers and summary_tags:
        warnings.append("평가 태그는 보이지만 개별 리뷰 목록은 현재 필터/권한/동적 API 상태에서 비어 있습니다.")
    elif empty_markers:
        warnings.append("현재 화면에서 개별 리뷰 목록이 비어 있습니다.")
    if any(signal.get("status") == "system_error" for signal in signals):
        warnings.append("리뷰 목록 API 응답 중 system_error가 있어 Chrome 화면 기준 태그와 다른 네트워크 응답을 함께 확인해야 합니다.")

    status = "ok" if summary_tags or review_texts else "partial_data"
    review_list_status = "available" if review_texts else ("empty" if empty_markers else "unknown")
    return {
        "status": status,
        "provider": "chrome_devtools",
        "provider_version": "0.5.18",
        "source_type": "browser",
        "live_verified": True,
        "source_url": source_url,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "summary_tags": summary_tags,
        "review_texts": review_texts,
        "review_list_status": review_list_status,
        "empty_markers": empty_markers,
        "network_signals": signals,
        "warnings": warnings,
        "seller_notes": [
            "평가 태그는 상품 반응의 방향성 확인용으로 사용하세요.",
            "개별 리뷰 목록이 비어 있으면 옵션/필터를 바꾸거나 로그인 상태의 Chrome 네트워크 응답을 다시 캡처하세요.",
        ],
    }
