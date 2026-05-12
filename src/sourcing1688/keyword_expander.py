from __future__ import annotations

from sourcing1688.models import KeywordExpansion


KEYWORD_MAP: dict[str, list[str]] = {
    "암막우산": ["黑胶伞", "防晒伞", "遮阳伞", "晴雨伞", "防紫外线伞", "遮光伞"],
    "여행용 파우치": ["旅行收纳袋", "旅游收纳包", "行李箱收纳袋", "旅行分装袋", "便携收纳包"],
    "주방 정리함": ["厨房收纳盒", "厨房置物架", "厨房整理箱", "调料收纳盒", "橱柜收纳盒"],
    "반려동물 빗": ["宠物梳子", "猫狗梳毛器", "宠物针梳", "宠物去毛梳", "宠物美容梳"],
    "차량용 햇빛가리개": ["汽车遮阳挡", "车载遮阳帘", "汽车防晒挡", "车窗遮阳帘", "汽车隔热遮阳挡"],
    "휴대용 선풍기": ["便携风扇", "手持小风扇", "迷你风扇", "挂脖风扇", "USB小风扇"],
    "무드등": ["氛围灯", "小夜灯", "LED氛围灯", "床头灯", "创意夜灯"],
    "수납박스": ["收纳箱", "收纳盒", "塑料收纳箱", "折叠收纳箱", "衣物收纳箱"],
    "실리콘 주방용품": ["硅胶厨具", "硅胶厨房用品", "硅胶锅铲", "硅胶餐具", "硅胶烘焙工具"],
}


SYNONYMS: dict[str, list[str]] = {
    "우산": ["伞", "雨伞", "晴雨伞"],
    "파우치": ["收纳袋", "收纳包"],
    "정리함": ["收纳盒", "收纳箱"],
    "선풍기": ["风扇", "小风扇"],
    "무드등": ["氛围灯", "小夜灯"],
}


def expand_keywords(keyword: str) -> KeywordExpansion:
    normalized = " ".join(keyword.strip().split())
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

    expanded: list[str] = [normalized]
    for korean_term, chinese_terms in SYNONYMS.items():
        if korean_term in normalized:
            expanded.extend(chinese_terms)

    placeholder = f"{normalized} 中文关键词候选"
    expanded.append(placeholder)
    deduped = list(dict.fromkeys(expanded))
    return KeywordExpansion(
        status="partial_data",
        original_keyword=normalized,
        keywords=deduped,
        needs_review=True,
        note="No curated mapping exists yet. Review the placeholder Chinese sourcing keyword before live sourcing.",
    )

