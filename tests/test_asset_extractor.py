from bs4 import BeautifulSoup

from sourcing1688.parsers.asset_extractor import extract_assets, extract_urls_from_text, normalize_url


def test_extract_urls_skips_xpath_like_invalid_url_candidates():
    text = """
    const bad = "https://*[@id=";
    const image = "https://cbu01.alicdn.com/img/ibank/O1CN-valid.jpg";
    const video = "https://cloud.video.taobao.com/play/u/1/p/1/e/6/t/1/valid.mp4";
    """

    images, videos = extract_urls_from_text(text)

    assert images == ["https://cbu01.alicdn.com/img/ibank/O1CN-valid.jpg"]
    assert videos == ["https://cloud.video.taobao.com/play/u/1/p/1/e/6/t/1/valid.mp4"]


def test_normalize_url_rejects_malformed_netloc_without_raising():
    assert normalize_url("https://*[@id=") is None
    assert normalize_url("https://[bad") is None


def test_extract_assets_does_not_crash_on_malformed_script_url():
    html = """
    <html>
      <body>
        <img src="//cbu01.alicdn.com/img/ibank/O1CN-main.jpg">
        <script>
          window.xpath = "https://*[@id=";
          window.video = "https://cloud.video.taobao.com/play/u/1/p/1/e/6/t/1/valid.mp4";
        </script>
      </body>
    </html>
    """

    assets = extract_assets(BeautifulSoup(html, "html.parser"), html)

    assert assets["main_images"] == ["https://cbu01.alicdn.com/img/ibank/O1CN-main.jpg"]
    assert assets["videos"] == ["https://cloud.video.taobao.com/play/u/1/p/1/e/6/t/1/valid.mp4"]
