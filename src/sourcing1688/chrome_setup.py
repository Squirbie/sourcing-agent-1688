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
            "Start-Process -FilePath $chrome -ArgumentList @('--new-tab', 'about:blank') | Out-Null",
            "Start-Sleep -Milliseconds 1000",
            "Add-Type -AssemblyName UIAutomationClient",
            "Add-Type -AssemblyName UIAutomationTypes",
            "Add-Type 'using System; using System.Runtime.InteropServices; public class S1688Win32 { [DllImport(\"user32.dll\")] public static extern bool SetForegroundWindow(IntPtr hWnd); [DllImport(\"user32.dll\")] public static extern bool ShowWindowAsync(IntPtr hWnd, int nCmdShow); [DllImport(\"user32.dll\")] public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo); }'",
            "$proc = Get-Process chrome | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1",
            "[S1688Win32]::ShowWindowAsync($proc.MainWindowHandle, 9) | Out-Null",
            "[S1688Win32]::SetForegroundWindow($proc.MainWindowHandle) | Out-Null",
            "$root = [System.Windows.Automation.AutomationElement]::FromHandle($proc.MainWindowHandle)",
            "$condition = New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::ControlTypeProperty, [System.Windows.Automation.ControlType]::Edit)",
            "$addressBar = $root.FindFirst([System.Windows.Automation.TreeScope]::Descendants, $condition)",
            "$addressBar.SetFocus()",
            "$valuePattern = $addressBar.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern)",
            "$valuePattern.SetValue($url)",
            "Start-Sleep -Milliseconds 200",
            "[S1688Win32]::keybd_event(0x0D, 0, 0, [UIntPtr]::Zero)",
            "Start-Sleep -Milliseconds 50",
            "[S1688Win32]::keybd_event(0x0D, 0, 2, [UIntPtr]::Zero)",
        ]
    )
