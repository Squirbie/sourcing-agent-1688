from sourcing1688.parsers.reviews import parse_review_snapshot
from sourcing1688.parsers.search_results import parse_search_results_snapshot


def test_search_results_snapshot_normalizes_candidates_and_krw():
    items = [
        {
            "title": "旅行收纳袋 出差行李整理包",
            "url": f"https://detail.1688.com/offer/{800000000000 + index}.html",
            "price_text": f"¥{5 + index}.8",
            "sold_text": "已售1.2万+件",
            "seller_name": f"义乌旅行用品工厂{index}",
            "image_url": "https://cbu01.alicdn.com/img/ibank/test.jpg",
        }
        for index in range(10)
    ]

    payload = parse_search_results_snapshot(
        keyword="旅行用品",
        source_url="https://s.1688.com/selloffer/offer_search.htm?keywords=%C2%C3%D0%D0%D3%C3%C6%B7",
        items=items,
        cny_krw_rate=190,
        min_items=10,
    )

    assert payload["status"] == "ok"
    assert payload["count"] == 10
    assert payload["items"][0]["title_ko_summary"] == "여행용 수납/휴대 편의용품"
    assert payload["items"][0]["price_krw_min"] == 1102
    assert payload["items"][0]["sold_count"] == 12000
    assert payload["warnings"] == []


def test_search_results_snapshot_warns_when_fewer_than_minimum():
    payload = parse_search_results_snapshot(
        keyword="旅行用品",
        source_url="https://s.1688.com/selloffer/offer_search.htm",
        items=[{"title": "旅行分装瓶", "url": "https://detail.1688.com/offer/800000000001.html", "price_text": "¥2.5"}],
        cny_krw_rate=200,
        min_items=10,
    )

    assert payload["count"] == 1
    assert payload["warnings"]


def test_review_snapshot_extracts_tags_and_empty_review_state():
    payload = parse_review_snapshot(
        source_url="https://detail.1688.com/offer/755178864684.html",
        body_text="\n".join(
            [
                "买家评价",
                "价格很实惠 51",
                "质量不错 45",
                "性价比超高 32",
                "发货快 29",
                "暂无有效评价",
            ]
        ),
        network_payloads=['{"resultCode":"SUCCESS","data":{"totalCount":0}}', '{"error":"SYSTEM_ERROR::null"}'],
    )

    assert payload["status"] == "ok"
    assert payload["review_list_status"] == "empty"
    assert payload["summary_tags"][0] == {"label_zh": "价格很实惠", "count": 51}
    assert any(signal["status"] == "system_error" for signal in payload["network_signals"])
    assert payload["warnings"]
