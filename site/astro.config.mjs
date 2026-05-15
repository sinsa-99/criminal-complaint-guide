// @ts-check
import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";
import remarkMermaidPre from "./remark-mermaid-pre.mjs";

// GitHub Pages: https://sinsa-99.github.io/criminal-complaint-guide/
const SITE = "https://sinsa-99.github.io";
const BASE = "/criminal-complaint-guide";

export default defineConfig({
  site: SITE,
  base: BASE,
  trailingSlash: "always",
  markdown: {
    remarkPlugins: [remarkMermaidPre],
  },
  integrations: [
    starlight({
      title: "고소·피소 가이드",
      description:
        "한국 형사절차 학습 자료 — 고소하는 쪽과 고소당한 쪽 양면. 용어·플로우·죄목·고소장·판례·22건 실전 스토리·피의자 방어.",
      defaultLocale: "root",
      locales: {
        root: { label: "한국어", lang: "ko" },
      },
      components: {
        // SocialIcons 슬롯을 글자크기 버튼으로 교체 (다크모드 토글 옆에 위치)
        SocialIcons: "./src/components/FontSizeControls.astro",
      },
      head: [
        // Mermaid 클라이언트 렌더링
        {
          tag: "script",
          attrs: { type: "module" },
          content: `
import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
function applyTheme() {
  const dark = document.documentElement.dataset.theme === "dark";
  mermaid.initialize({
    startOnLoad: true,
    theme: dark ? "dark" : "default",
    securityLevel: "loose",
    fontFamily: "inherit",
  });
}
applyTheme();
new MutationObserver(() => {
  document.querySelectorAll(".mermaid").forEach((el) => {
    if (el.dataset.processed === "true") {
      el.removeAttribute("data-processed");
      el.innerHTML = el.dataset.source ?? el.innerHTML;
    }
  });
  applyTheme();
  mermaid.run();
}).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
          `.trim(),
        },
      ],
      customCss: ["./src/styles/custom.css"],
      sidebar: [
        { label: "📖 시작하기", link: "/" },
        {
          label: "1. 기초",
          items: [
            { label: "절차 플로우차트", link: "/procedure/" },
            { label: "핵심 용어 사전", link: "/glossary/" },
          ],
        },
        {
          label: "2. 고소하기",
          items: [
            { label: "상황별 죄목·법조", link: "/charges/" },
            { label: "고소장 작성법", link: "/writing/" },
            { label: "고소장 완성본 + 체크리스트", link: "/tips/" },
          ],
        },
        {
          label: "3. 실전 스토리",
          items: [
            { label: "스토리 종합본 (1건 깊이)", link: "/story-overview/" },
            { label: "7가지 실전 상황", link: "/scenarios-7/" },
            { label: "22건 스토리집", link: "/stories-22/" },
            { label: "주요 판례집", link: "/cases/" },
          ],
        },
        {
          label: "4. 반대편 입장",
          items: [{ label: "피의자 방어 매뉴얼", link: "/defense/" }],
        },
        {
          label: "부록",
          items: [{ label: "페이지 인덱스", link: "/page-index/" }],
        },
      ],
    }),
  ],
});
