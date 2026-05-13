# 1688 Fields

- `offer_id`: stable 1688 offer id from URL or API `offerId`/ranking `itemId`.
- `title_zh`: Chinese product title, commonly `subject` or `title`.
- `subjectTrans` / `title_ko_optional`: translated title when API returns it.
- `image_url`: main image URL for search result cards.
- `price_min`, `price_max`: wholesale price range.
- `promotion_price`: API promotional price if present.
- `consign_price`: one-piece/drop-ship price if present.
- `minOrderQuantity` / `moq`: minimum order quantity.
- `monthSold` / `month_sold`: monthly sales signal.
- `tradeVolume` / `trade_volume`: transaction volume signal.
- `buyer_count`: ranking/API buyer count if present.
- `repurchaseRate` / `repurchase_rate`: repeat purchase rate, normalized to 0-1.
- `tradeScore` / `seller_score`: seller or composite service score.
- `seller_level`: medal/level such as trade medal level.
- `seller badges`: seller identities such as factory, `tp_member`, certified marks.
- `shipping time guarantee`: 24h/48h shipping badges.
- `isOnePsale`: one-piece dropship availability.
- `offerIdentities`: product badges such as `1688Selection`.
- `sellerIdentities`: seller badges.
- `missing_fields`: fields unavailable from this provider/run. Do not overstate quality when this list is long.

