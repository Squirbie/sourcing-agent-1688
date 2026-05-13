from pathlib import Path

from sourcing1688.parsers.rendered_html import parse_rendered_html, parse_rendered_html_file


FIXTURES = Path(__file__).parent / "fixtures"


def test_rendered_html_parser_extracts_detail_assets_and_fields():
    result = parse_rendered_html_file(FIXTURES / "singlefile_detail_sample.html")

    assert result.status == "partial_data"
    detail = result.item
    assert detail.offer_id == "123456789"
    assert detail.title_zh
    assert "https://cbu01.alicdn.com/img/ibank/O1CN-main-1.jpg" in detail.main_image_urls
    assert "https://cbu01.alicdn.com/img/ibank/O1CN-detail-1.jpg" in detail.detail_image_urls
    assert "https://cbu01.alicdn.com/img/ibank/O1CN-option-black.jpg" in detail.option_image_urls
    assert detail.video_urls == ["https://cloud.video.taobao.com/play/u/1/p/1/e/6/t/1/123.mp4"]
    assert detail.main_image_urls.count("https://cbu01.alicdn.com/img/ibank/O1CN-main-1.jpg") == 1
    assert not any("lazyload" in url for url in detail.main_image_urls)
    assert detail.attributes


def test_existing_product_detail_fixture_is_parseable():
    result = parse_rendered_html_file(FIXTURES / "product_detail_sample.html")

    assert result.item.offer_id == "123456789"
    assert result.item.title_zh


def test_rendered_html_parser_accepts_source_url_for_chrome_captured_html():
    html = """
    <html>
      <head><title>Chrome captured product</title></head>
      <body>
        <h1>Chrome captured product</h1>
        <img src="//cbu01.alicdn.com/img/ibank/O1CN-chrome-main.jpg">
      </body>
    </html>
    """

    result = parse_rendered_html(html, source_url="https://detail.1688.com/offer/1018990720574.html")

    assert result.item.offer_id == "1018990720574"
    assert result.item.url == "https://detail.1688.com/offer/1018990720574.html"
    assert result.item.main_image_urls == ["https://cbu01.alicdn.com/img/ibank/O1CN-chrome-main.jpg"]


def test_rendered_html_parser_extracts_1688_model_trade_and_seller_fields():
    html = """
    <html>
      <head><title>Fallback title</title></head>
      <body>
        <script>
        window.__DATA__ = {
          "global": {
            "globalData": {
              "model": {
                "offerModel": {
                  "offerId": 1018990720574,
                  "subject": "宠物硅胶梳通用梳子",
                  "leafCategoryName": "宠物梳子"
                },
                "sellerModel": {
                  "companyName": "义乌市捷煜日用百货有限公司",
                  "sellerIdentity": "tp",
                  "winportUrl": "https://shop.example.1688.com",
                  "sellerSign": {"signs": {"isTp": true, "isFactoryDealer": false}}
                },
                "tradeModel": {
                  "beginAmount": 1,
                  "canBookedAmount": 35282,
                  "priceDisplay": "3.74",
                  "saleCount": 210,
                  "offerPriceModel": {
                    "currentPrices": [{"beginAmount": 1, "price": "3.74"}]
                  }
                },
                "skuModel": {
                  "skuProps": [
                    {
                      "prop": "颜色",
                      "value": [
                        {
                          "name": "粉色小号",
                          "imageUrl": "https://cbu01.alicdn.com/img/ibank/O1CN-option.jpg"
                        }
                      ]
                    }
                  ]
                }
              }
            }
          }
        };
        </script>
      </body>
    </html>
    """

    result = parse_rendered_html(html)
    detail = result.item

    assert detail.offer_id == "1018990720574"
    assert detail.title_zh == "宠物硅胶梳通用梳子"
    assert detail.category == "宠物梳子"
    assert detail.price_tiers[0].price == 3.74
    assert detail.price_tiers[0].min_quantity == 1
    assert detail.stock == 35282
    assert detail.trade_volume == 210
    assert detail.seller.name == "义乌市捷煜日用百货有限公司"
    assert detail.seller.url == "https://shop.example.1688.com"
    assert detail.sku_options[0].name == "颜色"
    assert detail.sku_options[0].values == ["粉色小号"]
    assert detail.option_image_urls == ["https://cbu01.alicdn.com/img/ibank/O1CN-option.jpg"]


def test_rendered_html_parser_warns_when_video_metadata_is_hidden():
    html = """
    <html>
      <body>
        <script>
        window.__DATA__ = {
          "offerModel": {"offerId": 775988776405, "subject": "宠物用品", "leafCategoryName": "宠物牵引绳"},
          "tradeModel": {"beginAmount": 1, "canBookedAmount": 10, "priceDisplay": "11.50", "saleCount": 1728},
          "sellerModel": {"companyName": "测试卖家"},
          "wirelessVideo": {"videoId": 0, "videoUrl": ""}
        };
        </script>
      </body>
    </html>
    """

    result = parse_rendered_html(html)

    assert result.item.video_urls == []
    assert result.warnings
    assert "no downloadable video url" in result.warnings[0].lower()
