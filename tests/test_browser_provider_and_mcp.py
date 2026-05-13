from pathlib import Path

import pytest

from sourcing1688.mcp_server import mcp
from sourcing1688.providers.browser_provider import Browser1688Provider


@pytest.mark.anyio
async def test_browser_provider_verification_marker_detection():
    provider = Browser1688Provider()

    status, message = provider.detect_block_state_from_text("https://sec.taobao.com", "安全验证", "验证码")

    assert status == "blocked_by_verification"
    assert "verification" in message.lower()


def test_browser_search_dom_parser_fixture():
    html = (Path(__file__).parent / "fixtures" / "search_result_sample.html").read_text(encoding="utf-8")
    provider = Browser1688Provider()

    items = provider._parse_search_dom(html, "黑胶伞", 5)

    assert items[0].offer_id == "123456789"
    assert items[0].source_keyword == "黑胶伞"


def test_mcp_server_registers_expected_tools():
    tool_names = {tool.name for tool in mcp._tool_manager.list_tools()}

    assert "parse_1688_rendered_html" in tool_names
    assert "parse_1688_rendered_html_content" in tool_names
    assert "image_search_1688_products" in tool_names
    assert "check_1688_provider_capabilities" in tool_names
    assert "check_1688_browser_profile" in tool_names
    assert "open_1688_browser_profile" in tool_names
