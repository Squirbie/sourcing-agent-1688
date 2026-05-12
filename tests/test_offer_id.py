import pytest

from sourcing1688.utils import extract_offer_id


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
