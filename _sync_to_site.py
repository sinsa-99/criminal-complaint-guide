#!/usr/bin/env python3
"""원본 md의 본문 변경분을 site/src/content/docs/의 대응 파일로 sync.

- frontmatter는 site/ 파일 그대로 유지
- 본문은 원본 첫 # 헤딩 제거 + 내부 [..](..md) 링크 치환 후 대체

기본은 02·11만 sync. 다른 파일 필요하면 PAIRS에 추가.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).parent
SITE_DOCS = ROOT / "site" / "src" / "content" / "docs"

# (원본 md 파일명, site 슬러그 파일명)
PAIRS = [
    ("02_용어사전.md", "glossary.md"),
    ("06_스토리_종합본.md", "story-overview.md"),
    ("08_22건_스토리집.md", "stories-22.md"),
    ("10_심화팁_체크리스트.md", "tips.md"),
    ("11_고소당했을때_대처법.md", "defense.md"),
]

# 내부 .md 링크 치환 매핑 (마이그레이션 스크립트와 동일)
SLUG_MAP = {
    "00_README.md": "intro",  # index
    "01_절차_플로우차트.md": "procedure",
    "02_용어사전.md": "glossary",
    "03_상황별_고소가능_죄목.md": "charges",
    "04_고소장_작성법.md": "writing",
    "05_페이지_인덱스.md": "page-index",
    "06_스토리_종합본.md": "story-overview",
    "07_실전상황별_가이드.md": "scenarios-7",
    "08_22건_스토리집.md": "stories-22",
    "09_판례집.md": "cases",
    "10_심화팁_체크리스트.md": "tips",
    "11_고소당했을때_대처법.md": "defense",
}


def strip_first_heading(text: str) -> str:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith("# "):
            del lines[i]
            if i < len(lines) and not lines[i].strip():
                del lines[i]
            break
    return "\n".join(lines)


def rewrite_internal_links(text: str) -> str:
    def repl(m: re.Match) -> str:
        label, target, tail = m.group(1), m.group(2), m.group(3)
        anchor = ""
        if "#" in target:
            target, anchor = target.split("#", 1)
            anchor = "#" + anchor
        if target in SLUG_MAP:
            slug = SLUG_MAP[target]
            base = "/" if slug == "intro" else f"/{slug}/"
            return f"[{label}]({base}{anchor})"
        return m.group(0)

    return re.sub(r"\[([^\]]+)\]\(([^)]+\.md)([^)]*)\)", repl, text)


def extract_frontmatter(site_text: str) -> tuple[str, str]:
    """site 파일에서 frontmatter 블록과 (그 다음 본문)을 분리해 반환."""
    if not site_text.startswith("---\n"):
        return "", site_text
    end = site_text.find("\n---\n", 4)
    if end == -1:
        return "", site_text
    fm = site_text[: end + len("\n---\n")]
    body = site_text[end + len("\n---\n") :]
    return fm, body


def main() -> None:
    for orig_name, site_name in PAIRS:
        orig = ROOT / orig_name
        site = SITE_DOCS / site_name
        if not orig.exists() or not site.exists():
            print(f"  ✗ skip: {orig_name} or {site_name} missing")
            continue
        orig_text = orig.read_text(encoding="utf-8")
        new_body = strip_first_heading(orig_text)
        new_body = rewrite_internal_links(new_body)

        site_text = site.read_text(encoding="utf-8")
        fm, _ = extract_frontmatter(site_text)
        if not fm:
            print(f"  ✗ {site_name} has no frontmatter — skipped")
            continue

        site.write_text(fm + "\n" + new_body, encoding="utf-8")
        print(f"  ✓ {orig_name} → {site.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
