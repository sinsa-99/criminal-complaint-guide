# 고소·피소 가이드

> 한국 형사절차 학습용 자료 패키지. 고소하는 쪽과 고소당한 쪽 양면. 용어 사전 → 절차 그래프 → 죄목 매칭 → 고소장 작성법 → 피의자 방어 → 22개 실전 상황 → 심화 팁 → 실제 판례까지.

📖 **라이브 보기**: https://sinsa-99.github.io/criminal-complaint-guide/

by Kim Donghyeon

---

## ✨ 특징

- 🌳 **Mermaid 절차 그래프** + 단계별 누적 시간 표
- ⚖️ **법제처 Open API** 조회 결과 기반 법령 조문 (형법·정통망법·스토킹법 등 15개+)
- 📚 **대법원·고등법원 실제 판례** (사건번호·핵심 쟁점)
- 🎭 **22개 실전 상황** 시나리오 (모두 가상·가명)
- 📋 **실전 고소장 완성본** + **변호사 상담 10분 체크리스트**
- 🛡 **피의자 방어 8단계 매뉴얼** (고소당했을 때)
- 🔍 **풀텍스트 검색** (Pagefind) · 🌓 다크모드 · 글자크기 조정 · 반응형

---

## 📁 파일 구성

| 항목 | 내용 |
|---|---|
| `00_README.md` ~ `11_고소당했을때_대처법.md` | 원본 학습 자료 (md 12개) |
| `site/` | **Astro Starlight** 빌드 프로젝트 (실제 사이트 생성처) |
| `site/src/content/docs/*.md` | 사이트에 렌더되는 md (frontmatter 입혀진 사본) |
| `site/astro.config.mjs` | 사이드바·테마·Mermaid 등 설정 |
| `site/src/components/FontSizeControls.astro` | 헤더 글자크기 +/- 버튼 |
| `.github/workflows/deploy.yml` | push → GitHub Pages 자동 배포 |
| `_legacy/` | 이전 Pandoc 기반 단일 HTML 빌드 산출물 (보존용) |

---

## 🚀 사용법

### 1. 웹에서 바로 보기
[Live Site](https://sinsa-99.github.io/criminal-complaint-guide/)

### 2. 로컬에서 미리보기
```bash
cd site
npm install   # 처음 한 번만
npm run dev   # http://localhost:4321/criminal-complaint-guide/
```

### 3. 빌드 (배포 산출물 생성)
```bash
cd site
npm run build   # → site/dist/
```

### 4. 자료 수정 후 배포
1. `site/src/content/docs/*.md` 수정 (또는 원본 `*.md` 수정 후 다시 옮김)
2. `git commit && git push`
3. GitHub Actions가 자동으로 빌드 & 배포

---

## 📞 무료 법률상담 채널

- 대한법률구조공단: **132**
- 여성긴급전화: **1366**
- 사이버수사대: **117**
- 금감원 보이스피싱: **1332**
- 디지털성범죄피해자지원센터: **02-735-8994**
- 층간소음이웃사이센터: **1661-2642**
- 노동부: **1350**
- 개인정보침해 신고센터: **118**

---

## ⚠️ 주의사항

- 일반 학습·참고용 자료입니다. 실제 사건 처리 시 반드시 **변호사와 상담**하세요.
- 법령·판례는 **2026년 5월 기준** (이후 개정 가능, 최신 법령은 법제처 [law.go.kr](https://law.go.kr) 확인).
- 모든 사례·인물은 **가상·가명**이며 실존 인물·사건과 무관합니다.
- 정리물은 **변환된 학습자료**로, 어떤 책의 원문도 그대로 포함하지 않습니다.

---

## 📜 License

개인 학습·교육 목적 자유 사용. 상업적 이용 시 별도 문의.
