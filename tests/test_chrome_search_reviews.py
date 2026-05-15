from sourcing1688.parsers.reviews import parse_review_snapshot
from sourcing1688.parsers.search_results import parse_search_results_snapshot


def test_search_results_snapshot_normalizes_candidates_and_krw():
    items = [
        {
            "title": f"旅行收纳袋六件套旅游用品衣物整理包{index}",
            "url": f"https://detail.1688.com/offer/{800000000000 + index}.html",
            "price_text": f"¥{5 + index}.8",
            "sold_text": "已售1.2万件",
            "seller_name": f"义乌旅行用品工厂{index}",
            "image_url": "https://cbu01.alicdn.com/img/ibank/test.jpg",
            "raw_text": "源头工厂 48小时发货 回头率59% 已售1.2万件",
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
    assert payload["items"][0]["title_ko_summary"] == "여행/수납 관련 후보"
    assert payload["items"][0]["price_krw_min"] == 1102
    assert payload["items"][0]["sold_count"] == 12000
    assert payload["items"][0]["repurchase_rate"] == 0.59
    assert "源头工厂" in payload["items"][0]["badges"]
    assert "48小时发货" in payload["items"][0]["badges"]
    assert payload["warnings"] == []


def test_search_results_snapshot_canonicalizes_mobile_offer_id_links():
    payload = parse_search_results_snapshot(
        keyword="旅行用品",
        source_url="https://s.1688.com/selloffer/offer_search.htm",
        items=[
            {
                "title": "旅行收纳袋可折叠",
                "url": "http://detail.m.1688.com/page/index.html?offerId=787690257525&skuId=123",
                "price_text": "¥6.2",
                "raw_text": "回头率70%",
            }
        ],
        cny_krw_rate=190,
        min_items=1,
    )

    assert payload["items"][0]["offer_id"] == "787690257525"
    assert payload["items"][0]["url"] == "https://detail.1688.com/offer/787690257525.html"
    assert payload["items"][0]["raw_url"].startswith("http://detail.m.1688.com")
    assert payload["items"][0]["repurchase_rate"] == 0.7


def test_search_results_snapshot_warns_when_fewer_than_minimum():
    payload = parse_search_results_snapshot(
        keyword="旅行用品",
        source_url="https://s.1688.com/selloffer/offer_search.htm",
        items=[{"title": "旅行收纳袋", "url": "https://detail.1688.com/offer/800000000001.html", "price_text": "¥2.5"}],
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
                "采购商评价",
                "质量很好 51",
                "包装严实 45",
                "发货很快 32",
                "做工不错 29",
                "综合评价",
                "5.0",
                "100+条评价",
                "好评率100%",
                "有内容9",
                "暂无更多评价",
            ]
        ),
        network_payloads=['{"resultCode":"SUCCESS","data":{"totalCount":0}}', '{"error":"SYSTEM_ERROR::null"}'],
    )

    assert payload["status"] == "ok"
    assert payload["review_list_status"] == "empty"
    assert payload["review_summary"]["score"] == 5.0
    assert payload["review_summary"]["review_count_text"] == "100+"
    assert payload["review_summary"]["positive_rate"] == 1.0
    assert payload["review_summary"]["content_review_count_text"] == "9"
    assert payload["summary_tags"][0] == {"label_zh": "质量很好", "count": 51}
    assert any(signal["status"] == "system_error" for signal in payload["network_signals"])
    assert payload["warnings"]
