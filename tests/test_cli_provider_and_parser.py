import json
from pathlib import Path

from typer.testing import CliRunner

from sourcing1688.cli import app


runner = CliRunner()
FIXTURES = Path(__file__).parent / "fixtures"


def test_providers_cli_json_lists_capabilities():
    result = runner.invoke(app, ["providers", "--json"])
    payload = json.loads(result.output)

    assert result.exit_code == 0
    assert payload["status"] == "ok"
    assert {"mock", "api", "browser", "local_html"}.issubset(payload["providers"])


def test_provider_check_mock_json():
    result = runner.invoke(app, ["provider-check", "--provider", "mock", "--json"])
    payload = json.loads(result.output)

    assert result.exit_code == 0
    assert payload["status"] == "ok"
    assert payload["provider"] == "mock"
    assert payload["ready"] is True
    assert payload["live_verified"] is False
    assert payload["capabilities"]["search"] is True


def test_parse_html_cli_json():
    result = runner.invoke(app, ["parse-html", str(FIXTURES / "singlefile_detail_sample.html"), "--json"])
    payload = json.loads(result.output)

    assert result.exit_code == 0
    assert payload["status"] == "partial_data"
    assert payload["item"]["offer_id"] == "123456789"


def test_download_assets_from_html_cli_json(tmp_path, monkeypatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("dry-run must not attempt network downloads")

    monkeypatch.setattr("sourcing1688.assets.downloader._download_url", fail_if_called)
    result = runner.invoke(
        app,
        ["download-assets-from-html", str(FIXTURES / "singlefile_detail_sample.html"), "--out", str(tmp_path), "--dry-run", "--json"],
    )
    payload = json.loads(result.output)

    assert result.exit_code == 0
    assert payload["status"] == "dry_run"
    assert payload["manifest_path"]
    assert payload["manifest"]["dry_run_assets"]


def test_download_assets_from_html_default_out_uses_home_assets(tmp_path, monkeypatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("dry-run must not attempt network downloads")

    monkeypatch.setattr("sourcing1688.assets.downloader._download_url", fail_if_called)
    result = runner.invoke(
        app,
        ["download-assets-from-html", str(FIXTURES / "singlefile_detail_sample.html"), "--dry-run", "--json"],
        env={"SOURCING1688_HOME": str(tmp_path)},
    )
    payload = json.loads(result.output)

    assert result.exit_code == 0
    assert payload["status"] == "dry_run"
    assert Path(payload["manifest"]["saved_dir"]).is_relative_to(tmp_path / "assets")


def test_download_assets_cli_dry_run_json(tmp_path, monkeypatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("dry-run must not attempt network downloads")

    monkeypatch.setattr("sourcing1688.assets.downloader._download_url", fail_if_called)
    result = runner.invoke(
        app,
        ["download-assets", "123456789", "--provider", "mock", "--out", str(tmp_path), "--dry-run", "--json"],
    )
    payload = json.loads(result.output)

    assert result.exit_code == 0
    assert payload["status"] == "dry_run"
    assert payload["manifest"]["dry_run_assets"]


def test_download_assets_default_out_uses_home_assets(tmp_path, monkeypatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("dry-run must not attempt network downloads")

    monkeypatch.setattr("sourcing1688.assets.downloader._download_url", fail_if_called)
    result = runner.invoke(
        app,
        ["download-assets", "123456789", "--provider", "mock", "--dry-run", "--json"],
        env={"SOURCING1688_HOME": str(tmp_path)},
    )
    payload = json.loads(result.output)

    assert result.exit_code == 0
    assert payload["status"] == "dry_run"
    assert Path(payload["manifest"]["saved_dir"]).is_relative_to(tmp_path / "assets")


def test_image_search_mock_cli_json():
    result = runner.invoke(app, ["image-search", "--image-url", "https://cbu01.alicdn.com/img/ibank/O1CN.jpg", "--provider", "mock", "--json"])
    payload = json.loads(result.output)

    assert result.exit_code == 0
    assert payload["status"] == "ok"
    assert payload["items"][0]["offer_id"] == "222333444"
