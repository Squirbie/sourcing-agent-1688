from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_docs_references_contains_required_links():
    content = (ROOT / "docs" / "references.md").read_text(encoding="utf-8")

    assert "https://github.com/openclaw/skills" in content
    assert "https://github.com/jiyun/1688" in content
    assert "https://github.com/netkaruma/search1688api" in content
    assert "CAPTCHA" in content
