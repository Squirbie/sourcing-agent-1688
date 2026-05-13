from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO_URL = "https://github.com/Squirbie/sourcing-agent-1688.git"
GIT_REPO_URL = f"git+{REPO_URL}"
MARKETPLACE_NAME = "sourcing-agent-1688-marketplace"
PLUGIN_NAME = "sourcing-agent-1688"
PLUGIN_CONFIG_ID = f'{PLUGIN_NAME}@{MARKETPLACE_NAME}'
SOURCING_MCP_NAME = "sourcing1688"
CHROME_MCP_NAME = "chrome-devtools"


def codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")


def sourcing_home() -> Path:
    return Path(os.environ.get("SOURCING1688_HOME") or Path.home() / ".sourcing1688")


def _run(command: list[str], *, check: bool = False) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except FileNotFoundError:
        return {
            "command": command,
            "returncode": 127,
            "ok": False,
            "stdout": "",
            "stderr": f"Command not found: {command[0]}",
        }
    result = {
        "command": command,
        "returncode": completed.returncode,
        "ok": completed.returncode == 0,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
    }
    if check and completed.returncode != 0:
        raise RuntimeError(json.dumps(result, ensure_ascii=False))
    return result


def _plugin_block() -> str:
    return f'[plugins."{PLUGIN_CONFIG_ID}"]\nenabled = true\n'


def enable_plugin_in_config(config_path: Path) -> dict[str, Any]:
    config_path.parent.mkdir(parents=True, exist_ok=True)
    original = config_path.read_text(encoding="utf-8") if config_path.exists() else ""
    lines = original.splitlines()
    header = f'[plugins."{PLUGIN_CONFIG_ID}"]'
    output: list[str] = []
    index = 0
    replaced = False

    while index < len(lines):
        line = lines[index]
        if line.strip() == header:
            output.append(header)
            output.append("enabled = true")
            replaced = True
            index += 1
            while index < len(lines) and not lines[index].lstrip().startswith("["):
                index += 1
            continue
        output.append(line)
        index += 1

    if not replaced:
        if output and output[-1].strip():
            output.append("")
        output.extend(_plugin_block().rstrip("\n").splitlines())

    config_path.write_text("\n".join(output).rstrip() + "\n", encoding="utf-8")
    return {"config_path": str(config_path), "plugin_id": PLUGIN_CONFIG_ID, "enabled": True}


def disable_plugin_in_config(config_path: Path) -> dict[str, Any]:
    if not config_path.exists():
        return {"config_path": str(config_path), "removed": False}
    lines = config_path.read_text(encoding="utf-8").splitlines()
    header = f'[plugins."{PLUGIN_CONFIG_ID}"]'
    output: list[str] = []
    removed = False
    index = 0
    while index < len(lines):
        if lines[index].strip() == header:
            removed = True
            index += 1
            while index < len(lines) and not lines[index].lstrip().startswith("["):
                index += 1
            continue
        output.append(lines[index])
        index += 1
    config_path.write_text("\n".join(output).rstrip() + ("\n" if output else ""), encoding="utf-8")
    return {"config_path": str(config_path), "removed": removed}


def _copy_plugin_bundle(home: Path) -> dict[str, Any]:
    source = home / ".tmp" / "marketplaces" / MARKETPLACE_NAME / "plugins" / PLUGIN_NAME
    if not source.exists():
        return {
            "status": "skipped",
            "reason": "marketplace_plugin_bundle_not_found",
            "source": str(source),
        }

    manifest_path = source / ".codex-plugin" / "plugin.json"
    try:
        version = json.loads(manifest_path.read_text(encoding="utf-8")).get("version", "current")
    except Exception:
        version = "current"

    cache_root = home / "plugins" / "cache" / MARKETPLACE_NAME / PLUGIN_NAME
    target = cache_root / str(version)
    if cache_root.exists():
        shutil.rmtree(cache_root)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target)
    return {"status": "ok", "source": str(source), "target": str(target), "version": version}


def _open_chrome_setup_page() -> dict[str, Any]:
    url = "chrome://inspect/#remote-debugging"
    if sys.platform.startswith("win"):
        result = _run(["cmd", "/c", "start", "", url])
    elif sys.platform == "darwin":
        result = _run(["open", url])
    else:
        result = _run(["xdg-open", url])
    return {"url": url, "result": result}


def _add_sourcing_mcp() -> list[dict[str, Any]]:
    home = str(sourcing_home()).replace("\\", "/")
    return [
        _run(["codex", "mcp", "remove", SOURCING_MCP_NAME]),
        _run(
            [
                "codex",
                "mcp",
                "add",
                SOURCING_MCP_NAME,
                "--env",
                "SOURCING1688_PROVIDER=auto",
                "--env",
                f"SOURCING1688_HOME={home}",
                "--",
                "uvx",
                "--refresh",
                "--from",
                GIT_REPO_URL,
                "sourcing1688-mcp",
            ]
        ),
    ]


def _add_chrome_mcp() -> list[dict[str, Any]]:
    remove = _run(["codex", "mcp", "remove", CHROME_MCP_NAME])
    if sys.platform.startswith("win"):
        add = _run(
            [
                "codex",
                "mcp",
                "add",
                CHROME_MCP_NAME,
                "--env",
                "SystemRoot=C:\\Windows",
                "--env",
                "PROGRAMFILES=C:\\Program Files",
                "--env",
                "CHROME_DEVTOOLS_MCP_NO_USAGE_STATISTICS=true",
                "--",
                "cmd",
                "/c",
                "npx",
                "-y",
                "chrome-devtools-mcp@latest",
                "--auto-connect",
                "--redact-network-headers",
                "--no-usage-statistics",
                "--no-performance-crux",
            ]
        )
    else:
        add = _run(
            [
                "codex",
                "mcp",
                "add",
                CHROME_MCP_NAME,
                "--env",
                "CHROME_DEVTOOLS_MCP_NO_USAGE_STATISTICS=true",
                "--",
                "npx",
                "-y",
                "chrome-devtools-mcp@latest",
                "--auto-connect",
                "--redact-network-headers",
                "--no-usage-statistics",
                "--no-performance-crux",
            ]
        )
    return [remove, add]


def install_codex(*, open_chrome_setup: bool = True) -> dict[str, Any]:
    if shutil.which("codex") is None:
        return {
            "status": "error",
            "message": "Codex CLI was not found on PATH.",
            "next_step": "Install or open Codex Desktop first, then rerun this command.",
        }
    if shutil.which("uvx") is None:
        return {
            "status": "error",
            "message": "uvx was not found on PATH.",
            "next_step": "Install uv first, then rerun this command.",
        }

    home = codex_home()
    config_path = home / "config.toml"
    home.mkdir(parents=True, exist_ok=True)

    steps: dict[str, Any] = {}
    steps["marketplace_add"] = _run(["codex", "plugin", "marketplace", "add", REPO_URL])
    steps["marketplace_upgrade"] = _run(["codex", "plugin", "marketplace", "upgrade", MARKETPLACE_NAME])
    if not steps["marketplace_add"]["ok"] and not steps["marketplace_upgrade"]["ok"]:
        return {
            "status": "error",
            "message": "Could not add or upgrade the Codex plugin marketplace.",
            "steps": steps,
        }

    steps["plugin_enabled"] = enable_plugin_in_config(config_path)
    steps["plugin_cache"] = _copy_plugin_bundle(home)
    steps["sourcing_mcp"] = _add_sourcing_mcp()
    steps["chrome_mcp"] = _add_chrome_mcp()
    steps["mcp_list"] = _run(["codex", "mcp", "list"])
    if open_chrome_setup:
        steps["chrome_setup_page"] = _open_chrome_setup_page()

    failed = [name for name in ["sourcing_mcp", "chrome_mcp"] if not steps[name][-1]["ok"]]
    status = "ok" if not failed else "partial_success"
    return {
        "status": status,
        "message": "Codex Desktop plugin and MCP servers are installed." if status == "ok" else "Install finished with MCP warnings.",
        "codex_home": str(home),
        "config_path": str(config_path),
        "plugin_id": PLUGIN_CONFIG_ID,
        "mcp_servers": [SOURCING_MCP_NAME, CHROME_MCP_NAME],
        "steps": steps,
        "next_step": "Restart Codex Desktop, open a new chat, then use @sourcing-agent-1688.",
    }


def uninstall_codex(*, remove_runtime: bool = False) -> dict[str, Any]:
    home = codex_home()
    steps: dict[str, Any] = {}
    steps["mcp_remove"] = [
        _run(["codex", "mcp", "remove", SOURCING_MCP_NAME]),
        _run(["codex", "mcp", "remove", CHROME_MCP_NAME]),
    ]
    steps["marketplace_remove"] = _run(["codex", "plugin", "marketplace", "remove", MARKETPLACE_NAME])
    steps["plugin_config"] = disable_plugin_in_config(home / "config.toml")

    cache = home / "plugins" / "cache" / MARKETPLACE_NAME
    if cache.exists():
        shutil.rmtree(cache)
        cache_removed = True
    else:
        cache_removed = False
    steps["plugin_cache"] = {"path": str(cache), "removed": cache_removed}

    if remove_runtime:
        runtime = sourcing_home()
        if runtime.exists():
            shutil.rmtree(runtime)
            runtime_removed = True
        else:
            runtime_removed = False
        steps["runtime"] = {"path": str(runtime), "removed": runtime_removed}

    return {
        "status": "ok",
        "message": "Codex Desktop plugin, marketplace, and MCP server config removed.",
        "steps": steps,
        "next_step": "Restart Codex Desktop.",
    }
