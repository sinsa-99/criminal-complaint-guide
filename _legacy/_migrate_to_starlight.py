#!/usr/bin/env python3
"""md 12개 → site/src/content/docs/ 영문 슬러그로 이주 + frontmatter 입히기.

frontmatter 생성 규칙:
- title: 원본 md의 첫 # 라인에서 추출
- description: 첫 > blockquote 라인에서 추출 (있으면)
- sidebar.order: 파일명 prefix 번호

내부 [xx](yy.md) 링크는 별도 task에서 처리.
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
DOCS = ROOT / "site" / "src" / "content" / "docs"

# (원본 파일명, 영문 슬러그, sidebar order)
MAPPING: list[tuple[str, str, int]] = [
    ("00_README.md",                 "intro",            0),
    ("01_절차_플로우차트.md",        "procedure",        1),
    ("02_용어사전.md",                "glossary",         2),
    ("03_상황별_고소가능_죄목.md",   "charges",          3),
    ("04_고소장_작성법.md",           "writing",          4),
    ("05_페이지_인덱스.md",           "page-index",       5),
    ("06_스토리_종합본.md",           "story-overview",   6),
    ("07_실전상황별_가이드.md",       "scenarios-7",      7),
    ("08_22건_스토리집.md",           "stories-22",       8),
    ("09_판례집.md",                  "cases",            9),
    ("10_심화팁_체크리스트.md",       "tips",            10),
    ("11_고소당했을때_대처법.md",     "defense",         11),
]

# 슬러그 매핑: 원본 md 파일명 → 새 슬러그 경로
SLUG_MAP = {src: slug for src, slug, _ in MAPPING}


def extract_title_and_desc(text: str) -> tuple[str, str | None]:
    """첫 # 헤딩과 첫 > blockquote 추출."""
    title = ""
    desc: str | None = None
    for line in text.splitlines()[:10]:
        s = line.strip()
        if not title and s.startswith("# "):
            title = s[2:].strip()
        elif desc is None and s.startswith("> "):
            desc = s[2:].strip()
            # description은 한 줄로 (markdown 제거 살짝)
            desc = re.sub(r"\*\*([^*]+)\*\*", r"\1", desc)
            desc = re.sub(r"`([^`]+)`", r"\1", desc)
            if len(desc) > 160:
                desc = desc[:157] + "..."
            break
    return title, desc


def strip_first_heading(text: str) -> str:
    """첫 # 헤딩 한 줄만 제거 (Starlight가 frontmatter title을 H1로 렌더링하므로 중복 방지)."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith("# "):
            del lines[i]
            # 바로 다음 빈 줄도 제거
            if i < len(lines) and not lines[i].strip():
                del lines[i]
            break
    return "\n".join(lines)


def rewrite_internal_links(text: str) -> str:
    """[xxx](yy.md) → [xxx](/criminal-complaint-guide/SLUG/) 형태로 변환.

    Starlight base path 포함된 절대경로로 작성. (base는 astro.config에서 설정)
    """
    def repl(m: re.Match) -> str:
        label, target = m.group(1), m.group(2)
        # 앵커 분리
        anchor = ""
        if "#" in target:
            target, anchor = target.split("#", 1)
            anchor = "#" + anchor
        if target in SLUG_MAP:
            return f"[{label}](/{SLUG_MAP[target]}/{anchor})"
        return m.group(0)

    return re.sub(r"\[([^\]]+)\]\(([^)]+\.md)([^)]*)\)", repl, text)


def yaml_escape(s: str) -> str:
    """YAML scalar로 안전하게 — 콜론/따옴표 포함 시 큰따옴표로 감싸고 내부 큰따옴표 이스케이프."""
    return s.replace('\\', '\\\\').replace('"', '\\"')


def build_frontmatter(title: str, desc: str | None, order: int) -> str:
    lines = ["---"]
    lines.append(f'title: "{yaml_escape(title)}"')
    if desc:
        lines.append(f'description: "{yaml_escape(desc)}"')
    lines.append("sidebar:")
    lines.append(f"  order: {order}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def main() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    for src_name, slug, order in MAPPING:
        src = ROOT / src_name
        if not src.exists():
            print(f"  skip (not found): {src_name}")
            continue
        text = src.read_text(encoding="utf-8")
        title, desc = extract_title_and_desc(text)
        body = strip_first_heading(text)
        body = rewrite_internal_links(body)

        # 'intro'는 사이트 루트로 (index.md로 저장하면 / 가 됨)
        if slug == "intro":
            out_path = DOCS / "index.md"
        else:
            out_path = DOCS / f"{slug}.md"

        out_path.write_text(build_frontmatter(title, desc, order) + body, encoding="utf-8")
        print(f"  ✓ {src_name} → {out_path.relative_to(ROOT)} [{title}]")


if __name__ == "__main__":
    main()
