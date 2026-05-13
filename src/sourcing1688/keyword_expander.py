from __future__ import annotations

import re

from sourcing1688.models import KeywordExpansion


KEYWORD_MAP: dict[str, list[str]] = {
    "\uc554\ub9c9\uc6b0\uc0b0": ["\u9ed1\u80f6\u4f1e", "\u9632\u6652\u4f1e", "\u906e\u9633\u4f1e", "\u6674\u96e8\u4f1e", "\u9632\u7d2b\u5916\u7ebf\u4f1e", "\u906e\u5149\u4f1e"],
    "\uc5ec\ud589\uc6a9 \ud30c\uc6b0\uce58": ["\u65c5\u884c\u6536\u7eb3\u888b", "\u65c5\u884c\u5316\u5986\u5305", "\u65c5\u6e38\u6d17\u6f31\u5305", "\u884c\u674e\u6536\u7eb3\u5305", "\u51fa\u5dee\u6536\u7eb3\u888b"],
    "\uc8fc\ubc29 \uc815\ub9ac\ud568": ["\u53a8\u623f\u6536\u7eb3\u76d2", "\u53a8\u623f\u7f6e\u7269\u67b6", "\u8c03\u6599\u6536\u7eb3\u76d2", "\u9910\u5177\u6536\u7eb3\u76d2", "\u53a8\u623f\u6536\u7eb3\u67b6"],
    "\ubc18\ub824\ub3d9\ubb3c \ube57": ["\u5ba0\u7269\u68b3\u5b50", "\u5ba0\u7269\u5237", "\u5ba0\u7269\u9664\u6bdb\u68b3", "\u732b\u72d7\u68b3\u5b50", "\u5ba0\u7269\u6309\u6469\u68b3"],
    "\ucc28\ub7c9\uc6a9 \ud587\ube5b\uac00\ub9ac\uac1c": ["\u6c7d\u8f66\u906e\u9633\u6321", "\u8f66\u7a97\u906e\u9633\u5e18", "\u6c7d\u8f66\u9632\u6652\u5e18", "\u524d\u6321\u906e\u9633\u677f", "\u8f66\u7528\u906e\u9633\u677f"],
    "\ud734\ub300\uc6a9 \uc120\ud48d\uae30": ["\u4fbf\u643a\u98ce\u6247", "\u624b\u6301\u5c0f\u98ce\u6247", "USB\u5c0f\u98ce\u6247", "\u8ff7\u4f60\u98ce\u6247", "\u6302\u8116\u98ce\u6247"],
    "\ubb34\ub4dc\ub4f1": ["\u6c1b\u56f4\u706f", "\u5c0f\u591c\u706f", "LED\u6c1b\u56f4\u706f", "\u5e8a\u5934\u706f", "\u88c5\u9970\u706f"],
    "\uc218\ub0a9\ubc15\uc2a4": ["\u6536\u7eb3\u7bb1", "\u6536\u7eb3\u76d2", "\u5851\u6599\u6536\u7eb3\u7bb1", "\u8863\u7269\u6536\u7eb3\u7bb1", "\u5bb6\u7528\u6536\u7eb3\u7bb1"],
    "\uc2e4\ub9ac\ucf58 \uc8fc\ubc29\uc6a9\ud488": ["\u7845\u80f6\u53a8\u5177", "\u7845\u80f6\u53a8\u623f\u7528\u54c1", "\u7845\u80f6\u9505\u94f2", "\u7845\u80f6\u70d8\u7119\u5de5\u5177", "\u7845\u80f6\u9910\u5177"],
    "\uc6d4\ub4dc\ucef5 \ucd95\uad6c \uc720\ub2c8\ud3fc": ["\u4e16\u754c\u676f\u7403\u8863", "\u8db3\u7403\u670d", "\u56fd\u5bb6\u961f\u7403\u8863", "2026\u4e16\u754c\u676f\u7403\u8863", "\u8db3\u7403\u8bad\u7ec3\u670d"],
    "\uc6b4\ub3d9 \uc591\ub9d0": ["\u8fd0\u52a8\u889c", "\u8dd1\u6b65\u889c", "\u6bdb\u5dfe\u5e95\u889c", "\u4e2d\u7b52\u8fd0\u52a8\u889c"],
    "\ub0a8\uc131 \ubca8\ud2b8": ["\u7537\u58eb\u76ae\u5e26", "\u81ea\u52a8\u6263\u76ae\u5e26", "\u8170\u5e26", "\u5546\u52a1\u76ae\u5e26"],
    "\ud06c\ub77c\ud504\ud2b8 \ud3ec\uc7a5\ubd09\ud22c": ["\u725b\u76ae\u7eb8\u888b", "\u5916\u5356\u5305\u88c5\u888b", "\u98df\u54c1\u5305\u88c5\u888b", "\u624b\u63d0\u725b\u76ae\u7eb8\u888b"],
    "\ub7ec\ub2dd\ud654": ["\u8dd1\u6b65\u978b", "\u8fd0\u52a8\u978b", "\u900f\u6c14\u8dd1\u978b", "\u4f11\u95f2\u8fd0\u52a8\u978b"],
    "\ub0a8\uc131 \uc18d\uc637": ["\u7537\u58eb\u5185\u88e4", "\u5e73\u89d2\u88e4", "\u7eaf\u68c9\u7537\u5185\u88e4", "\u7537\u58eb\u56db\u89d2\u88e4"],
    "\uc2a4\ub9c8\ud2b8\ud3f0 \uac70\uce58\ub300": ["\u624b\u673a\u652f\u67b6", "\u8f66\u8f7d\u624b\u673a\u652f\u67b6", "\u684c\u9762\u624b\u673a\u652f\u67b6", "\u61d2\u4eba\u624b\u673a\u652f\u67b6", "\u624b\u673a\u67b6"],
    "\ud734\ub300\ud3f0 \uac70\uce58\ub300": ["\u624b\u673a\u652f\u67b6", "\u8f66\u8f7d\u624b\u673a\u652f\u67b6", "\u684c\u9762\u624b\u673a\u652f\u67b6", "\u61d2\u4eba\u624b\u673a\u652f\u67b6", "\u624b\u673a\u67b6"],
}

COMPONENT_MAP: dict[str, list[str]] = {
    "\uc6d4\ub4dc\ucef5": ["\u4e16\u754c\u676f\u7403\u8863", "2026\u4e16\u754c\u676f\u7403\u8863"],
    "\ucd95\uad6c": ["\u8db3\u7403\u670d", "\u8db3\u7403\u8bad\u7ec3\u670d"],
    "\uc720\ub2c8\ud3fc": ["\u7403\u8863", "\u961f\u670d", "\u56fd\u5bb6\u961f\u7403\u8863"],
    "\uc591\ub9d0": ["\u8fd0\u52a8\u889c", "\u8dd1\u6b65\u889c"],
    "\ubca8\ud2b8": ["\u7537\u58eb\u76ae\u5e26", "\u8170\u5e26"],
    "\ud3ec\uc7a5": ["\u5305\u88c5\u888b", "\u98df\u54c1\u5305\u88c5\u888b"],
    "\ubd09\ud22c": ["\u725b\u76ae\u7eb8\u888b", "\u624b\u63d0\u725b\u76ae\u7eb8\u888b"],
    "\uc6b0\uc0b0": ["\u9632\u6652\u4f1e", "\u6674\u96e8\u4f1e"],
    "\ud30c\uc6b0\uce58": ["\u6536\u7eb3\u888b", "\u5316\u5986\u5305"],
    "\uc120\ud48d\uae30": ["\u4fbf\u643a\u98ce\u6247", "\u624b\u6301\u5c0f\u98ce\u6247"],
    "\uc18d\uc637": ["\u7537\u58eb\u5185\u88e4", "\u5e73\u89d2\u88e4"],
    "\uc2a4\ub9c8\ud2b8\ud3f0": ["\u624b\u673a\u652f\u67b6", "\u624b\u673a\u67b6"],
    "\ud734\ub300\ud3f0": ["\u624b\u673a\u652f\u67b6", "\u624b\u673a\u67b6"],
    "\uac70\uce58\ub300": ["\u624b\u673a\u652f\u67b6", "\u8f66\u8f7d\u624b\u673a\u652f\u67b6", "\u684c\u9762\u624b\u673a\u652f\u67b6"],
}


def _normalize(keyword: str) -> str:
    return " ".join(keyword.strip().split())


def _contains_chinese(value: str) -> bool:
    return bool(re.search(r"[\u4e00-\u9fff]", value))


def _dedupe(values: list[str]) -> list[str]:
    return list(dict.fromkeys(value for value in values if value))


def expand_keywords(keyword: str) -> KeywordExpansion:
    normalized = _normalize(keyword)
    if not normalized:
        return KeywordExpansion(
            status="partial_data",
            original_keyword=keyword,
            keywords=[],
            needs_review=True,
            note="Empty keyword. Provide a Korean or Chinese product keyword.",
        )

    if normalized in KEYWORD_MAP:
        return KeywordExpansion(original_keyword=normalized, keywords=KEYWORD_MAP[normalized])

    if _contains_chinese(normalized):
        return KeywordExpansion(
            status="ok",
            original_keyword=normalized,
            keywords=[normalized],
            source_language="zh",
            target_language="zh",
        )

    expanded: list[str] = []
    compact = normalized.replace(" ", "")
    for korean_term, chinese_terms in COMPONENT_MAP.items():
        if korean_term in normalized or korean_term.replace(" ", "") in compact:
            expanded.extend(chinese_terms)

    deduped = _dedupe(expanded)
    if deduped:
        return KeywordExpansion(
            status="partial_data",
            original_keyword=normalized,
            keywords=deduped,
            needs_review=True,
            note="Built from curated component terms. Review before live sourcing.",
        )

    return KeywordExpansion(
        status="partial_data",
        original_keyword=normalized,
        keywords=[normalized],
        needs_review=True,
        note="No curated Chinese sourcing mapping exists yet. Provide a Chinese keyword or open a 1688 page in Chrome for analysis.",
    )
