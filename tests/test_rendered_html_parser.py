from pathlib import Path

from sourcing1688.parsers.rendered_html import parse_rendered_html_file


FIXTURES = Path(__file__).parent / "fixtures"


def test_rendered_html_parser_extracts_detail_assets_and_fields():
    result = parse_rendered_html_file(FIXTURES / "singlefile_detail_sample.html")

    assert result.status == "partial_data"
    detail = result.item
    assert detail.offer_id == "123456789"
    assert detail.title_zh == "黑胶防晒晴雨伞 三折遮阳伞"
    assert "https://cbu01.alicdn.com/img/ibank/O1CN-main-1.jpg" in detail.main_image_urls
    assert "https://cbu01.alicdn.com/img/ibank/O1CN-detail-1.jpg" in detail.detail_image_urls
    assert "https://cbu01.alicdn.com/img/ibank/O1CN-option-black.jpg" in detail.option_image_urls
    assert detail.video_urls == ["https://cloud.video.taobao.com/play/u/1/p/1/e/6/t/1/123.mp4"]
    assert detail.main_image_urls.count("https://cbu01.alicdn.com/img/ibank/O1CN-main-1.jpg") == 1
    assert not any("lazyload" in url for url in detail.main_image_urls)
    assert detail.attributes["材质"] == "碰击布"


def test_existing_product_detail_fixture_is_parseable():
    result = parse_rendered_html_file(FIXTURES / "product_detail_sample.html")

    assert result.item.offer_id == "123456789"
    assert result.item.title_zh == "黑胶防晒晴雨伞 三折遮阳伞"
