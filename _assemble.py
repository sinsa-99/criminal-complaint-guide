#!/usr/bin/env python3
"""body.html을 self-contained HTML 템플릿에 임베드"""
import re
from pathlib import Path

base = Path("/Users/dddhhh5137/고소의 기술/정리")
body = (base / "_body.html").read_text()

# Pandoc TOC를 본문에서 추출 — 첫번째 <nav> 블록
toc_match = re.search(r'(<nav id="TOC"[^>]*>.*?</nav>)', body, re.DOTALL)
toc_html = toc_match.group(1) if toc_match else ""
body_no_toc = body.replace(toc_html, "") if toc_html else body

# TOC의 nav id, role 정리 (모바일 사이드바용)
toc_html = toc_html.replace('id="TOC"', 'id="toc"').replace('role="doc-toc"', '')

template = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>고소의 기술 — 통합 정리집</title>
<style>
:root {
  --bg: #ffffff;
  --fg: #1a1a1a;
  --muted: #6b7280;
  --accent: #2563eb;
  --accent-soft: #dbeafe;
  --border: #e5e7eb;
  --code-bg: #f6f8fa;
  --table-stripe: #f9fafb;
  --quote-border: #2563eb;
  --quote-bg: #eff6ff;
  --shadow: 0 1px 3px rgba(0,0,0,0.05);
}
[data-theme="dark"] {
  --bg: #0f172a;
  --fg: #e2e8f0;
  --muted: #94a3b8;
  --accent: #60a5fa;
  --accent-soft: #1e3a5f;
  --border: #1e293b;
  --code-bg: #1e293b;
  --table-stripe: #1a2436;
  --quote-border: #60a5fa;
  --quote-bg: #172033;
  --shadow: 0 1px 3px rgba(0,0,0,0.3);
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; -webkit-text-size-adjust: 100%; }
body {
  margin: 0;
  font-family: -apple-system, "Apple SD Gothic Neo", "Pretendard", BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  font-size: 16px;
  line-height: 1.7;
  color: var(--fg);
  background: var(--bg);
  display: flex;
  min-height: 100vh;
}

/* 사이드바 (TOC) */
#sidebar {
  width: 320px;
  flex-shrink: 0;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
  border-right: 1px solid var(--border);
  padding: 24px 16px;
  background: var(--bg);
  z-index: 100;
}
#sidebar h2 {
  margin: 0 0 12px 0;
  font-size: 14px;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--muted);
}
#sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
#sidebar li { margin: 2px 0; }
#sidebar a {
  display: block;
  padding: 6px 10px;
  font-size: 14px;
  color: var(--fg);
  text-decoration: none;
  border-radius: 6px;
  border-left: 3px solid transparent;
}
#sidebar a:hover {
  background: var(--accent-soft);
  border-left-color: var(--accent);
}
#sidebar ul ul { margin-left: 10px; border-left: 1px solid var(--border); }
#sidebar ul ul a { font-size: 13px; color: var(--muted); }
#sidebar ul ul ul { display: none; }  /* 3단 이상 숨김 */

/* 본문 */
main {
  flex: 1;
  max-width: 880px;
  margin: 0 auto;
  padding: 32px 48px 96px;
  min-width: 0;
}
h1 { font-size: 2em; margin-top: 1.5em; padding-bottom: 0.3em; border-bottom: 2px solid var(--border); }
h2 { font-size: 1.5em; margin-top: 1.8em; padding-bottom: 0.3em; border-bottom: 1px solid var(--border); }
h3 { font-size: 1.2em; margin-top: 1.5em; }
h4 { font-size: 1.05em; margin-top: 1.3em; color: var(--accent); }
h1, h2, h3, h4 { line-height: 1.3; font-weight: 700; }
p { margin: 0.8em 0; }
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }

/* 표 */
table {
  border-collapse: collapse;
  margin: 1em 0;
  width: 100%;
  font-size: 0.95em;
  box-shadow: var(--shadow);
  display: block;
  overflow-x: auto;
}
th, td {
  border: 1px solid var(--border);
  padding: 8px 12px;
  text-align: left;
  vertical-align: top;
}
th { background: var(--accent-soft); font-weight: 600; }
tr:nth-child(even) td { background: var(--table-stripe); }

/* 코드·인용 */
code {
  background: var(--code-bg);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.9em;
  font-family: "SF Mono", Menlo, Consolas, monospace;
}
pre {
  background: var(--code-bg);
  padding: 16px;
  border-radius: 8px;
  overflow-x: auto;
  border: 1px solid var(--border);
}
pre code { background: none; padding: 0; }
blockquote {
  margin: 1em 0;
  padding: 12px 18px;
  border-left: 4px solid var(--quote-border);
  background: var(--quote-bg);
  border-radius: 4px;
}
blockquote p { margin: 0.3em 0; }

/* Mermaid 컨테이너 */
pre.mermaid {
  background: var(--bg);
  border: 1px solid var(--border);
  text-align: center;
  padding: 24px;
}

/* 컨트롤 (다크모드 토글 + 인쇄 + 글자크기) */
#controls {
  position: fixed;
  top: 16px;
  right: 24px;
  display: flex;
  gap: 8px;
  z-index: 200;
}
#controls button {
  background: var(--bg);
  color: var(--fg);
  border: 1px solid var(--border);
  padding: 8px 14px;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  box-shadow: var(--shadow);
  font-family: inherit;
}
#controls button:hover { background: var(--accent-soft); border-color: var(--accent); }

/* 모바일 사이드바 토글 */
#menu-toggle {
  display: none;
  position: fixed;
  top: 16px;
  left: 16px;
  z-index: 200;
  background: var(--accent);
  color: white;
  border: none;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  box-shadow: var(--shadow);
}

/* 모바일 반응형 */
@media (max-width: 900px) {
  body { display: block; }
  #sidebar {
    position: fixed;
    left: -100%;
    width: 280px;
    transition: left 0.25s;
    box-shadow: 4px 0 20px rgba(0,0,0,0.15);
  }
  #sidebar.open { left: 0; }
  main { max-width: 100%; padding: 64px 20px 64px; }
  #menu-toggle { display: block; }
  #controls { top: 16px; right: 16px; }
  #controls button { padding: 8px 10px; font-size: 13px; }
  table { font-size: 0.88em; }
  h1 { font-size: 1.6em; }
  h2 { font-size: 1.3em; }
}

/* 인쇄 */
@media print {
  body { display: block; }
  #sidebar, #controls, #menu-toggle { display: none; }
  main { max-width: 100%; padding: 0; }
  a { color: inherit; text-decoration: none; }
  pre, blockquote, table { break-inside: avoid; }
  h1, h2, h3 { break-after: avoid; }
  pre.mermaid { border: none; }
}

/* 글자 크기 토글 */
body[data-fontsize="large"] { font-size: 18px; }
body[data-fontsize="xlarge"] { font-size: 20px; }

/* 부드러운 진입 */
main > * { animation: fadeIn 0.3s ease-out; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: translateY(0); } }
</style>
</head>
<body data-theme="light" data-fontsize="normal">

<button id="menu-toggle" onclick="document.getElementById('sidebar').classList.toggle('open')">☰ 목차</button>

<div id="controls">
  <button onclick="toggleTheme()">🌓 다크모드</button>
  <button onclick="cycleFont()">Aa 글자</button>
  <button onclick="window.print()">🖨 인쇄/PDF</button>
</div>

<aside id="sidebar">
  <h2>📑 목차</h2>
  __TOC__
</aside>

<main>
__BODY__
</main>

<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
mermaid.initialize({
  startOnLoad: true,
  theme: document.body.dataset.theme === "dark" ? "dark" : "default",
  flowchart: { useMaxWidth: true, htmlLabels: true }
});

function toggleTheme() {
  const body = document.body;
  const next = body.dataset.theme === "light" ? "dark" : "light";
  body.dataset.theme = next;
  localStorage.setItem("theme", next);
  // mermaid 재렌더링
  document.querySelectorAll("pre.mermaid").forEach(el => {
    if (!el.dataset.original) el.dataset.original = el.textContent;
    el.removeAttribute("data-processed");
    el.innerHTML = el.dataset.original;
  });
  mermaid.initialize({ startOnLoad: false, theme: next === "dark" ? "dark" : "default" });
  mermaid.run();
}
function cycleFont() {
  const order = ["normal", "large", "xlarge"];
  const cur = document.body.dataset.fontsize;
  const next = order[(order.indexOf(cur) + 1) % order.length];
  document.body.dataset.fontsize = next;
  localStorage.setItem("fontsize", next);
}
// 복원
(function() {
  const t = localStorage.getItem("theme");
  if (t) document.body.dataset.theme = t;
  const f = localStorage.getItem("fontsize");
  if (f) document.body.dataset.fontsize = f;
})();
// 모바일에서 링크 클릭 시 사이드바 닫기
document.querySelectorAll("#sidebar a").forEach(a => {
  a.addEventListener("click", () => {
    if (window.innerWidth <= 900) document.getElementById("sidebar").classList.remove("open");
  });
});
</script>
</body>
</html>
"""

final = template.replace("__TOC__", toc_html).replace("__BODY__", body_no_toc)

output = base / "고소의_기술_통합정리집.html"
output.write_text(final)
print(f"✅ 빌드 완료: {output}")
print(f"   크기: {output.stat().st_size:,} bytes ({output.stat().st_size/1024:.1f} KB)")
