import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_root_codex_plugin_manifest_points_to_root_mcp_json():
    plugin = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    mcp = json.loads((ROOT / ".mcp.json").read_text(encoding="utf-8"))

    assert plugin["name"] == "sourcing-agent-1688"
    assert plugin["version"] == "0.5.0"
    assert plugin["skills"] == "./skills/"
    assert plugin["mcpServers"] == "./.mcp.json"
    assert "mcpServers" in mcp
    assert "mcp_servers" not in mcp
    assert mcp["mcpServers"]["sourcing1688"]["command"] == "uvx"
    assert "git+https://github.com/Squirbie/sourcing-agent-1688.git" in mcp["mcpServers"]["sourcing1688"]["args"]


def test_removed_marketplace_and_nested_plugin_layouts_are_absent():
    assert not (ROOT / ".agents").exists()
    assert not (ROOT / "plugins").exists()
    assert not (ROOT / ".mcp.codex.json").exists()
    assert not (ROOT / ".claude-plugin").exists()
