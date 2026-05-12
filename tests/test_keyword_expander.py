from sourcing1688.keyword_expander import expand_keywords


def test_expands_korean_blackout_umbrella_to_chinese_sourcing_terms():
    result = expand_keywords("암막우산")

    assert result.status == "ok"
    assert "黑胶伞" in result.keywords
    assert "防晒伞" in result.keywords
    assert result.needs_review is False


def test_unknown_keyword_returns_reviewable_placeholder():
    result = expand_keywords("새로운테스트상품")

    assert result.status == "partial_data"
    assert result.original_keyword == "새로운테스트상품"
    assert "새로운테스트상품" in result.keywords
    assert result.needs_review is True
    assert result.note
