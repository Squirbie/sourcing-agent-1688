import json

from typer.testing import CliRunner

from sourcing1688.cli import app


runner = CliRunner()


def parse_json_output(result):
    assert result.exit_code == 0, result.output
    return json.loads(result.output)


def test_cli_expand_keywords_json():
    result = runner.invoke(app, ["expand-keywords", "암막우산", "--json"])
    payload = parse_json_output(result)

    assert payload["status"] == "ok"
    assert "黑胶伞" in payload["keywords"]
    assert "\\u9ed1" not in result.output
    assert "암막우산" in result.output


def test_cli_search_json_with_mock_provider(monkeypatch):
    monkeypatch.setenv("SOURCING1688_PROVIDER", "mock")
    result = runner.invoke(app, ["search", "암막우산", "--top", "1", "--json"])
    payload = parse_json_output(result)

    assert payload["status"] == "ok"
    assert len(payload["items"]) == 1
    assert payload["items"][0]["offer_id"] == "123456789"


def test_cli_failure_is_valid_json():
    result = runner.invoke(app, ["analyze-url", "not-a-valid-offer", "--json"])
    payload = json.loads(result.output)

    assert result.exit_code != 0
    assert payload["status"] == "error"
    assert payload["error"]["code"] == "invalid_offer_id"


def test_cli_unknown_provider_json_failure_is_valid_json():
    result = runner.invoke(app, ["search", "암막우산", "--provider", "nope", "--json"])
    payload = json.loads(result.output)

    assert result.exit_code != 0
    assert payload["status"] == "error"
    assert payload["error"]["code"] == "unknown_provider"
