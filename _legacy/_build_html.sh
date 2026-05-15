#!/bin/bash
set -e
cd "/Users/dddhhh5137/고소의 기술/정리"

# 1. 표지·서문 + 7개 md 지정 순서로 합치기
cat > _combined.md << 'COVER'
---
title: 고소의 기술 — 통합 정리집
subtitle: 학습용 변환자료
date: 2026-05-15
---

<p style="font-size:13px;color:var(--muted);margin:0 0 24px 0;">by Kim Donghyeon</p>

# 고소의 기술 — 통합 정리집

> 학습용 변환된 자료. 형사절차 표준 지식 + 법제처 실시간 조회 법령·판례 + 가상 사례로 재구성.

## 이 문서의 구성

1. **용어 사전** — 고소·송치·기소·무죄까지 핵심 용어
2. **절차 플로우차트** — 고소→수사→재판 트리 (Mermaid 다이어그램)
3. **상황별 고소가능 죄목** — 무슨 죄로 매칭되는지
4. **고소장 작성법** — 9블록 표준 + 실패 패턴
5. **고소당했을 때 대처법** — 피의자 방어 8단계 매뉴얼
6. **22개 실전 상황 가이드** — 일상 사건별 매뉴얼
7. **심화 팁 + 실전 고소장 완성본 + 변호사 상담 체크리스트**
8. **실제 판례집** — 대법원·고등법원 사건번호·핵심 쟁점

## 이 문서의 한계

- 일반 학습·참고용. 본인 사건 처리 시 변호사 상담 권장
- 법령·판례는 2026년 5월 기준 (이후 개정 가능)
- 가상 사례의 인물·사건은 모두 가명·허구

---

COVER

# 지정 순서대로 본문 합치기 (제목 충돌 방지 위해 헤더 한 단계 내림)
for f in 02_용어사전.md 01_절차_플로우차트.md 03_상황별_고소가능_죄목.md 04_고소장_작성법.md 11_고소당했을때_대처법.md 07_실전상황별_가이드.md 10_심화팁_체크리스트.md 09_판례집.md; do
  echo "" >> _combined.md
  echo "---" >> _combined.md
  echo "" >> _combined.md
  cat "$f" >> _combined.md
done

# 2. 푸터
cat >> _combined.md << 'FOOTER'

---

## 마무리

이 문서는 형사절차를 빠르게 익히기 위한 학습용 자료입니다.
실제 사건 처리 시에는 반드시 변호사와 상담하세요.

- **무료 법률상담**: 대한법률구조공단 132
- **여성긴급전화**: 1366
- **사이버수사대**: 117
- **금감원 보이스피싱**: 1332
- **디지털성범죄피해자지원센터**: 02-735-8994
- **층간소음이웃사이센터**: 1661-2642
- **117 학교폭력신고센터**: 117
- **노동부**: 1350
- **개인정보침해 신고센터**: 118

FOOTER

# 3. Pandoc으로 body HTML 변환 (--standalone X, fragment만)
pandoc _combined.md -o _body.html --toc --toc-depth=3 -f markdown -t html5 2>&1

# 4. mermaid 코드블록 후처리: pandoc이 만든 모든 형태 → <pre class="mermaid">순수text</pre>
python3 << 'PY'
import re, html as htmllib
with open('_body.html', 'r') as f:
    src = f.read()

def clean(text):
    # <code> 태그 제거
    text = re.sub(r'</?code[^>]*>', '', text)
    # 모든 HTML 엔티티 디코드 (&quot; &gt; &lt; &amp; &#39; 등 전부)
    text = htmllib.unescape(text)
    return text.strip()

# 패턴 0 (가장 흔함): <pre class="mermaid"><code>...</code></pre> — Pandoc 표준
src = re.sub(
    r'<pre class="mermaid">\s*<code[^>]*>(.*?)</code>\s*</pre>',
    lambda m: '<pre class="mermaid">\n' + clean(m.group(1)) + '\n</pre>',
    src, flags=re.DOTALL
)
# 패턴 1: <pre class="...language-mermaid..."><code>...</code></pre>
src = re.sub(
    r'<pre[^>]*class="[^"]*language-mermaid[^"]*"[^>]*>(.*?)</pre>',
    lambda m: '<pre class="mermaid">\n' + clean(m.group(1)) + '\n</pre>',
    src, flags=re.DOTALL
)
# 패턴 2: <div class="sourceCode"><pre class="sourceCode mermaid"><code>...</code></pre></div>
src = re.sub(
    r'<div class="sourceCode"[^>]*>\s*<pre[^>]*class="sourceCode mermaid"[^>]*>(.*?)</pre>\s*</div>',
    lambda m: '<pre class="mermaid">\n' + clean(m.group(1)) + '\n</pre>',
    src, flags=re.DOTALL
)
# 패턴 3: <pre><code class="mermaid">...</code></pre>
src = re.sub(
    r'<pre[^>]*>\s*<code[^>]*class="[^"]*mermaid[^"]*"[^>]*>(.*?)</code>\s*</pre>',
    lambda m: '<pre class="mermaid">\n' + clean(m.group(1)) + '\n</pre>',
    src, flags=re.DOTALL
)

with open('_body.html', 'w') as f:
    f.write(src)

# 검증
count = len(re.findall(r'<pre class="mermaid">', src))
remaining = len(re.findall(r'&quot;|&lt;|&gt;', src))
print(f"mermaid 후처리 완료: {count}개 블록")
# 첫 블록 출력 검증
m = re.search(r'<pre class="mermaid">(.*?)</pre>', src, re.DOTALL)
if m:
    print("--- 첫 블록 미리보기 ---")
    print(m.group(1)[:200])
PY

echo "==> _body.html 빌드 완료"
wc -c _body.html
