import json
from pathlib import Path

from typer.testing import CliRunner

from sourcing1688 import codex_install
from sourcing1688.cli import app


runner = CliRunner()


class Completed:
    def __init__(self, returncode=0, stdout="ok", stderr=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def write_marketplace_bundle(home: Path) -> None:
    plugin_dir = home / ".tmp" / "marketplaces" / codex_install.MARKETPLACE_NAME / "plugins" / codex_install.PLUGIN_NAME
    manifest_dir = plugin_dir / ".codex-plugin"
    manifest_dir.mkdir(parents=True)
    (manifest_dir / "plugin.json").write_text(json.dumps({"version": "0.5.16"}), encoding="utf-8")
    (plugin_dir / ".mcp.json").write_text(json.dumps({"mcpServers": {}}), encoding="utf-8")
    (plugin_dir / "README.md").write_text("# Plugin", encoding="utf-8")


def test_enable_and_disable_plugin_config(tmp_path):
    config = tmp_path / "config.toml"
    config.write_text("[features]\nhooks = true\n", encoding="utf-8")

    enabled = codex_install.enable_plugin_in_config(config)

    assert enabled["enabled"] is True
    assert f'[plugins."{codex_install.PLUGIN_CONFIG_ID}"]' in config.read_text(encoding="utf-8")
    assert "enabled = true" in config.read_text(encoding="utf-8")

    removed = codex_install.disable_plugin_in_config(config)

    assert removed["removed"] is True
    assert codex_install.PLUGIN_CONFIG_ID not in config.read_text(encoding="utf-8")


def test_install_codex_registers_marketplace_plugin_and_removes_global_mcp(monkeypatch, tmp_path):
    write_marketplace_bundle(tmp_path)
    commands = []

    def fake_which(name):
        return f"C:/bin/{name}.exe"

    def fake_run(command, **kwargs):
        commands.append(command)
        if command[:3] == ["codex", "mcp", "remove"]:
            return Completed(returncode=1, stderr="not found")
        return Completed()

    monkeypatch.setenv("CODEX_HOME", str(tmp_path))
    monkeypatch.setattr(codex_install.shutil, "which", fake_which)
    monkeypatch.setattr(codex_install.subprocess, "run", fake_run)

    payload = codex_install.install_codex(open_chrome_setup=False)

    assert payload["status"] == "ok"
    assert ["codex", "plugin", "marketplace", "add", codex_install.REPO_URL] in commands
    assert ["codex", "mcp", "remove", "sourcing1688"] in commands
    assert ["codex", "mcp", "remove", "chrome-devtools"] in commands
    assert not any(command[:3] == ["codex", "mcp", "add"] for command in commands)
    assert codex_install.PLUGIN_CONFIG_ID in (tmp_path / "config.toml").read_text(encoding="utf-8")
    assert (tmp_path / "plugins" / "cache" / codex_install.MARKETPLACE_NAME / codex_install.PLUGIN_NAME / "0.5.16").exists()


def test_install_codex_cli_json_can_be_mocked(monkeypatch, tmp_path):
    payload = {
        "status": "ok",
        "plugin_id": codex_install.PLUGIN_CONFIG_ID,
        "mcp_servers": "plugin-bundled",
    }

    monkeypatch.setattr("sourcing1688.cli.install_codex", lambda open_chrome_setup=True: payload)
    result = runner.invoke(app, ["install-codex", "--no-open-chrome-setup", "--json"])
    parsed = json.loads(result.output)

    assert result.exit_code == 0
    assert parsed["status"] == "ok"
    assert parsed["mcp_servers"] == "plugin-bundled"


def test_global_mcp_cleanup_removes_legacy_servers(monkeypatch):
    commands = []

    def fake_run(command, **kwargs):
        commands.append(command)
        return Completed()

    monkeypatch.setattr(codex_install.subprocess, "run", fake_run)

    codex_install._remove_global_mcp_servers()

    assert ["codex", "mcp", "remove", "sourcing1688"] in commands
    assert ["codex", "mcp", "remove", "chrome-devtools"] in commands
    assert not any(command[:3] == ["codex", "mcp", "add"] for command in commands)


def test_open_chrome_setup_page_skips_when_marker_exists(monkeypatch, tmp_path):
    monkeypatch.setenv("SOURCING1688_HOME", str(tmp_path))
    marker = codex_install.mark_chrome_setup_opened(tmp_path, command=["already-opened"])
    calls = []

    def fake_run(command, **kwargs):
        calls.append(command)
        return Completed()

    monkeypatch.setattr(codex_install.subprocess, "run", fake_run)

    payload = codex_install._open_chrome_setup_page()

    assert payload["ok"] is True
    assert payload["skipped"] is True
    assert payload["marker"]["path"] == marker["path"]
    assert calls == []


def test_uninstall_codex_cli_json_can_be_mocked(monkeypatch):
    monkeypatch.setattr("sourcing1688.cli.uninstall_codex", lambda remove_runtime=False: {"status": "ok", "remove_runtime": remove_runtime})

    result = runner.invoke(app, ["uninstall-codex", "--remove-runtime", "--json"])
    parsed = json.loads(result.output)

    assert result.exit_code == 0
    assert parsed["status"] == "ok"
    assert parsed["remove_runtime"] is True
