#!/usr/bin/env python3
"""'처벌X' 표현 6곳을 맥락 맞게 수정.

- 형사미성년자 (1곳): '처벌 안 함' (법이 의도적으로 면제)
- 친고죄·반의사불벌 (5곳): '처벌 못 함' (소추 요건 미충족)

원본(정리/*.md)과 site/src/content/docs/*.md 둘 다 동일하게 수정.
"""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).parent
SITE_DOCS = ROOT / "site" / "src" / "content" / "docs"

# (대상 파일 stem(원본) / 슬러그, 찾을 라인, 바꿀 라인)
EDITS = [
    # 형사미성년자 — '처벌 안 함'
    (
        "07_실전상황별_가이드.md", "scenarios-7.md",
        "> 💡 **만 14세 미만 = 형사미성년자** — 형사처벌 X, 보호처분 (소년법). 만 10~14세는 \"촉법소년\" — 형사 미성년이지만 보호처분 가능.",
        "> 💡 **만 14세 미만 = 형사미성년자** — 형사처벌 안 함, 보호처분 (소년법). 만 10~14세는 \"촉법소년\" — 형사 미성년이지만 보호처분 가능.",
    ),
    # 친고죄·반의사불벌 — '처벌 못 함'
    (
        "02_용어사전.md", "glossary.md",
        "| **친고죄 고소** | 고소가 있어야만 처벌 가능 | 모욕죄(§311), 사자명예훼손(§308) | 고소 없으면 수사기관도 처벌 X |",
        "| **친고죄 고소** | 고소가 있어야만 처벌 가능 | 모욕죄(§311), 사자명예훼손(§308) | 고소 없으면 수사기관도 처벌 못 함 |",
    ),
    (
        "02_용어사전.md", "glossary.md",
        "> 💡 **친고죄와 반의사불벌의 차이**: 친고죄는 \"고소가 있어야 처벌\", 반의사불벌은 \"처벌 의사가 없으면 처벌 X\". 출발점과 종결 방향이 반대.",
        "> 💡 **친고죄와 반의사불벌의 차이**: 친고죄는 \"고소가 있어야 처벌\", 반의사불벌은 \"처벌 의사가 없으면 처벌 못 함\". 출발점과 종결 방향이 반대.",
    ),
    (
        "03_상황별_고소가능_죄목.md", "charges.md",
        "- 과거: 피해자가 처벌 안 원하면 처벌 X",
        "- 과거: 피해자가 처벌 안 원하면 처벌 못 함",
    ),
    (
        "03_상황별_고소가능_죄목.md", "charges.md",
        "| 모욕 (311조) | **친고죄** | 고소 없으면 처벌 X |",
        "| 모욕 (311조) | **친고죄** | 고소 없으면 처벌 못 함 |",
    ),
    (
        "07_실전상황별_가이드.md", "scenarios-7.md",
        "- 친고죄(모욕): 고소기간 6개월, 고소 없으면 처벌 X",
        "- 친고죄(모욕): 고소기간 6개월, 고소 없으면 처벌 못 함",
    ),
]


def apply(path: Path, find: str, replace: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if find not in text:
        return False
    path.write_text(text.replace(find, replace), encoding="utf-8")
    return True


def main() -> None:
    total = 0
    for orig_name, slug_name, find, replace in EDITS:
        orig_path = ROOT / orig_name
        slug_path = SITE_DOCS / slug_name
        for p in (orig_path, slug_path):
            ok = apply(p, find, replace)
            mark = "✓" if ok else "✗ (not found)"
            print(f"  {mark} {p.relative_to(ROOT)}")
            if ok:
                total += 1
    print(f"\n총 {total}곳 수정")


if __name__ == "__main__":
    main()
