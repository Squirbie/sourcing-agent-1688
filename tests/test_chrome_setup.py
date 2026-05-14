from pathlib import Path

from sourcing1688 import chrome_setup


def test_windows_chrome_setup_uses_chrome_exe_directly(monkeypatch, tmp_path):
    chrome = tmp_path / "chrome.exe"
    chrome.write_text("", encoding="utf-8")

    monkeypatch.setattr(chrome_setup.sys, "platform", "win32")
    monkeypatch.setattr(chrome_setup.shutil, "which", lambda name: str(chrome) if name == "chrome.exe" else None)

    command = chrome_setup.chrome_devtools_setup_command()

    assert command[:4] == ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass"]
    assert str(chrome) in command[-1]
    assert chrome_setup.CHROME_DEVTOOLS_SETUP_URL in command[-1]
    assert "UIAutomationClient" in command[-1]
    assert "ValuePattern" in command[-1]
    assert "about:blank" in command[-1]
    assert "keybd_event" in command[-1]
    assert "cmd" not in command


def test_windows_chrome_setup_falls_back_without_cmd_start(monkeypatch):
    monkeypatch.setattr(chrome_setup.sys, "platform", "win32")
    monkeypatch.setattr(chrome_setup.shutil, "which", lambda name: None)
    monkeypatch.setattr(Path, "exists", lambda self: False)

    command = chrome_setup.chrome_devtools_setup_command()

    assert command[:4] == ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass"]
    assert "chrome.exe" in command[-1]
    assert chrome_setup.CHROME_DEVTOOLS_SETUP_URL in command[-1]
    assert "cmd" not in command


def test_macos_chrome_setup_uses_open_app(monkeypatch):
    monkeypatch.setattr(chrome_setup.sys, "platform", "darwin")

    command = chrome_setup.chrome_devtools_setup_command()

    assert command == ["open", "-a", "Google Chrome", chrome_setup.CHROME_DEVTOOLS_SETUP_URL]


def test_linux_chrome_setup_uses_chrome_command(monkeypatch):
    monkeypatch.setattr(chrome_setup.sys, "platform", "linux")
    monkeypatch.setattr(chrome_setup.shutil, "which", lambda name: None)

    command = chrome_setup.chrome_devtools_setup_command()

    assert command == ["google-chrome", "--new-tab", chrome_setup.CHROME_DEVTOOLS_SETUP_URL]
