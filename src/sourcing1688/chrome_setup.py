from __future__ import annotations

import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHROME_DEVTOOLS_SETUP_URL = "chrome://inspect/#remote-debugging"
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


def _ps_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def _windows_focus_chrome_setup_script(chrome_command: str) -> str:
    chrome = _ps_quote(chrome_command)
    url = _ps_quote(CHROME_DEVTOOLS_SETUP_URL)
    return "; ".join(
        [
            "$ErrorActionPreference = 'SilentlyContinue'",
            f"$chrome = {chrome}",
            f"$url = {url}",
            "Start-Process -FilePath $chrome -ArgumentList @('--new-tab', $url) | Out-Null",
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
