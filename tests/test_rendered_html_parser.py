from pathlib import Path

from sourcing1688.parsers.rendered_html import parse_rendered_html, parse_rendered_html_file, parse_visible_page_snapshot


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


def test_rendered_html_parser_uses_visible_1688_text_when_json_is_sparse():
    html = """
    <html>
      <head>
        <title>杜老汉兔子趴趴垫保暖冬天兔子垫子夹夹垫侏儒垂耳兔荷兰猪兔子窝</title>
      </head>
      <body>
        <script>window.__DATA__ = {"offerModel": {"offerId": 856551681324}};</script>
        <div>杜老汉（山东）生物科技有限公司</div>
        <h1>杜老汉兔子趴趴垫保暖冬天兔子垫子夹夹垫侏儒垂耳兔荷兰猪兔子窝</h1>
        <div>一年内</div>
        <div>100+</div>
        <div>个成交</div>
        <div>价格</div>
        <div>¥</div>
        <div>25.00</div>
        <div>~</div>
        <div>¥</div>
        <div>39.00</div>
        <div>1个起批</div>
        <div>商品属性</div>
        <div>材质</div>
        <div>布类</div>
        <div>品牌</div>
        <div>杜老汉</div>
        <div>是否跨境出口专供货源</div>
        <div>是</div>
        <div>商品描述</div>
        <script>
          window.assetHints = [
            "https://cbu01.alicdn.com/img/ibank/O1CN01rejsj61Bs2sgIAIpZ_!!0-0-cib.jpg",
            "https://cbu01.alicdn.com/img/ibank/O1CN01ORwIZS1s7oW8LiPmR_!!2216180205720-0-cib.jpg",
            "https://cloud.video.taobao.com/play/u/2216180205720/p/2/e/6/t/1/494830060237.mp4"
          ];
        </script>
      </body>
    </html>
    """

    result = parse_rendered_html(html, source_url="https://detail.1688.com/offer/856551681324.html")
    detail = result.item

    assert detail.offer_id == "856551681324"
    assert detail.price_tiers[0].min_quantity == 1
    assert detail.price_tiers[0].price == 25.0
    assert detail.trade_volume == 100
    assert detail.seller.name == "杜老汉（山东）生物科技有限公司"
    assert detail.attributes["材质"] == "布类"
    assert detail.attributes["品牌"] == "杜老汉"
    assert detail.main_image_urls
    assert detail.video_urls == ["https://cloud.video.taobao.com/play/u/2216180205720/p/2/e/6/t/1/494830060237.mp4"]


def test_visible_page_snapshot_parser_keeps_live_dom_fields_compactly():
    body_text = "\n".join(
        [
            "杜老汉（山东）生物科技有限公司",
            "杜老汉兔子趴趴垫保暖冬天兔子垫子夹夹垫侏儒垂耳兔荷兰猪兔子窝",
            "一年内",
            "100+",
            "个成交",
            "价格",
            "¥",
            "25.00",
            "~",
            "¥",
            "39.00",
            "1个起批",
            "商品属性",
            "材质",
            "布类",
            "品牌",
            "杜老汉",
            "商品描述",
        ]
    )

    result = parse_visible_page_snapshot(
        source_url="https://detail.1688.com/offer/856551681324.html",
        title="杜老汉兔子趴趴垫保暖冬天兔子垫子夹夹垫侏儒垂耳兔荷兰猪兔子窝",
        body_text=body_text,
        media_urls=[
            "https://cbu01.alicdn.com/img/ibank/O1CN01rejsj61Bs2sgIAIpZ_!!0-0-cib.jpg",
            "https://cloud.video.taobao.com/play/u/2216180205720/p/2/e/6/t/1/494830060237.mp4",
        ],
    )
    detail = result.item

    assert result.provider == "chrome_devtools"
    assert detail.source_type == "browser"
    assert detail.price_tiers[0].price == 25.0
    assert detail.trade_volume == 100
    assert detail.seller.name == "杜老汉（山东）生物科技有限公司"
    assert detail.main_image_urls == ["https://cbu01.alicdn.com/img/ibank/O1CN01rejsj61Bs2sgIAIpZ_!!0-0-cib.jpg"]
    assert detail.video_urls == ["https://cloud.video.taobao.com/play/u/2216180205720/p/2/e/6/t/1/494830060237.mp4"]


def test_rendered_html_parser_merges_extra_json_seller_and_images():
    html = """
    <html>
      <body>
        <script>
        window.__DATA__ = {
          "offerId": "888888888",
          "subject": "测试商品",
          "priceInfo": {"price": "19.90", "beginAmount": 2},
          "sellerDataInfo": {"companyName": "测试源头工厂", "compositeServiceScore": "4.7"},
          "imageList": [{"imageUrl": "https://cbu01.alicdn.com/img/ibank/O1CN-json-main.jpg"}]
        };
        </script>
      </body>
    </html>
    """

    detail = parse_rendered_html(html).item

    assert detail.price_tiers[0].min_quantity == 2
    assert detail.price_tiers[0].price == 19.9
    assert detail.seller.name == "测试源头工厂"
    assert detail.seller.score == 4.7
    assert detail.main_image_urls == ["https://cbu01.alicdn.com/img/ibank/O1CN-json-main.jpg"]
