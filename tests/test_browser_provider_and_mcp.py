from pathlib import Path

import pytest

from sourcing1688 import mcp_server
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


def test_browser_search_dom_parser_handles_mobile_offer_links():
    html = """
    <html><body>
      <a href="http://detail.m.1688.com/page/index.html?offerId=812305105474&skuId=5505516668292">
        抖音款金属直播手机支架 10万+件 回头率55%
        <img src="//cbu01.alicdn.com/img/ibank/O1CN015ws3s41zgo2Mv28yO_!!2216935376744-0-cib.jpg">
      </a>
      <a href="https://s.1688.com/selloffer/similar_search.html?offerIds=812305105474">找相似</a>
    </body></html>
    """
    provider = Browser1688Provider()

    items = provider._parse_search_dom(html, "\u624b\u673a\u652f\u67b6", 5)

    assert len(items) == 1
    assert items[0].offer_id == "812305105474"
    assert items[0].image_url == "https://cbu01.alicdn.com/img/ibank/O1CN015ws3s41zgo2Mv28yO_!!2216935376744-0-cib.jpg"


def test_mcp_server_registers_expected_tools():
    tool_names = {tool.name for tool in mcp._tool_manager.list_tools()}

    assert "parse_1688_rendered_html" in tool_names
    assert "parse_1688_rendered_html_content" in tool_names
    assert "parse_1688_network_payload_content" in tool_names
    assert "download_1688_product_assets_from_html_content" in tool_names
    assert "image_search_1688_products" in tool_names
    assert "check_1688_provider_capabilities" in tool_names
    assert "provider_check_1688" in tool_names
    assert "check_1688_browser_profile" in tool_names
    assert "open_1688_browser_profile" in tool_names
    assert "open_chrome_devtools_setup" in tool_names


def test_open_chrome_devtools_setup_can_be_mocked(monkeypatch):
    calls = []

    class MockCompleted:
        returncode = 0
        stderr = ""

    def mock_run(args, **kwargs):
        calls.append(args)
        return MockCompleted()

    monkeypatch.setattr(mcp_server.subprocess, "run", mock_run)
    monkeypatch.setattr(mcp_server.sys, "platform", "win32")

    payload = mcp_server.open_chrome_devtools_setup()

    assert payload["status"] == "ok"
    assert payload["returncode"] == 0
    assert any("chrome://inspect/#remote-debugging" in " ".join(call) for call in calls)
    assert not any("https://www.1688.com" in " ".join(call) for call in calls)
