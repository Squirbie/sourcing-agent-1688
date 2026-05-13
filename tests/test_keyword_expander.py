from sourcing1688.keyword_expander import expand_keywords


def test_expands_korean_blackout_umbrella_to_chinese_sourcing_terms():
    result = expand_keywords("\uc554\ub9c9\uc6b0\uc0b0")

    assert result.status == "ok"
    assert "\u9ed1\u80f6\u4f1e" in result.keywords
    assert "\u9632\u6652\u4f1e" in result.keywords
    assert result.needs_review is False


def test_expands_requested_commerce_terms_without_placeholder():
    examples = {
        "\uc6d4\ub4dc\ucef5 \ucd95\uad6c \uc720\ub2c8\ud3fc": ["\u4e16\u754c\u676f\u7403\u8863", "\u8db3\u7403\u670d", "\u56fd\u5bb6\u961f\u7403\u8863", "2026\u4e16\u754c\u676f\u7403\u8863", "\u8db3\u7403\u8bad\u7ec3\u670d"],
        "\uc6b4\ub3d9 \uc591\ub9d0": ["\u8fd0\u52a8\u889c", "\u8dd1\u6b65\u889c", "\u6bdb\u5dfe\u5e95\u889c", "\u4e2d\u7b52\u8fd0\u52a8\u889c"],
        "\ub0a8\uc131 \ubca8\ud2b8": ["\u7537\u58eb\u76ae\u5e26", "\u81ea\u52a8\u6263\u76ae\u5e26", "\u8170\u5e26", "\u5546\u52a1\u76ae\u5e26"],
        "\ud06c\ub77c\ud504\ud2b8 \ud3ec\uc7a5\ubd09\ud22c": ["\u725b\u76ae\u7eb8\u888b", "\u5916\u5356\u5305\u88c5\u888b", "\u98df\u54c1\u5305\u88c5\u888b", "\u624b\u63d0\u725b\u76ae\u7eb8\u888b"],
        "\ub7ec\ub2dd\ud654": ["\u8dd1\u6b65\u978b", "\u8fd0\u52a8\u978b", "\u900f\u6c14\u8dd1\u978b", "\u4f11\u95f2\u8fd0\u52a8\u978b"],
        "\ub0a8\uc131 \uc18d\uc637": ["\u7537\u58eb\u5185\u88e4", "\u5e73\u89d2\u88e4", "\u7eaf\u68c9\u7537\u5185\u88e4", "\u7537\u58eb\u56db\u89d2\u88e4"],
    }

    for keyword, expected in examples.items():
        result = expand_keywords(keyword)
        assert result.status == "ok"
        assert result.keywords == expected
        assert not any("\u4e2d\u6587\u5173\u952e\u8bcd\u5019\u9009" in item for item in result.keywords)


def test_unknown_keyword_returns_original_without_fake_chinese_placeholder():
    result = expand_keywords("\uc0c8\ub85c\uc6b4\ud14c\uc2a4\ud2b8\uc0c1\ud488")

    assert result.status == "partial_data"
    assert result.original_keyword == "\uc0c8\ub85c\uc6b4\ud14c\uc2a4\ud2b8\uc0c1\ud488"
    assert result.keywords == ["\uc0c8\ub85c\uc6b4\ud14c\uc2a4\ud2b8\uc0c1\ud488"]
    assert result.needs_review is True
    assert "\u4e2d\u6587\u5173\u952e\u8bcd\u5019\u9009" not in " ".join(result.keywords)
    assert result.note
