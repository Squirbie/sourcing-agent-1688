import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_codex_mcp_json_uses_codex_mcp_servers_key():
    payload = json.loads((ROOT / ".mcp.codex.json").read_text(encoding="utf-8"))

    assert "mcp_servers" in payload
    assert "mcpServers" not in payload
    assert payload["mcp_servers"]["sourcing1688"]["command"] == "uv"
    assert payload["mcp_servers"]["sourcing1688"]["env"]["SOURCING1688_PROVIDER"] == "auto"


def test_standard_mcp_json_uses_mcp_servers_key():
    payload = json.loads((ROOT / ".mcp.json").read_text(encoding="utf-8"))

    assert "mcpServers" in payload
    assert "mcp_servers" not in payload
    assert payload["mcpServers"]["sourcing1688"]["command"] == "uv"


def test_plugin_manifest_points_to_codex_mcp_json():
    payload = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))

    assert payload["name"] == "sourcing-agent-1688"
    assert payload["mcpServers"] == "./.mcp.codex.json"
