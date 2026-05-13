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


def test_bundled_codex_plugin_layout_is_explicit():
    marketplace = json.loads((ROOT / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8"))
    bundle_root = ROOT / "plugins" / "sourcing-agent-1688"
    plugin = json.loads((bundle_root / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    mcp = json.loads((bundle_root / ".mcp.codex.json").read_text(encoding="utf-8"))

    assert marketplace["plugins"][0]["source"] == {
        "source": "local",
        "path": "./plugins/sourcing-agent-1688",
    }
    assert marketplace["plugins"][0]["policy"]["installation"] == "INSTALLED_BY_DEFAULT"
    assert marketplace["plugins"][0]["policy"]["authentication"] == "ON_INSTALL"
    assert plugin["name"] == "sourcing-agent-1688"
    assert plugin["mcpServers"] == "./.mcp.codex.json"
    assert mcp["mcp_servers"]["sourcing1688"]["command"] == "uvx"
    assert "git+https://github.com/Squirbie/sourcing-agent-1688.git" in mcp["mcp_servers"]["sourcing1688"]["args"]
