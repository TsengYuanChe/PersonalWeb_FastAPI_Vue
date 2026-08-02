# adamtseng.com 專案現況總覽

> 更新日期：2026-08-01
> 盤點基準：repository 當前實際程式碼，而非 README、舊架構文件或先前版本。
> 目的：讓未讀過程式碼的工程師快速理解網站定位、資訊架構、資料流、部署方式與大改版風險。

## 0. 閱讀標記

- **【程式碼事實】**：可由目前 repository 的程式碼、設定或資料直接確認。
- **【推測／建議】**：由現有實作推導，仍需產品負責人或外部環境確認。
- 本文件不記錄任何 secret、憑證或密碼實際內容。

## 1. 網站定位與目前功能

### 1.1 產品定位

**【程式碼事實】** 這是一個以 Adam Tseng 為主體的英文個人軟體工程作品集，內容聚焦：

- Software Engineer 身份與完整產品交付能力。
- Full-stack、backend API、database、data processing、CI/CD 與 deployment 經驗。
- 工作與學術 Journey。
- 工程專案、架構、trade-offs 與未來方向。
- Resume 與 GitHub、LinkedIn 等外部入口。

**【產品規格】** 本網站的主要用途是 **Software Engineer Portfolio**，主要受眾為 Recruiter、Engineering Manager 與技術面試官。Freelance 僅為次要用途，因此首頁優先呈現工程能力、工作／學術歷程與代表作品，而不是服務項目、報價或接案型 landing page。

### 1.2 使用者可見功能

**【程式碼事實】** 網站目前有四個前端 route：

1. `/`：首頁 Preview，包含 Profile、Journey、Projects。
2. `/about`：About 詳細頁架構，目前六個 section 都是 `Coming soon.`。
3. `/experience`：完整 Journey，從 FastAPI 載入。
4. `/project`：完整 Projects，從 FastAPI 載入。

首頁另提供：

- 固定 Sidebar 身份資訊與 hash navigation。
- GitHub、LinkedIn、Instagram、Facebook、Resume links。
- Last updated 日期。
- Desktop cursor glow 與首頁內層 smooth scrolling。

## 2. 系統架構

```text
Browser
  │
  ├─ HTML / JS / CSS / public assets
  ▼
Cloud Run: vue-frontend
Nginx :8080
  ├─ serves Vite build output
  └─ try_files $uri /index.html（SPA history fallback）

Browser（詳細頁與 Last updated）
  │ fetch，base URL 由 VITE_API_BASE 在 build time 注入
  ▼
Cloud Run: fastapi-backend
Uvicorn :8080 → FastAPI
  │ router → service → repository
  ▼
backend/data/**/*.json
```

**【程式碼事實】** 前後端是兩個獨立 container、兩個 Cloud Run service、兩個 GitHub Actions workflow。沒有 application database、ORM、migration、authentication 或寫入 API。

## 3. 技術棧與重要套件

### 3.1 Frontend

| 技術／套件 | 版本 | 用途 | 位置 |
|---|---:|---|---|
| Vue | `^3.5.18` | Composition API 與 component rendering | `frontend/src/` |
| Vue Router | `^4.5.1` | history-mode 四個 routes、route meta layout | `frontend/src/router/index.js` |
| Vite | `^7.0.6` | dev server、production build | `frontend/vite.config.js` |
| Bootstrap | `^5.3.7` | spacing、flex、typography utilities | `frontend/src/main.js`、templates |
| Bootstrap Icons | `^1.13.1` | social、status、external action icons | App 與詳細頁元件 |
| Fetch API | Browser built-in | FastAPI client | `frontend/src/api/client.js` |
| Axios | `^1.11.0` | **目前未被任何程式 import** | `frontend/package.json` |
| ESLint | `^9.31.0` | JS/Vue lint | `frontend/eslint.config.js` |
| Prettier | `3.6.2` | `src/` formatting | `.prettierrc.json` |
| Vue DevTools plugin | `^8.0.0` | Vite devtools plugin；未依 mode 關閉 | `frontend/vite.config.js` |

**【程式碼事實】** 專案是 JavaScript，不是 TypeScript；只有 `jsconfig.json` alias 設定，沒有 `tsconfig` 或 project types。

### 3.2 Backend

| 技術 | 版本 | 用途 |
|---|---:|---|
| Python image | `3.13.9` | container runtime |
| FastAPI | `0.122.0` | HTTP API、OpenAPI、exception handlers、CORS |
| Uvicorn | `0.38.0` | ASGI server |
| Pydantic | `2.12.5` | v1 response validation 與 content validation script |
| Starlette | `0.50.0` | FastAPI foundation / HTTP exceptions |
| python-multipart | `0.0.20` | 已安裝，但目前沒有 upload/form endpoint |

## 4. 目錄結構

```text
PersonalWeb_Flask_Vue/
├── .github/workflows/
│   ├── frontend-deploy.yml        # Build/push/deploy Vue container
│   └── backend-deploy.yml         # Validate JSON + build/push/deploy FastAPI
├── backend/
│   ├── main.py                    # FastAPI app、CORS、全域 error envelope
│   ├── routers/v1/
│   │   ├── content.py             # legacy + v1 content endpoints
│   │   └── health.py              # /health
│   ├── services/content_service.py
│   ├── repositories/content_repository.py
│   ├── schemas/
│   │   ├── common.py              # Meta / ApiResponse
│   │   └── content.py             # About / Experience / Project models
│   ├── data/
│   │   └── portfolio/              # 依 Portfolio page 分組的 backend content
│   │       ├── about/about.json
│   │       ├── experience/         # 每段完整 Journey 各一份 slug JSON
│   │       │   ├── ezoom.json
│   │       │   ├── nycu-master.json
│   │       │   └── nchu-bachelor.json
│   │       ├── timeline/events.json # Journey Timeline 的非 Experience 事件
│   │       └── projects/           # 每個完整 Project 各一份 slug JSON
│   │           ├── mris.json
│   │           ├── personal-portfolio.json
│   │           └── mamatoya.json
│   ├── scripts/validate_content_schema.py
│   ├── core/config.py             # placeholder
│   ├── core/logging.py            # placeholder
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── main.js                # App bootstrap、CSS import order
│   │   ├── App.vue                # route-aware Home/Detail shell
│   │   ├── router/index.js        # 四個 routes 與 scrollBehavior
│   │   ├── views/
│   │   │   ├── HomeView.vue
│   │   │   ├── AboutView.vue
│   │   │   ├── ExperienceView.vue
│   │   │   └── ProjectView.vue
│   │   ├── components/
│   │   │   ├── layout/DetailPageHeader.vue
│   │   │   ├── experience/{HomeJourneyItem,JourneySection,JourneyDetail,Timeline}.vue
│   │   │   └── projects/{ProjectCover,ProjectAction,HomeProjectPreview,ProjectCard}.vue
│   │   ├── data/home/             # 首頁三份 local Preview JSON
│   │   ├── api/
│   │   │   ├── client.js          # fetch wrapper / error normalization
│   │   │   └── contentApi.js      # About / Experience / Projects service functions
│   │   ├── composables/           # mouse、scroll、project helpers
│   │   ├── utils/experienceLogos.js
│   │   └── assets/
│   │       ├── css/               # global + feature + RWD CSS
│   │       └── images/exp/         # 經歷 logo
│   ├── public/
│   │   ├── files/Adam_Tseng_Resume.pdf
│   │   └── favicon files
│   ├── index.html
│   ├── vite.config.js
│   ├── nginx.conf
│   ├── package.json / package-lock.json
│   ├── .env.development / .env.production
│   └── Dockerfile
├── AGENTS.md                       # agent 與 recruiter-first 產品方向
├── ARCHITECTURE*.md / FEATURES*.md / SYSTEM_DESIGN*.md
├── TODO.md / TODO_Layout.md / RWD_LAYOUT.md
└── overview.md
```

**Types／Services 現況：**

- Frontend 沒有 `src/types/`、TypeScript interface 或 TypeScript service；資料 shape 由 JSON、Vue runtime props 與使用端條件判斷共同約束。
- Frontend service layer 是 `src/api/client.js` 與 `src/api/contentApi.js`。
- Backend service layer 是 `backend/services/content_service.py`，並由 `repositories/content_repository.py` 讀取 JSON。

## 5. Routes、Layout 與頁面資料流

### 5.1 Router

定義於 `frontend/src/router/index.js`：

| URL | name | meta.layout | View |
|---|---|---|---|
| `/` | `home` | `home` | `HomeView.vue` |
| `/about` | `about` | `detail` | `AboutView.vue` |
| `/experience` | `experience` | `detail` | `ExperienceView.vue` |
| `/project` | `project` | `detail` | `ProjectView.vue` |

`createWebHistory(import.meta.env.BASE_URL)` 配合 Nginx `try_files $uri /index.html`，因此部署後直接開啟或重新整理 route 可回到 SPA。Router `scrollBehavior()` 對 route change 回傳 `{ top: 0 }`。目前沒有 catch-all 404 route。

### 5.2 Application shell

`frontend/src/App.vue` 以 `route.meta.layout` 決定版型：

- `home`：顯示 Sidebar、內層可捲動 `.main-content`、Desktop social area、Mobile footer。
- `detail`：不 render Sidebar/footer，使用 full-width `.detail-main` 與一般 document scrolling。
- `<RouterView />` 是所有頁面的 render outlet。

`useScrollProxy()` 只在 `.layout-container--home` 存在時攔截 wheel 並轉送給 `.main-content`。`useMouseGlow()` 仍在 App 全域啟用，Mobile 由 CSS 隱藏。

### 5.3 首頁設計原則

- Homepage 只提供可在短時間內掃讀的 Preview，完整內容放在 Detail Pages。
- Readability 與 recruiter scanning 優先於視覺裝飾。
- 首頁避免大型 card、大面積背景、陰影與不必要動畫。
- Journey 與 Projects 使用一致的低裝飾 list-style rows、內容間距與淡分隔線。
- 首頁保持精簡，避免完整履歷、完整專案工程細節或長篇個人故事造成資訊過載。
- 首頁主要展示 Software Engineer 定位、核心工程能力、工作／學習 Journey 與代表作品。
- About、Journey、Projects 的完整資訊分別由 `/about`、`/experience`、`/project` 承接。

## 6. 各頁面與主要元件

### 6.1 `/` Home

位置：`frontend/src/views/HomeView.vue`

| Section | 元件 | 資料來源 | Backend dependency |
|---|---|---|---|
| Profile (`#about`) | HomeView template | `src/data/home/about.json` | 內容不依賴 API |
| Journey (`#experiences`) | `HomeJourneyItem.vue` | `src/data/home/experiences.json` | 不依賴 API |
| Projects (`#projects`) | `HomeProjectPreview.vue` | `src/data/home/projects.json` | 不依賴 API |
| Last updated | App Sidebar/footer | `GET /api/v1/about` 的 `meta.updated_at` | **依賴 API** |

Sidebar navigation 使用 Vue Router hash links回到首頁的 `#about`、`#experiences`、`#projects`。`App.vue` 以 imperative `scrollTo()` 對齊相同頂部空間。

Profile、Journey、Projects Preview 使用 frontend local JSON，目的是避免 Cloud Run backend cold start 阻塞首頁主要內容。首頁仍會為 Last updated 呼叫 About API，但該請求失敗時只顯示 `—`，不會阻止三個 Preview sections render。

#### Profile Preview

- 兩段本地文字，template 仍使用 `v-html` 包裝 paragraph。
- `View more about me →` 前往 `/about`。

#### Journey Preview

- 三筆本地資料：logo、position、name、duration、short description。
- Desktop 為 92px logo + content row；Mobile 為 60px logo + content。
- `View full journey →` 前往 `/experience`。

#### Projects Preview

- 三筆本地資料，首頁專用 component，不共用詳細頁 card。
- Schema：`name`、`image`、`image_alt`、`image_ready`、`introduction`、`tags`；`website_url`、`source_url` 為選填。
- `image_ready: false` 時不建立 `<img>` request，顯示 `Coming soon`；true 時載入 `/images/projects/covers/*.webp`，error 時回退 placeholder。
- Desktop 為 160px 16:10 media + content row；≤1024px 改單欄。
- `View all projects →` 前往 `/project`。

### 6.2 `/about`

位置：`frontend/src/views/AboutView.vue`

- Full-width detail shell，外層 container 最大 1200px。
- Breadcrumb：`HOME > ABOUT`。
- Header：`About Me` + 一行 description。
- 正文最大寬度 880px。
- Sections：Introduction、What I Do、Current Role、Engineering Approach、Technical Background、Current Focus。
- 每個 section 目前僅顯示 `Coming soon.`。
- **目前不呼叫 About API**；後端已提供保留 legacy `paragraphs` 並新增 `sections[{id,title,paragraphs,items}]` 的可擴充 contract，前端串接留待下一階段。

### 6.3 `/experience`

位置：`frontend/src/views/ExperienceView.vue`

- Breadcrumb：`HOME > JOURNEY`，主標題 `Journey`。
- mount 後呼叫 `GET /api/v1/experience`。
- 提供 loading、error、empty、success 四種狀態。
- `JourneySection.vue` 完全由 backend Experience object 建立，且只負責永遠顯示的 Summary Header：logo、title、organization、summary、role、period 與 More／Less Detail toggle。
- `JourneyDetail.vue` 負責 Description、Responsibilities、Highlights、Projects、Skills／Technologies 與 Additional Details；空欄位不 render 標題或容器。
- Journey Sections 預設全部收合；展開狀態由 `ExperienceView.vue` 以單一 `expandedExperienceSlug` 管理，因此同一時間最多只有一段展開。整個 Summary Header 可點擊，More/Less Detail button 提供鍵盤操作、`aria-expanded` 與 `aria-controls`。
- Detail 使用與 Project Card 一致的 Vue `Transition` hooks，依實際 `scrollHeight` 執行 320ms 高度、透明度與輕微位移動畫，完成後恢復 `height: auto`，並支援 `prefers-reduced-motion`。
- 每段 Experience 來自 `backend/data/portfolio/experience/` 下的獨立 slug JSON，由 repository 動態掃描並依 `start_date` 新到舊排序；新增經歷不需修改既有 JSON。
- Logo filename 經 `utils/experienceLogos.js` 映射到 Vite-imported assets。
- Timeline 第一版由獨立 `Timeline.vue` 實作，不屬於 `JourneySection.vue`。它依 API Experience 的 `start_date`／`end_date` 自動建立 nodes，並以單一連續垂直線串接；新增 Experience JSON 時會跟隨 API list 自動增加。
- `ExperienceView.vue` 同時管理 `expandedExperienceSlug` 與 hover 用的 `activeExperienceSlug`，負責同步 Section 與 Timeline node；`JourneySection.vue` 不知道 Timeline 的存在。
- Timeline period 與 Journey Sections 由 `ExperienceView.vue` 放入對應的 CSS Grid header rows；收合狀態下，每段 Timeline 的上下 node 由 row 實際高度對齊對應 Section 的上下邊界。
- 展開時 `ExperienceView.vue` 在 Header 後插入獨立的 Journey Detail row；Detail 左側沒有 Timeline period，上一段 segment 高度保持不變，後續 Timeline 與 Section 一起下移，收合完成後恢復原位。同一時間仍只有一段正式展開。
- Timeline base segment 以每個 Header row 為單位，收合時由 connector 串接相鄰 periods；Detail row 存在時對應 connector 暫停，因此主線不穿越不具時間語意的 Detail。
- Timeline Events 來自獨立的 `timeline-events.json` 與 API，不屬於 Experience、Section 或 Detail。第一版支援單節點 Point Event 與雙節點／segment Duration Event，由 `Timeline.vue` 依年月在既有 Experience period 內換算位置並統一 render。
- Timeline Events 第一版只有靜態 label、node 與 duration segment，沒有 hover、highlight、animation、focus 或 click interaction；不會建立額外 Timeline column 或改變 Experience rows。
- Timeline 不再以 Desktop `160px`／Tablet `150px` 固定 period height 推算位置。Desktop 顯示於 Sections 左側、Tablet 縮小、Mobile（≤768px）暫時隱藏。
- Journey 詳細頁採用 **Timeline + Sections**，不沿用 Project Page 的 Card design language。每段 Journey 以極低對比 surface 輔助閱讀，移除外框、陰影、浮起與 hover border，主要透過 spacing 與淡 divider 區隔；Timeline 是頁面的主要視覺結構。
- Hover 或 keyboard focus Journey Section，以及 hover 或 focus 該 period 任一 Timeline node 時，`ExperienceView.vue` 以同一個 `activeExperienceSlug` 同步高亮上下 nodes 與中間 period segment。Timeline 保留完整低對比 base line，active segment 只覆蓋 Experience row，Experience 間的 connector gap 不高亮。
- Segment interaction 只有 220ms 顏色與克制 glow transition，支援 `prefers-reduced-motion`；目前沒有掃光、stretch、scroll animation 或與 expanded state 同步。
- 目前是詳細頁初版：分檔資料、完整 API、單段收合／展開與 Timeline Prototype 已接通，但內容校稿、Timeline 動態 segment 與更完整的可用性驗證仍待後續處理。

#### Timeline Events — Future Considerations

目前保留第一版的最簡單實作，以下特殊情況尚未提前實作，待後續另行設計最佳視覺方案：

1. **Cross-section Duration Event**：例如 Freelance 從 `2024-01` 延續至 `2025-10`，跨越多個 Experience Sections。未來需定義 segment 如何跨越 periods、Journey Detail 展開時如何切割，並確保線段不穿過 Detail row。
2. **Event 與 Experience 邊界重疊**：例如 Military start 與 Software Engineer start 同為 `2025-07`，或 Event end 與 Master end 同為 `2024-12`。未來需評估 nodes 是否重疊、labels 如何避碰、是否合併 node 或使用小幅偏移，同時維持 Timeline 可讀性。

### 6.4 `/project`

位置：`frontend/src/views/ProjectView.vue`

- Breadcrumb：`HOME > PROJECTS`，主標題 `Projects`。
- mount 後呼叫 `GET /api/v1/projects`。
- 提供 loading、error、empty、success 四種狀態。
- 顯示 API 回傳的所有 projects，沒有首頁三筆限制。
- `ProjectCard.vue` 完全由 backend Project object 建立，摘要使用 cover、title、subtitle、category、summary、role、period、technologies 與 action/status；詳細內容使用同一物件的 overview、responsibilities、architecture、challenges、deployment 與 lessons learned。
- Action 依序判斷 `website_url`、`source_url`；兩者皆無時顯示不可點擊的 `🔒 Internal`。這個判斷與首頁共用 `ProjectAction.vue`，不依賴 `status` 決定連結文字。
- `showcase` 目前保留在資料 contract 中但三個專案皆為空陣列，因此頁面不 render Showcase 標題或空容器。
- Project Card 預設全部收合並永遠顯示 Summary Header；Overview 起的 detail sections 只有展開時才 render。
- Summary Header 可用滑鼠點擊切換，Meta 中的語意化 More/Less Detail button 提供鍵盤操作、`aria-expanded` 與 `aria-controls`。Live／Source links 不觸發 toggle。
- 展開狀態由 `ProjectView.vue` 以單一 `expandedProjectSlug` 管理，因此同一時間最多只有一個 Project 展開；狀態不寫入 URL 或 localStorage。
- Detail 使用 Vue `Transition` hooks 依實際 `scrollHeight` 執行 320ms 高度、透明度與輕微位移動畫，完成後恢復 `height: auto`，並支援 `prefers-reduced-motion`。
- `/project` 的 Search、Category 與 Technology filters 都是純前端 computed 行為，只處理首次 API response，不會因條件變更重新呼叫 backend。Search 對 summary 與 detail 的公開文字做不分大小寫的完整 token 比對，不使用任意 substring；多個搜尋詞採 AND 邏輯。
- Category 與 Technology options 分別由 API projects 的 `category` 與 `technologies` 動態去重、排序產生，並以完整值比對；Search、Category、Technology 三者亦採 AND 邏輯且保留 backend 原始排序。
- 若已展開 Project 被條件排除，`expandedProjectSlug` 會清除。搜尋／篩選沒有使用 server-side parameters、URL query、localStorage 或 visibility fields。
- Search／Filter 使用直接置於頁面背景的輕量工具列，不使用外層 Card 容器。Desktop 依序排列 Category、Technology、彈性空間／Clear filters 與右側克制寬度的 Search；Tablet、Mobile 依既有 `1024px`、`768px` breakpoint 重排。
- Field 的可見標題已移除，但原生 label 仍以 visually hidden 方式保留。欄位視覺目前由 Projects feature 的 `projects.css` 與 `projects-rwd.css` 管理，尚未抽成全域表單系統。
- 詳細頁仍使用既有大型 card 視覺；首頁 Preview styles 使用 `.home-project-*` namespace，不會覆蓋它。
- 目前是詳細頁初版：完整 backend narrative、基本狀態與單卡收合／展開已接通，但 Showcase、圖片／架構圖與進一步 layout 整理仍待完成。

## 7. 共用 UI、Navigation、Footer

### 7.1 共用元件

- `DetailPageHeader.vue`：三個詳細頁共用 Breadcrumb、唯一 `h1` 與 description。
- `HomeJourneyItem.vue` / `JourneySection.vue` / `JourneyDetail.vue`：首頁 Preview、詳細頁 Summary Header 與展開 Detail 分離。
- `Timeline.vue`：詳細 Journey 專用的 data-driven Timeline Prototype；只 render line/nodes 並 emit hover/focus state，不包含 Section 或展開邏輯。
- `ProjectCover.vue`：首頁與詳細 Projects 共用的 160×100、16:10 cover／placeholder。
- `ProjectAction.vue`：首頁與詳細 Projects 共用 Live／Source／Internal 判斷與外部連結語意。
- `HomeProjectPreview.vue` / `ProjectCard.vue`：首頁與詳細 Projects 分離，並共用 `ProjectCover.vue`。
- Sidebar：不是獨立 component，markup 位於 `App.vue`，並由 `v-if="isHomeLayout"` 控制。
- Home/Detail Layout：沒有獨立 `HomeLayout.vue` 或 `DetailLayout.vue`；`App.vue` 依 route meta 條件渲染，搭配 `.layout-container--home`、`.layout-container--detail`、`.detail-main` 與 `.detail-page-container`。
- Breadcrumb：不是單獨的 `Breadcrumb.vue`，而是 `DetailPageHeader.vue` 的一部分。
- Shared Section Header：首頁三個 sections 共用 `.section-heading` 與 `.home-journey-link` CSS pattern，但沒有獨立 Vue component。

### 7.2 Sidebar 與 social links

**【程式碼事實】** Sidebar 只出現在首頁：

- Adam Tseng、Software Engineer、定位短句。
- Home、Journey、Projects hash navigation。
- GitHub、LinkedIn、Instagram、Facebook、Resume。
- Last updated。

Desktop social links 位於 Sidebar 底部；Mobile 則以 App template 中的 fixed `.mobile-footer` 顯示。詳細頁沒有 Sidebar、social links 或一般 Footer。

## 8. CSS、視覺系統與 RWD

### 8.1 CSS 載入順序

`frontend/src/main.js` 在 Bootstrap / Bootstrap Icons 後依序載入：

1. `main.css`
2. `main-rwd.css`
3. `projects.css`
4. `projects-rwd.css`
5. `about.css`
6. `about-rwd.css`
7. `exp.css`
8. `exp-rwd.css`

全部是 global CSS；沒有 scoped styles、CSS Modules 或 Sass。Cascade 與 import order 是實際 design system 的一部分。

### 8.2 核心 tokens 與 typography

`main.css :root`：

| Token | 值 | 用途 |
|---|---|---|
| `--site-bg` | `#0c1a2b` | 深藍背景 |
| `--site-text` | `#e4e9f0` | 主要文字 |
| `--site-secondary` | `#8fa3bd` | 次要文字 |
| `--layout-max-width` | `1300px` | 首頁 shell 最大寬度 |
| `--sidebar-min-width` | `300px` | 首頁 Sidebar 下限 |
| `--main-inline-padding` | `90px` | Desktop 首頁內容左右 padding |

沒有自訂 web font；實際使用 Bootstrap/system font stack。Accent 主要為 `#9bbcff`、`#4da4ff` 與 Bootstrap info colors，但尚未全部 token 化。

### 8.3 Layout 與 breakpoints

#### Large Desktop

- 首頁 Grid：`minmax(300px, 27fr) minmax(0, 73fr)`。
- shell 最大 1300px；右側 `.main-content` 最大 1000px。
- Sidebar sticky、main 為 100vh 內層 scroll。
- 詳細頁不使用 Grid，container 最大 1200px；About 正文最大 880px。

#### ≤1024px

- 首頁仍維持雙欄；Sidebar 最小 300px，padding 收窄。
- 首頁 Projects Preview 切換為單欄。
- 詳細頁 padding 為 `44px 36px 60px`。

#### ≤768px

- 首頁 Grid 改 block。
- Sidebar 變 fixed mobile header；social/updated date 變 fixed mobile footer。
- main 高度由 `--real-vh - --header-height - --footer-height` 計算並內層捲動。
- 詳細頁覆寫為一般 auto-height document flow，不顯示 Sidebar/footer。
- 詳細頁 padding 為 `28px 20px 48px`。
- cursor glow 隱藏。

### 8.4 Motion

- Navigation、social icons、詳細卡片與 tags 仍有 hover transform/transition。
- 首頁 Journey/Projects links 只有輕微箭頭位移，並處理 `prefers-reduced-motion`。
- 首頁 Journey/Projects rows 本身沒有 card hover 上浮。
- cursor glow 是 400×400 radial gradient，mousemove 時直接寫入 transform。

## 9. 資料與靜態資產

| 類型 | 位置 | 使用者 |
|---|---|---|
| 首頁 About Preview | `frontend/src/data/home/about.json` | HomeView |
| 首頁 Journey Preview | `frontend/src/data/home/experiences.json` | HomeJourneyItem |
| 首頁 Projects Preview | `frontend/src/data/home/projects.json` | HomeProjectPreview |
| 完整 About JSON | `backend/data/portfolio/about/about.json` | About API；目前頁面內容未使用 |
| 完整 Experience JSON | `backend/data/portfolio/experience/{ezoom,nycu-master,nchu-bachelor}.json` | Experience API/detail page |
| Timeline Events JSON | `backend/data/portfolio/timeline/events.json` | Timeline Events API／Timeline.vue |
| 完整 Projects JSON | `backend/data/portfolio/projects/{mris,personal-portfolio,mamatoya}.json` | Projects API/detail page |
| Experience logos | `frontend/src/assets/images/exp/*.png` | Vite asset imports |
| Future project screenshots | 預定 `frontend/public/images/projects/covers/*.webp` | 目前檔案尚不存在 |
| Resume | `frontend/public/files/Adam_Tseng_Resume.pdf` | 首頁 social area |
| Favicons | `frontend/public/favicon*` | `index.html` |

### 9.1 Project Cover Specification

#### Aspect Ratio

- `16:10`（`8:5`）。

#### Display Size

- 由共用 CSS variables 控制；不要將 pixel 顯示尺寸 hardcode 到 image assets 或個別 components。

#### Recommended Export Resolution

- `1280 × 800 px`，格式使用 `.webp`。

#### Rendering

- Real images 使用 `object-fit: cover`。
- Home 與 Project pages 統一使用共用 `ProjectCover.vue`，不得建立不同的 cover 規格。

**【程式碼事實】** Backend JSON 會隨 container image 部署，每次 request 都重新讀檔；沒有 cache 或 database。

### 9.2 Project 資料責任

- 每個完整 Project 使用一份穩定 slug JSON；同一物件同時包含 card summary metadata 與 detail sections。
- Backend Project JSON 是 `/project` 的完整內容來源；frontend 不保存另一份 Project Detail JSON。
- 首頁仍只讀取 `frontend/src/data/home/projects.json` 的三筆小型 summary，避免為 Preview 載入不需要的 detail 與 Cloud Run cold start。首頁不顯示 architecture、challenges、deployment 或 showcase。
- Cover 檔案仍由 frontend 靜態資產路徑 `frontend/public/images/projects/covers/` 負責；backend JSON 只保存公開 path 與 ready flag。
- Project repository 以固定 slug/file mapping 維持 MRIS、Personal Portfolio Website、Mamatoya 的目前顯示順序。尚未實作 visibility、hide、featured、public、archived 等欄位或篩選邏輯。

### 9.3 Portfolio page data responsibility

Backend Portfolio content 統一以頁面為單位放在 `backend/data/portfolio/`：

- About：`portfolio/about/`，管理個人介紹 paragraphs 與結構化 sections。
- Experience：`portfolio/experience/`，管理 Journey Sections 與 Detail 的獨立 slug JSON。
- Timeline：`portfolio/timeline/`，管理屬於 Journey 時間軸、但不屬於 Experience 的 events。
- Projects：`portfolio/projects/`，管理 Project summary 與 detail JSON。

舊的 `backend/data/profile/` 分類已移除；未來新增 Portfolio page data 時應建立對應 page folder，不把頁面資料放回 portfolio root。

## 10. Backend API 與 schemas

### 10.1 Endpoints

所有 endpoints 都是無認證 `GET`，沒有 request body 或 query parameter；單筆 Project endpoint 使用 `slug` path parameter。

| Method | Path | Response |
|---|---|---|
| GET | `/` | `{ "msg": "FastAPI backend running!" }` |
| GET | `/health` | `{ "status": "ok" }` |
| GET | `/api/about` | About object + top-level `updated_at`（legacy） |
| GET | `/api/experience` | Experience object + `updated_at`（legacy） |
| GET | `/api/timeline-events` | Timeline Events list + `updated_at`（legacy） |
| GET | `/api/projects` | 三個完整 Project objects + 最新檔案 `updated_at`（legacy shape） |
| GET | `/api/projects/{slug}` | 指定 slug 的完整 `ProjectItem`；不存在時回傳標準 404 error envelope |
| GET | `/api/v1/about` | `AboutResponse` |
| GET | `/api/v1/experience` | `ExperienceResponse` |
| GET | `/api/v1/timeline-events` | `TimelineEventsResponse` |
| GET | `/api/v1/projects` | `ProjectsResponse` |
| GET | `/docs`, `/redoc`, `/openapi.json` | FastAPI defaults |

### 10.2 v1 envelope

```json
{
  "data": {},
  "meta": {
    "updated_at": "YYYY-MM-DD HH:MM:SS",
    "version": "v1"
  }
}
```

`updated_at` 來自 JSON 檔案在 container filesystem 的 mtime，不是資料中的發布欄位或 Git commit time。

### 10.3 Models

```text
AboutData
├── paragraphs: string[]（backward compatibility）
└── sections: AboutSection[]
    ├── id / title: string
    ├── paragraphs: string[]
    └── items: string[]

ExperienceData
└── experience: ExperienceItem[]
    ├── slug / category: string
    ├── title / organization / role: string
    ├── location: string
    ├── start_date: string
    ├── end_date?: string | null
    ├── period / summary / logo: string
    ├── skills / technologies: string[]
    ├── description / responsibilities / highlights: string[]
    ├── projects: string[]
    └── gpa?: string | null

TimelineEventsData
└── timeline_events: (PointTimelineEvent | DurationTimelineEvent)[]
    ├── Point: id / label / type="point" / date（YYYY-MM）
    └── Duration: id / label / type="duration" / start_date / end_date（YYYY-MM）

ProjectData
└── projects: ProjectItem[]
    ├── slug: string
    ├── title: string
    ├── subtitle: string
    ├── category: string
    ├── summary: string
    ├── cover / cover_alt: string
    ├── cover_ready: boolean
    ├── period / role: string
    ├── status: "internal" | "live"
    ├── website_url / source_url: string | null
    ├── technologies: string[]
    ├── overview: { title, paragraphs[] }
    ├── responsibilities: { title, items[] }
    ├── architecture: { title, paragraphs[], highlights[] }
    ├── challenges: { title, items[{ title, description }] }
    ├── deployment: { title, paragraphs[], highlights[] }
    ├── lessons_learned: { title, items[] }
    └── showcase: ShowcaseItem[]
```

`GET /api/projects` 與 `GET /api/v1/projects` 會依 repository 的固定順序讀取並逐筆以 `ProjectItem` 驗證；`GET /api/projects/{slug}` 使用相同 repository 與 schema，不建立第二套 loader。三個 Project 的 `showcase` 目前都是空陣列，但 `ShowcaseItem` 已定義 image、image_alt 與選填 caption，供後續加入公開素材。

`GET /api/experience` 與 `GET /api/v1/experience` 共用相同 repository/service aggregation：repository 動態讀取 `portfolio/experience/*.json`，service 逐筆以 `ExperienceItem` 驗證並組成 Experience list。現況沒有 `GET /api/experience/{slug}` endpoint。

`GET /api/timeline-events` 與 `GET /api/v1/timeline-events` 讀取獨立的 `portfolio/timeline/events.json`，並以 discriminated union schema 驗證 point／duration 所需欄位；Experience objects 不包含 Timeline Events。

首頁 Projects Preview schema 是獨立的前端 schema，不應與 backend `ProjectItem` 混用。

目前沒有實際 TypeScript type。依 JSON 與 component usage，可用概念型別表示為：

```text
HomeProjectPreview
├── name: string
├── image: string
├── image_alt: string
├── image_ready: boolean
├── introduction: string
├── tags: string[]
├── website_url?: string
└── source_url?: string
```

`website_url` 與 `source_url` 不要求同時存在；目前 local JSON 可能省略欄位或使用空字串，component 以 truthy URL 依 Live → Source → Internal 順序顯示 action。`image_ready: false` 時顯示 placeholder 且不發出圖片 request；未來把圖片放到 `frontend/public/images/projects/covers/` 的 JSON 指定路徑，再把 flag 改為 true 即可啟用。

### 10.4 Error envelope

```json
{
  "error": {
    "code": "CONTENT_NOT_FOUND | NOT_FOUND | HTTP_<status> | INTERNAL_ERROR",
    "message": "human-readable message",
    "details": null
  }
}
```

- Missing content file：404 / `CONTENT_NOT_FOUND`。
- HTTP 404：`NOT_FOUND`；其他 HTTP exceptions：`HTTP_<status>`。
- 未處理錯誤：500 / `INTERNAL_ERROR`。

## 11. 環境變數與環境差異

### 11.1 Frontend runtime/build config

唯一 application environment variable：

- `VITE_API_BASE`：FastAPI base URL。

位置：

- `frontend/.env.development`：本機開發 API base。
- `frontend/.env.production`：production API base，在 Vite build 時編入 bundle。

這兩個檔案不是 secret store；任何 `VITE_` 值都會出現在 browser bundle。本文不列出實際 URL。

### 11.2 Deployment secrets

GitHub Actions 使用：

- `GCP_SA_KEY`
- `GCP_PROJECT_ID`
- `CLOUD_RUN_REGION`

實際內容只應存在 GitHub Secrets／雲端設定，不應寫入 repository 或本文。

## 12. 建置、啟動、檢查與部署

### 12.1 Frontend local

```bash
cd frontend
npm install
npm run dev
npm run build
./node_modules/.bin/eslint .
npm run preview
```

注意：`npm run lint` 實際執行 `eslint . --fix`，會修改檔案；唯讀檢查應直接執行 `./node_modules/.bin/eslint .`。

### 12.2 Backend local

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

內容 schema 驗證（repository root 執行）：

```bash
python backend/scripts/validate_content_schema.py
```

### 12.3 Docker

- Frontend：`node:20` build stage 執行 `npm install` + `npm run build`，再複製到 `nginx:stable-alpine-slim`。
- Backend：`python:3.13.9`，安裝 requirements，以 Uvicorn 監聽 8080。
- Frontend Nginx 對所有未知檔案 path fallback 到 `index.html`。

### 12.4 GitHub Actions / Cloud Run

兩個 workflow 都在 push 到 `main` 且對應目錄有變更時觸發：

1. Google service-account authentication。
2. 設定 gcloud 與 Artifact Registry auth。
3. 建立 `latest` Docker image。
4. push 到 `asia-east1-docker.pkg.dev`。
5. `gcloud run deploy` 到對應 service 與 secret 指定 region。

Backend workflow 在建 image 前會安裝依賴並執行 content schema validation。Frontend workflow目前沒有 lint 或 test gate。

## 13. 測試現況

**【程式碼事實】** Repository 沒有：

- Frontend unit/component/E2E tests。
- Backend pytest tests。
- Visual regression tests。
- Coverage configuration。

目前可用的自動檢查只有：

- Frontend ESLint。
- Frontend production build。
- Backend JSON/Pydantic schema validation script。

## 14. 已知問題、placeholder 與技術債

### 14.1 已知未完成內容

- `/about` 六個 sections 全部是 `Coming soon.`。
- 三張 Project screenshots 尚未存在；首頁 `image_ready` 與 backend `cover_ready` 全為 false，三份 backend `showcase` 亦為空陣列。
- Backend About API 已具備結構化 sections，但 `/about` 仍是 frontend placeholder，尚未消費正式內容。

### 14.2 Frontend debt

- Global CSS 共 8 個檔案且依載入順序生效；仍有大量 Bootstrap utility、`!important`、散落顏色與重複數值。
- `App.vue` 同時負責 layout、Sidebar、social links、Last updated、hash scroll、viewport CSS variables 與 RouterView。
- `useScrollProxy` 攔截首頁所有 wheel events；nested scrolling、鍵盤與觸控行為需要持續驗證。
- Mobile 首頁高度依 DOM measurement 與三個 runtime CSS variables，受 orientation、browser chrome、內容高度影響。
- `useMouseGlow` 每次 mousemove 查 DOM 並讀取尺寸；詳細頁 Desktop 仍會啟用。
- `requestRaw()` 無 timeout/abort/retry，且先呼叫 `res.json()`；非 JSON error response 會變成 parse error。
- 首頁 Profile 本地 JSON與詳細 Experience API內容使用 `v-html`；沒有 frontend sanitization。
- Axios、`request()`、`isFeaturedProject()`、`previewEngineering()` 目前沒有 consumer。
- 沒有 catch-all 404 route。
- `index.html` 的 `lang` 為空，且缺少 description、canonical、Open Graph、Twitter card 與 structured data。
- Vue DevTools plugin 沒有明確限制只在 development 使用。

### 14.3 Backend debt

- CORS 同時使用 `allow_origins=["*"]` 與 `allow_credentials=True`，production policy 過寬且語意不清。
- JSON rich text 含外部 `<a target="_blank">`，部分內容未包含 `rel="noopener noreferrer"`，並由 `v-html` render。
- 每個 request 都同步開檔與解析 JSON，沒有 cache。
- Legacy `/api/*` endpoints仍保留，是否有外部 consumer 未知。
- Project visibility、hide、featured、public、archived 與分類篩選尚未設計或實作；目前固定依 repository mapping 顯示三筆。
- `core/config.py` 與 `core/logging.py` 只是 placeholder。
- `python-multipart` 已安裝但未使用。
- 沒有 authentication、rate limiting、explicit cache headers 或 security headers。

### 14.4 Deployment debt

- Images 只使用 mutable `latest` tag，缺少 commit SHA tag與明確 rollback artifact。
- Frontend Docker 使用 `npm install` 而非 `npm ci`。
- Cloud Run deploy command沒有在 repository 中設定 resource limits、autoscaling、health probe 或 unauthenticated policy。
- Production API URL 是 build-time config，切換環境需要重新 build frontend。

## 15. 高耦合與改版風險

| 區域 | 耦合原因 | 可能影響 |
|---|---|---|
| `App.vue` + `main-rwd.css` | DOM selectors、route meta、mobile measurements、Sidebar/footer | 首頁 scrolling、detail layout、mobile viewport |
| `.main-content` | 首頁是內層 scroll；詳細頁是 document flow | wheel proxy、route scroll、anchor spacing |
| Global CSS | Home/detail selectors共存在同一 cascade | 修改 `.project-card`、`.exp-card` 或 Bootstrap class可能跨頁影響 |
| Home/Detail summary duplication | 首頁小型 Preview JSON 與 backend Project summary 需人工同步；完整 detail 僅存在 backend | 文案、tags、links 漂移 |
| JSON → Pydantic → Vue | 詳細頁 contract跨三層 | 欄位 rename、optional semantics、HTML rendering |
| Experience logo mapping | Backend只給 filename，frontend hard-code imports | 新增 logo需同時改 JSON、檔案與 mapping |
| Experience folder aggregation | Repository 會自動發現新 slug JSON，但 logo 仍由 frontend mapping，排序依 `start_date` 字串 | 新增資料需使用一致日期格式並補 logo mapping |
| Project images | JSON path + `image_ready` + public asset | 檔名或 flag錯誤會顯示 placeholder |
| Deploy-time API base | URL baked into frontend bundle | backend service/domain/region更名需重建 frontend |

## 16. 建議修改順序與驗證方式

### 16.1 目前內容 Roadmap

- **About 正式內容**：將六個 `Coming soon.` sections 補成正式個人與工程介紹。
- **About API 整合**：現有 `/api/v1/about` 已同時提供 backward-compatible `paragraphs` 與結構化 `sections`；下一步是讓 `/about` 取代 frontend placeholder 並加入 loading/error/empty states。
- **Experience 詳細內容**：三份 slug JSON、聚合 API、單段收合／展開、shared-row Timeline 與 active segment glow 已存在；仍需內容校稿、公開資訊確認、Timeline stretch 與詳細頁視覺整理。
- **Project 詳細內容**：三份 slug JSON、API、完整欄位與單卡收合／展開互動已存在；仍需內容校稿、公開資訊確認、Showcase、架構圖與詳細頁視覺整理。
- **Homepage Project screenshots**：三張 future paths 已設定，但實體 `.webp` 尚未加入，`image_ready` 仍為 false。
- **Homepage Project 資料挑選**：目前固定維護三筆 local JSON，尚無自動排序／選取規則；需人工確認哪些作品最適合 recruiter-first 首頁。
- **Mobile 細節優化**：持續檢查 fixed header/footer、內層 scrolling、orientation、safe area、長標題、links 與 200% zoom。
- **整體內容校稿**：統一 Software Engineer／Journey 等用詞，修正文法與拼字，確認 Resume、首頁 Preview 與 backend 完整資料一致。

### 16.2 Phase 1：建立安全網

1. 加 frontend component tests：Home preview conditional links、image fallback、loading/error states。
2. 加 backend endpoint/contract tests。
3. CI 加 `npm ci`、唯讀 lint、build、tests。
4. 建立 320/375/768/1024/1300px visual baselines。

### 16.3 Phase 2：內容契約

1. 為既有 About section-based API 補 frontend contract tests，確認 optional items 與 section ordering。
2. 決定 Preview 與 backend content 的同步來源或產生流程。
3. 定義 rich-text sanitization 策略。
4. 修正 backend content 拼字與空字串 link semantics，但先做 contract test。

### 16.4 Phase 3：Layout / design system

1. 抽出 declarative Home layout primitives，降低 App DOM selector依賴。
2. 將 colors、spacing、type、motion補成 tokens。
3. 限縮 feature styles，避免 global selector跨頁。
4. 改善 reduced motion、keyboard scroll、focus 與 200% zoom。

### 16.5 Phase 4：內容與產品

1. 完成 About sections。
2. 補 Project screenshots與 architecture diagrams。
3. 強化 recruiter-first project narratives與個人貢獻。
4. 補 SEO metadata、404 與可下載 Resume的版本管理。

### 16.6 每階段最低驗證

- `npm run build`
- `./node_modules/.bin/eslint .`（不帶 `--fix`）
- `python backend/scripts/validate_content_schema.py`
- `/`、`/about`、`/experience`、`/project` 直接開啟與重新整理
- FastAPI success/error/empty response states
- Desktop/Tablet/Mobile、keyboard-only、reduced-motion、200% zoom
- Social links、Resume、external project links、logo與image fallback
- Cloud Run staging smoke test與 rollback確認

## 17. 外部環境仍需確認的事項

以下無法只靠 repository 證明：

- 正式 custom domain、DNS 與 Cloud Run domain mapping現況。
- Cloud Run IAM/public access、resource limits、autoscaling、health checks。
- GitHub Secrets與service account最小權限。
- Legacy endpoints是否仍有外部 consumer。
- Backend JSON是否為 production唯一內容來源。
- Production logs、monitoring、alerts、billing與最近成功 revision。
- Portfolio、工作內容與外部 links的公開／保密審查狀態。

---

本文件描述的是上述更新日期的 repository 實況。當其他 README、ARCHITECTURE、FEATURES、SYSTEM_DESIGN 或 TODO 文件與程式碼衝突時，應以可執行程式碼為準，並把差異視為待整理的文件債務。
