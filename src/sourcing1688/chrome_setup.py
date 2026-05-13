from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path


CHROME_DEVTOOLS_SETUP_URL = "chrome://inspect/#remote-debugging"


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
        if chrome:
            return [chrome, CHROME_DEVTOOLS_SETUP_URL]
        return ["chrome.exe", CHROME_DEVTOOLS_SETUP_URL]
    if sys.platform == "darwin":
        return ["open", "-a", "Google Chrome", CHROME_DEVTOOLS_SETUP_URL]
    chrome = find_chrome_executable() or "google-chrome"
    return [chrome, CHROME_DEVTOOLS_SETUP_URL]
