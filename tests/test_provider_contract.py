import pytest

from sourcing1688.providers.api_provider import Api1688Provider
from sourcing1688.providers.base import Base1688Provider
from sourcing1688.providers.browser_provider import Browser1688Provider
from sourcing1688.providers.mock_provider import Mock1688Provider


def test_mock_provider_implements_base_contract():
    provider = Mock1688Provider()

    assert isinstance(provider, Base1688Provider)


@pytest.mark.anyio
async def test_mock_provider_returns_fixture_search_and_detail():
    provider = Mock1688Provider()

    search = await provider.search_products("암막우산", page_size=1)
    detail = await provider.get_product_detail("123456789")
    hot = await provider.get_hot_keywords(limit=2)

    assert search.status == "ok"
    assert search.items[0].offer_id == "123456789"
    assert detail.status == "ok"
    assert detail.item.offer_id == "123456789"
    assert len(hot.items) == 2


@pytest.mark.anyio
async def test_api_provider_without_credentials_returns_missing_credentials(monkeypatch):
    monkeypatch.delenv("ALI1688_APP_KEY", raising=False)
    monkeypatch.delenv("ALI1688_APP_SECRET", raising=False)
    monkeypatch.delenv("ALI1688_REFRESH_TOKEN", raising=False)
    provider = Api1688Provider()

    result = await provider.search_products("黑胶伞")

    assert result.status == "missing_credentials"
    assert result.error is not None
    assert result.error.code == "missing_credentials"
    assert result.needs_human_action is False


@pytest.mark.anyio
async def test_browser_provider_without_profile_returns_needs_human_login(monkeypatch, tmp_path):
    monkeypatch.delenv("SOURCING1688_BROWSER_PROFILE", raising=False)
    monkeypatch.setenv("SOURCING1688_HOME", str(tmp_path / "missing-home"))
    provider = Browser1688Provider()

    result = await provider.search_products("黑胶伞")

    assert result.status == "needs_human_login"
    assert result.error is not None
    assert result.error.code == "needs_human_login"
    assert result.needs_human_action is True
