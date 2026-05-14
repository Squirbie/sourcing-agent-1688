import pytest

from sourcing1688.utils import encode_1688_search_keyword, extract_offer_id


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("https://detail.1688.com/offer/123456789.html", "123456789"),
        ("http://detail.1688.com/offer/123456789.html", "123456789"),
        ("detail.1688.com/offer/123456789.html", "123456789"),
        ("123456789", "123456789"),
        ("https://m.1688.com/offer/123456789.html?spm=a2615", "123456789"),
    ],
)
def test_extract_offer_id(value, expected):
    assert extract_offer_id(value) == expected


def test_extract_offer_id_rejects_invalid_input():
    with pytest.raises(ValueError):
        extract_offer_id("https://example.com/no-offer")


def test_encode_1688_search_keyword_uses_gbk_for_chinese_search_page():
    assert encode_1688_search_keyword("\u624b\u673a\u652f\u67b6") == "%CA%D6%BB%FA%D6%A7%BC%DC"
