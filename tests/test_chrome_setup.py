from pathlib import Path

from sourcing1688 import chrome_setup


def test_windows_chrome_setup_uses_chrome_exe_directly(monkeypatch, tmp_path):
    chrome = tmp_path / "chrome.exe"
    chrome.write_text("", encoding="utf-8")

    monkeypatch.setattr(chrome_setup.sys, "platform", "win32")
    monkeypatch.setattr(chrome_setup.shutil, "which", lambda name: str(chrome) if name == "chrome.exe" else None)

    command = chrome_setup.chrome_devtools_setup_command()

    assert command == [str(chrome), "--new-tab", chrome_setup.CHROME_DEVTOOLS_SETUP_URL]
    assert "cmd" not in command
    assert "start" not in command


def test_windows_chrome_setup_falls_back_without_shell_start(monkeypatch):
    monkeypatch.setattr(chrome_setup.sys, "platform", "win32")
    monkeypatch.setattr(chrome_setup.shutil, "which", lambda name: None)
    monkeypatch.setattr(Path, "exists", lambda self: False)

    command = chrome_setup.chrome_devtools_setup_command()

    assert command == ["chrome.exe", "--new-tab", chrome_setup.CHROME_DEVTOOLS_SETUP_URL]


def test_macos_chrome_setup_uses_open_app(monkeypatch):
    monkeypatch.setattr(chrome_setup.sys, "platform", "darwin")

    command = chrome_setup.chrome_devtools_setup_command()

    assert command == ["open", "-a", "Google Chrome", chrome_setup.CHROME_DEVTOOLS_SETUP_URL]


def test_linux_chrome_setup_uses_chrome_command(monkeypatch):
    monkeypatch.setattr(chrome_setup.sys, "platform", "linux")
    monkeypatch.setattr(chrome_setup.shutil, "which", lambda name: None)

    command = chrome_setup.chrome_devtools_setup_command()

    assert command == ["google-chrome", "--new-tab", chrome_setup.CHROME_DEVTOOLS_SETUP_URL]
