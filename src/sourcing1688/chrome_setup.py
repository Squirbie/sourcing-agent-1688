from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import URLError
from urllib.request import urlopen


CHROME_DEVTOOLS_SETUP_URL = "chrome://inspect/#remote-debugging"
DEFAULT_CHROME_DEVTOOLS_PORT = 9222
DEFAULT_CHROME_DEVTOOLS_URL = f"http://127.0.0.1:{DEFAULT_CHROME_DEVTOOLS_PORT}"
DEFAULT_CHROME_START_URL = "https://www.1688.com/"
SETUP_MARKER_RELATIVE_PATH = Path("config") / "chrome-devtools-setup.json"


def _candidate_chrome_paths() -> list[Path]:
    candidates: list[Path] = []
    for env_name in ("PROGRAMFILES", "PROGRAMFILES(X86)", "LOCALAPPDATA"):
        root = os.environ.get(env_name)
        if root:
            candidates.append(Path(root) / "Google" / "Chrome" / "Application" / "chrome.exe")
    return candidates


def find_chrome_executable() -> str | None:
    for executable in ("chrome.exe", "chrome"):
        found = shutil.which(executable)
        if found:
            return found
    if sys.platform.startswith("win"):
        for path in _candidate_chrome_paths():
            if path.exists():
                return str(path)
    return None


def chrome_devtools_setup_command() -> list[str]:
    if sys.platform.startswith("win"):
        chrome = find_chrome_executable()
        chrome_command = chrome or "chrome.exe"
        script = _windows_focus_chrome_setup_script(chrome_command)
        return ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script]
    if sys.platform == "darwin":
        return ["open", "-a", "Google Chrome", CHROME_DEVTOOLS_SETUP_URL]
    chrome = find_chrome_executable() or "google-chrome"
    return [chrome, "--new-tab", CHROME_DEVTOOLS_SETUP_URL]


def chrome_devtools_profile_dir(home: str | Path | None = None) -> Path:
    root = Path(home) if home else Path(os.environ.get("SOURCING1688_HOME") or Path.home() / ".sourcing1688")
    return root / "chrome-devtools-profile"


def chrome_devtools_port_endpoint(port: int = DEFAULT_CHROME_DEVTOOLS_PORT) -> str:
    return f"http://127.0.0.1:{port}"


def chrome_devtools_port_command(
    *,
    port: int = DEFAULT_CHROME_DEVTOOLS_PORT,
    user_data_dir: str | Path | None = None,
    url: str = DEFAULT_CHROME_START_URL,
) -> list[str]:
    chrome = find_chrome_executable() or ("chrome.exe" if sys.platform.startswith("win") else "google-chrome")
    profile = Path(user_data_dir) if user_data_dir else chrome_devtools_profile_dir()
    return [
        chrome,
        f"--remote-debugging-port={port}",
        f"--user-data-dir={profile}",
        "--no-first-run",
        "--new-window",
        url,
    ]


def _get_json(url: str, *, timeout: float = 2.0) -> tuple[bool, Any, str | None]:
    try:
        with urlopen(url, timeout=timeout) as response:
            body = response.read().decode("utf-8", errors="replace")
    except (OSError, URLError) as exc:
        return False, None, str(exc)
    try:
        return True, json.loads(body), None
    except json.JSONDecodeError as exc:
        return False, None, str(exc)


def check_chrome_devtools_endpoint(endpoint: str = DEFAULT_CHROME_DEVTOOLS_URL, *, timeout: float = 2.0) -> dict[str, Any]:
    ok, payload, error = _get_json(f"{endpoint.rstrip('/')}/json/version", timeout=timeout)
    if not ok:
        return {
            "ok": False,
            "endpoint": endpoint,
            "error": error,
            "next_step": "Start Chrome with --remote-debugging-port=9222, then retry.",
        }
    return {
        "ok": True,
        "endpoint": endpoint,
        "browser": payload.get("Browser") if isinstance(payload, dict) else None,
        "websocket_debugger_url": payload.get("webSocketDebuggerUrl") if isinstance(payload, dict) else None,
    }


def list_chrome_devtools_pages(endpoint: str = DEFAULT_CHROME_DEVTOOLS_URL, *, timeout: float = 2.0) -> dict[str, Any]:
    ok, payload, error = _get_json(f"{endpoint.rstrip('/')}/json/list", timeout=timeout)
    if not ok:
        return {"ok": False, "endpoint": endpoint, "pages": [], "error": error}
    pages = payload if isinstance(payload, list) else []
    return {"ok": True, "endpoint": endpoint, "pages": pages}


def _ps_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def _windows_focus_chrome_setup_script(chrome_command: str) -> str:
    chrome = _ps_quote(chrome_command)
    inspect_url = "chrome%3A%2F%2Finspect%2F%23remote-debugging"
    return "; ".join(
        [
            "$ErrorActionPreference = 'Stop'",
            f"$chrome = {chrome}",
            f"$inspectUrl = '{inspect_url}'",
            f"$port = {DEFAULT_CHROME_DEVTOOLS_PORT}",
            "$endpoint = \"http://127.0.0.1:$port\"",
            "$home = [Environment]::GetEnvironmentVariable('SOURCING1688_HOME')",
            "if ([string]::IsNullOrWhiteSpace($home)) { $home = Join-Path $env:USERPROFILE '.sourcing1688' }",
            "$profile = Join-Path $home 'chrome-devtools-profile'",
            "New-Item -ItemType Directory -Force -Path $profile | Out-Null",
            "$ready = $false",
            "try { Invoke-RestMethod -UseBasicParsing -Uri \"$endpoint/json/version\" -TimeoutSec 1 | Out-Null; $ready = $true } catch { $ready = $false }",
            "if (-not $ready) { Start-Process -FilePath $chrome -ArgumentList @(\"--remote-debugging-port=$port\", \"--user-data-dir=$profile\", '--no-first-run', '--new-window', 'about:blank') | Out-Null }",
            "for ($i = 0; $i -lt 40 -and -not $ready; $i++) { try { Invoke-RestMethod -UseBasicParsing -Uri \"$endpoint/json/version\" -TimeoutSec 1 | Out-Null; $ready = $true } catch { Start-Sleep -Milliseconds 250 } }",
            "if (-not $ready) { throw \"Chrome DevTools endpoint did not respond at $endpoint. Close any existing Chrome process using port $port, then retry.\" }",
            "Invoke-RestMethod -UseBasicParsing -Method Put -Uri \"$endpoint/json/new?$inspectUrl\" -TimeoutSec 3 | Out-Null",
        ]
    )


def chrome_setup_marker_path(home: str | Path | None = None) -> Path:
    root = Path(home) if home else Path(os.environ.get("SOURCING1688_HOME") or Path.home() / ".sourcing1688")
    return root / SETUP_MARKER_RELATIVE_PATH


def read_chrome_setup_marker(home: str | Path | None = None) -> dict[str, Any] | None:
    path = chrome_setup_marker_path(home)
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    if not isinstance(data, dict):
        return None
    data.setdefault("path", str(path))
    return data


def is_chrome_setup_marker_verified(marker: dict[str, Any] | None) -> bool:
    return bool(marker and marker.get("status") == "verified" and marker.get("endpoint"))


def mark_chrome_setup_opened(home: str | Path | None = None, *, command: list[str] | None = None) -> dict[str, Any]:
    path = chrome_setup_marker_path(home)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "status": "opened",
        "url": CHROME_DEVTOOLS_SETUP_URL,
        "opened_at": datetime.now(timezone.utc).isoformat(),
        "command": command or chrome_devtools_setup_command(),
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"path": str(path), **payload}


def mark_chrome_devtools_endpoint_verified(
    home: str | Path | None = None,
    *,
    endpoint: str = DEFAULT_CHROME_DEVTOOLS_URL,
    command: list[str] | None = None,
    pages: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    path = chrome_setup_marker_path(home)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "status": "verified",
        "endpoint": endpoint,
        "verified_at": datetime.now(timezone.utc).isoformat(),
        "command": command,
        "pages": pages or [],
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"path": str(path), **payload}


def start_chrome_devtools_port(
    *,
    port: int = DEFAULT_CHROME_DEVTOOLS_PORT,
    url: str = DEFAULT_CHROME_START_URL,
    user_data_dir: str | Path | None = None,
    wait_seconds: float = 8.0,
) -> dict[str, Any]:
    endpoint = chrome_devtools_port_endpoint(port)
    profile = Path(user_data_dir) if user_data_dir else chrome_devtools_profile_dir()
    profile.mkdir(parents=True, exist_ok=True)

    existing = check_chrome_devtools_endpoint(endpoint, timeout=1.0)
    if existing.get("ok"):
        pages = list_chrome_devtools_pages(endpoint, timeout=1.0)
        marker = mark_chrome_devtools_endpoint_verified(endpoint=endpoint, command=None, pages=pages.get("pages", []))
        return {
            "status": "ok",
            "endpoint": endpoint,
            "already_running": True,
            "endpoint_verified": True,
            "pages": pages.get("pages", []),
            "marker": marker,
        }

    command = chrome_devtools_port_command(port=port, user_data_dir=profile, url=url)
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
    except Exception as exc:  # noqa: BLE001
        return {
            "status": "error",
            "endpoint": endpoint,
            "command": command,
            "error": str(exc),
            "next_step": "Check that Google Chrome is installed, then rerun `sourcing-agent-1688 chrome-devtools start`.",
        }

    deadline = time.monotonic() + wait_seconds
    check = {"ok": False}
    while time.monotonic() <= deadline:
        check = check_chrome_devtools_endpoint(endpoint, timeout=1.0)
        if check.get("ok"):
            pages = list_chrome_devtools_pages(endpoint, timeout=1.0)
            marker = mark_chrome_devtools_endpoint_verified(endpoint=endpoint, command=command, pages=pages.get("pages", []))
            return {
                "status": "ok",
                "endpoint": endpoint,
                "already_running": False,
                "endpoint_verified": True,
                "pid": getattr(process, "pid", None),
                "command": command,
                "profile_path": str(profile),
                "pages": pages.get("pages", []),
                "marker": marker,
            }
        time.sleep(0.25)

    return {
        "status": "error",
        "endpoint": endpoint,
        "endpoint_verified": False,
        "pid": getattr(process, "pid", None),
        "command": command,
        "profile_path": str(profile),
        "last_check": check,
        "next_step": f"Open {endpoint}/json/version in a browser. If it does not respond, close Chrome for this profile and rerun the start command.",
    }
