/**
 * remark plugin: ```mermaid``` 코드 펜스 → <pre class="mermaid"> HTML 노드로 치환.
 * 클라이언트 측 mermaid.min.js가 .mermaid 요소를 자동 렌더링.
 */
import { visit } from "unist-util-visit";

export default function remarkMermaidPre() {
  return (tree) => {
    visit(tree, "code", (node) => {
      if (node.lang !== "mermaid") return;
      const escaped = node.value
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
      node.type = "html";
      node.value = `<pre class="mermaid">${escaped}</pre>`;
      delete node.lang;
      delete node.meta;
    });
  };
}
