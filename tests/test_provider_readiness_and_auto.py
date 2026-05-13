import json

from typer.testing import CliRunner

from sourcing1688.cli import app


runner = CliRunner()


def test_provider_check_api_without_credentials_is_not_ready(monkeypatch):
    for key in ["ALI1688_APP_KEY", "ALI1688_APP_SECRET", "ALI1688_REFRESH_TOKEN", "ALI1688_ACCESS_TOKEN"]:
        monkeypatch.delenv(key, raising=False)

    result = runner.invoke(app, ["provider-check", "--provider", "api", "--json"])
    payload = json.loads(result.output)

    assert result.exit_code == 0
    assert payload["status"] == "missing_credentials"
    assert payload["ready"] is False
    assert payload["error"]["code"] == "missing_credentials"
    assert "ALI1688_APP_KEY" in payload["missing_env"]


def test_provider_check_browser_without_profile_is_not_ready(monkeypatch, tmp_path):
    monkeypatch.delenv("SOURCING1688_BROWSER_PROFILE", raising=False)
    monkeypatch.setenv("SOURCING1688_HOME", str(tmp_path / "missing-home"))

    result = runner.invoke(app, ["provider-check", "--provider", "browser", "--json"])
    payload = json.loads(result.output)

    assert result.exit_code == 0
    assert payload["status"] == "needs_human_login"
    assert payload["ready"] is False
    assert payload["error"]["code"] == "needs_human_login"


def test_auto_provider_without_live_access_does_not_launch_browser(monkeypatch, tmp_path):
    for key in ["ALI1688_APP_KEY", "ALI1688_APP_SECRET", "ALI1688_REFRESH_TOKEN", "ALI1688_ACCESS_TOKEN", "SOURCING1688_BROWSER_PROFILE"]:
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setenv("SOURCING1688_HOME", str(tmp_path / "missing-home"))

    result = runner.invoke(app, ["search", "黑胶伞", "--provider", "auto", "--top", "2", "--json"])
    payload = json.loads(result.output)

    assert result.exit_code == 0
    assert payload["status"] == "provider_unavailable"
    assert payload["error"]["code"] == "missing_live_provider"
    assert payload["provider"] == "auto"
    assert payload["items"] == []


def test_auto_provider_routes_missing_credentials_to_chrome_or_explicit_setup(monkeypatch, tmp_path):
    for key in ["ALI1688_APP_KEY", "ALI1688_APP_SECRET", "ALI1688_REFRESH_TOKEN", "ALI1688_ACCESS_TOKEN", "SOURCING1688_BROWSER_PROFILE"]:
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setenv("SOURCING1688_HOME", str(tmp_path / "missing-home"))

    result = runner.invoke(app, ["provider-check", "--provider", "auto", "--json"])
    payload = json.loads(result.output)

    assert result.exit_code == 0
    assert payload["status"] == "provider_unavailable"
    assert payload["selected_provider"] is None
    assert payload["ready"] is False
    assert payload["error"]["code"] == "missing_live_provider"
    assert "Chrome DevTools" in payload["suggested_action"]
