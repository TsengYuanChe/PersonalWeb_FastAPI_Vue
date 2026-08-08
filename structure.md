# Project Structure

> 盤點日期：2026-08-02  
> 依據：repository 目前 tracked files、實際 imports、routes、API 與 build configuration。  
> 範圍：不列出 `node_modules/`、`dist/`、`backend/venv/`、`__pycache__/`、`.DS_Store` 等本機或生成內容。

## Root Directory

```text
PersonalWeb_Flask_Vue/
├── .github/                 # GitHub Actions deployment workflows
├── backend/                 # FastAPI content API、schema validation、JSON content
├── frontend/                # Vue 3 SPA、static assets、Nginx runtime image
├── AGENTS.md                # AI coding agent product/coding instructions
├── BACKEND.md               # Backend architecture and maintenance guide
├── overview.md              # Product、architecture、data flow、risk overview
├── structure.md             # Current tracked file structure and responsibilities
├── README.md                # Repository-level introduction（部分內容可能落後現況）
├── ARCHITECTURE*.md         # 中英文架構文件
├── FEATURES*.md             # 中英文功能文件
├── SYSTEM_DESIGN*.md        # 中英文系統設計文件
├── PROJECT_DOCS.md          # Project documentation entry
├── RWD_LAYOUT.md            # Responsive layout notes
├── TODO.md                  # General backlog
├── TODO_Layout.md           # Layout backlog
└── .gitignore               # Python、environment、build、editor ignore rules
```

### Root responsibilities

- `.github/workflows/`：production deployment automation；runtime 不讀取。
- `backend/`：獨立 Cloud Run FastAPI service 的 build context。
- `frontend/`：獨立 Cloud Run Vue/Nginx service 的 build context。
- `overview.md`：產品定位、頁面行為、資料契約、部署與風險的主要現況文件。
- `structure.md`：以實際檔案為中心的責任地圖，供技術債盤點與 refactor 規劃。
- `BACKEND.md`：Backend architecture、content workflow、local development、validation 與 maintenance guide。
- 其他 root Markdown：歷史設計、功能、TODO 與 setup 文件；內容不一定與執行中程式完全同步。

## Backend Structure

```text
backend/
├── main.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── setup.md
├── data/
│   └── portfolio/
│       ├── about/
│       │   └── about.json
│       ├── journey/
│       │   ├── ezoom.json
│       │   ├── nycu-master.json
│       │   └── nchu-bachelor.json
│       ├── projects/
│       │   ├── mris.json
│       │   ├── personal-portfolio.json
│       │   └── andessence.json
│       └── timeline/
│           └── events.json
├── repositories/
│   ├── __init__.py
│   ├── common.py
│   ├── about_repository.py
│   ├── journey_repository.py
│   ├── project_repository.py
│   └── timeline_repository.py
├── services/
│   ├── __init__.py
│   ├── about_service.py
│   ├── journey_service.py
│   ├── project_service.py
│   └── timeline_service.py
├── schemas/
│   ├── __init__.py
│   ├── common.py
│   ├── about.py
│   ├── journey.py
│   ├── project.py
│   └── timeline.py
├── routers/
│   ├── __init__.py
│   └── v1/
│       ├── __init__.py
│       ├── about.py
│       ├── journey.py
│       ├── projects.py
│       ├── timeline.py
│       └── health.py
└── scripts/
    └── validate_content_schema.py
```

### Backend entry and runtime

- `main.py` — **runtime**：建立 FastAPI app、設定 CORS、各註冊一次 About／Journey／Projects／Timeline／Health routers，提供 root endpoint、FastAPI 預設 docs/OpenAPI 與統一 JSON error envelopes。
- `requirements.txt` — **build/runtime dependency manifest**：FastAPI、Uvicorn、Pydantic 等 pinned dependencies。
- `Dockerfile` — **deployment build/runtime**：以 Python 3.13.9 建置；先複製並安裝 requirements，再複製 backend source；使用 Uvicorn 綁定 `0.0.0.0:8080`。
- `.dockerignore` — **deployment build context filter**：排除 local virtual environments、Python bytecode/cache、tool caches、logs 與 `.DS_Store`，避免 `COPY . .` 納入非 runtime artifacts。
- `setup.md` — **documentation**：backend environment、local server、validation、content update 與 container commands；不參與 runtime。

### `backend/data/portfolio/`

所有檔案均為 **runtime content source**，同時由 validation script 檢查：

- `about/about.json`：About detail body 的結構化 `sections[{id,title,paragraphs,items}]`；不保存 View-owned page header copy。
- `journey/*.json`：每段 Journey 一份 slug JSON；repository 動態掃描並以 `start_date` 新到舊排序。
- `projects/*.json`：每個 Project 一份 summary + detail JSON；目前 repository 以固定 mapping 控制三筆順序及 slug lookup。
- `timeline/events.json`：不屬於 Journey 的 point/duration Timeline Events。

### `backend/repositories/`

- `common.py` — **runtime shared data access utility**：定義 backend data root、同步讀取 JSON，並將 filesystem mtime 格式化為 `updated_at`；不包含 resource logic。
- `about_repository.py` — **runtime data access**：管理 About JSON path，回傳 raw About data 與 timestamp。
- `journey_repository.py` — **runtime data access**：管理 Journey directory、動態掃描 `*.json`，並維持既有 `start_date` descending ordering 與最新 timestamp。
- `project_repository.py` — **runtime data access**：管理 Project directory、固定 slug/file mapping、list ordering 與 single-project lookup。
- `timeline_repository.py` — **runtime data access**：管理 Timeline Events JSON path，回傳 raw event data 與 timestamp。
- `content_repository.py` 已移除；目前沒有 wrapper、dead function 或 runtime consumer。
- Repository 不進行 Pydantic validation；validation 位於 service layer。

### `backend/services/`

- `about_service.py` — **runtime application/content layer**：讀取並驗證 About，組裝 About v1 response 與 timestamp metadata。
- `journey_service.py` — **runtime application/content layer**：驗證 Journey list、依 `start_date` descending 確保排序，並組裝 Journey v1 response。
- `project_service.py` — **runtime application/content layer**：驗證 Project list、保留 repository ordering，並處理 slug lookup 與 404。
- `timeline_service.py` — **runtime application/content layer**：驗證 Point／Duration Timeline Events，組裝 Timeline v1 response。
- `content_service.py` 已移除；目前沒有 legacy response helper 或集中式 service runtime consumer。

### `backend/schemas/`

- `common.py` — **runtime validation/serialization**：`Meta`、通用 `ApiResponse`。
- `about.py` — **runtime validation/serialization**：About section、data 與 response models。
- `journey.py` — **runtime validation/serialization**：Journey item、list data 與 response models。
- `project.py` — **runtime validation/serialization**：Project summary/detail nested models、showcase、challenge、item、data 與 response。
- `timeline.py` — **runtime validation/serialization**：Point／Duration Timeline Event models、discriminated union、data 與 response。
- `content.py` 已移除；目前沒有 compatibility wrapper、dead model 或 runtime consumer。
- Resource schemas 同時供 runtime services/routers 與 content validation tooling 使用。

### `backend/routers/`

- `routers/v1/about.py` — **runtime HTTP routing**：只處理 `GET /api/v1/about`。
- `routers/v1/journey.py` — **runtime HTTP routing**：只處理 `GET /api/v1/journey`。
- `routers/v1/projects.py` — **runtime HTTP routing**：處理 Project collection 與 slug endpoints。
- `routers/v1/timeline.py` — **runtime HTTP routing**：只處理 `GET /api/v1/timeline-events`。
- `routers/v1/health.py` — **runtime HTTP routing**：只處理 `GET /api/v1/health`。
- 各 `__init__.py` 只標記 Python package。

### `backend/scripts/`

- `validate_content_schema.py` — **validation/tooling**：
  - 掃描 `backend/data/**/*.json`。
  - 驗證 About、Journey、Projects、Timeline Events。
  - 對未知或缺少 schema mapping 的 JSON fail closed。
  - 由 backend GitHub Actions workflow 在 deployment build 前執行。

## Frontend Structure

```text
frontend/
├── src/
│   ├── main.js
│   ├── App.vue
│   ├── router/
│   │   └── index.js
│   ├── api/
│   │   ├── client.js
│   │   └── contentApi.js
│   ├── views/
│   │   ├── HomeView.vue
│   │   ├── AboutView.vue
│   │   ├── JourneyView.vue
│   │   └── ProjectView.vue
│   ├── components/
│   │   ├── about/
│   │   │   └── AboutSection.vue
│   │   ├── journey/
│   │   │   ├── HomeJourneyItem.vue
│   │   │   ├── JourneySection.vue
│   │   │   ├── JourneyDetail.vue
│   │   │   └── Timeline.vue
│   │   ├── layout/
│   │   │   ├── DetailPageHeader.vue
│   │   │   ├── HomeSidebar.vue
│   │   │   ├── MobileFooter.vue
│   │   │   └── SocialLinks.vue
│   │   └── projects/
│   │       ├── HomeProjectPreview.vue
│   │       ├── ProjectAction.vue
│   │       ├── ProjectCard.vue
│   │       ├── ProjectDetail.vue
│   │       └── ProjectCover.vue
│   ├── composables/
│   │   ├── useAutoHeightTransition.js
│   │   └── shell/
│   │       ├── useHomeSectionNavigation.js
│   │       ├── useHomeViewportMetrics.js
│   │       ├── useMouseGlow.js
│   │       └── useScrollProxy.js
│   ├── config/
│   │   ├── siteLinks.js
│   │   └── pageMeta.js
│   ├── utils/
│   │   ├── journey/
│   │   │   ├── journeyLogos.js
│   │   │   └── timelineMath.js
│   │   └── projects/
│   │       └── projectSearch.js
│   ├── data/home/
│   │   ├── about.json
│   │   ├── journey.json
│   │   └── projects.json
│   └── assets/
│       ├── css/
│       │   ├── main.css
│       │   ├── main-rwd.css
│       │   ├── about.css
│       │   ├── about-rwd.css
│       │   ├── journey.css
│       │   ├── journey-rwd.css
│       │   ├── projects.css
│       │   └── projects-rwd.css
│       └── images/journey/
│           ├── ezoom.png
│           ├── nycu.png
│           └── nchu.png
├── public/
│   ├── files/Adam_Tseng_Resume.pdf
│   └── favicon files
├── index.html
├── package.json
├── package-lock.json
├── vite.config.js
├── eslint.config.js
├── jsconfig.json
├── nginx.conf
├── Dockerfile
├── .dockerignore
├── .env.development
├── .env.production
└── setup/editor/documentation files
```

目前不存在：

- `frontend/src/services/`：content service abstraction 實際位於 `src/api/contentApi.js`。
- `frontend/src/stores/`：沒有 Pinia/Vuex；page state 由各 View 的 `ref`/`computed` 管理。
- `frontend/src/types/`：專案使用 JavaScript，沒有 TypeScript types。

### Frontend entry, shell, and routing

- `src/main.js` — **runtime entry**：建立 Vue app、安裝 router、依固定順序全域載入 Bootstrap、icons 與八個自訂 CSS 檔。
- `src/App.vue` — **runtime application shell**：依 route meta 切換 Home／Detail layout，組合 HomeSidebar／main／MobileFooter；擁有 Last updated API request、route watcher、global effects 與 RouterView，將 `updatedTime` 下傳給兩個 Home shell children，並提供 navigation／viewport／scroll proxy composables所需 template refs與 Home enablement。
- `src/router/index.js` — **runtime routing**：history-mode `/`、`/about`、`/journey`、`/project`；route meta 指定 layout；route change 回到頂部。沒有 catch-all 404 route。

### Views

- `HomeView.vue` — **Home-only**：直接 import 三份 frontend local preview JSON，組裝 Profile、Journey、Projects previews。
- `AboutView.vue` — **About-only**：選取 About page metadata，透過 `getAbout()` 載入 body sections，處理 loading/error/empty/success，交給 `DetailPageHeader` 與 `AboutSection` render。
- `JourneyView.vue` — **Journey-only orchestration**：選取 Journey page metadata、載入 Journey + Timeline Events、管理 active/expanded/leaving states、計算 Grid rows，並協調 DetailPageHeader、Timeline、JourneySection、JourneyDetail 與共用 dynamic-height transition hooks。
- `ProjectView.vue` — **Projects-only orchestration**：選取 Project page metadata、載入 Projects、管理 search/filter/empty state 與單一 expanded slug，協調 DetailPageHeader 並 render ProjectCard list。

### Components

#### `components/about/`

- `AboutSection.vue` — **About page-specific**：顯示單一 API section 的 heading、paragraphs、optional items；無 API 或 state ownership。

#### `components/journey/`

- `HomeJourneyItem.vue` — **Home-specific**：精簡 Journey preview row。
- `JourneySection.vue` — **Journey page-specific**：永遠可見的 Journey header、logo、summary、metadata、More/Less toggle；不知道 Timeline。
- `JourneyDetail.vue` — **Journey page-specific**：展開後的 description、responsibilities、highlights、projects、skills/technologies、additional details；不知道 Timeline 或 expanded state。
- `Timeline.vue` — **Journey page-specific**：擁有 props/computed presentation mapping、Journey periods、date labels、nodes、active segments、connectors、static Timeline Events、interaction 與 accessibility；接收 View 計算的 row mapping，不 render Journey content，底層日期／位置公式委派給純 utility。

#### `components/projects/`

- `HomeProjectPreview.vue` — **Home-specific**：精簡 Project preview row，組合 ProjectCover、ProjectAction。
- `ProjectCard.vue` — **Project page-specific orchestration**：Project summary header、expanded prop、toggle event、detail wrapper 與共用 dynamic-height transition hooks；將完整 detail rendering 委派給 ProjectDetail。
- `ProjectDetail.vue` — **Project page-specific renderer**：接收必填 Project object，依 `overview.md` 定義的 canonical Project section order 與 optional 判斷 render detail content，並顯示 technologies；不擁有 expanded state、toggle 或 Transition。
- `ProjectCover.vue` — **cross-page shared**：Home／Project Page 共用 160×100、16:10 image/placeholder/error fallback。
- `ProjectAction.vue` — **cross-page shared**：依 website/source URLs render Live、Source 或 non-clickable Internal。

#### `components/layout/`

- `DetailPageHeader.vue` — **detail-page shared**：About、Journey、Project 共用 breadcrumb、唯一 page `h1` 與 description；只 render View 傳入的 presentation props。
- `HomeSidebar.vue` — **Home shell-specific**：profile header、三個 section RouterLinks、desktop SocialLinks 與 Last updated；presentation-only，接收 `updatedTime`。
- `MobileFooter.vue` — **Home shell-specific**：mobile SocialLinks 與 Last updated；presentation-only，接收 `updatedTime`。
- `SocialLinks.vue` — **Home shell shared renderer**：以單一 anchor template render desktop/mobile social 與 Resume links，依 `variant` 保留既有 classes、labels 與 tooltip attributes。

### Frontend config

- `config/siteLinks.js`：GitHub、LinkedIn、Instagram、Facebook 與 Resume 的 id、label、URL、Bootstrap icon class 與 new-tab behavior；由 `SocialLinks.vue` 單獨消費。
- `config/pageMeta.js`：About、Journey、Project detail routes 的靜態 title／description；各 View 選取對應 entry，並交由 `DetailPageHeader.vue` render。它不擁有 backend portfolio body content。

### API layer

- `api/client.js`：
  - `requestRaw(path)` 組合 `VITE_API_BASE`、執行 Fetch、解析 JSON、正規化 API errors。
- `api/contentApi.js`：About、Journey、Timeline Events、Projects 的 feature-facing functions；將 v1 envelope 轉為 `{content, updatedAt}`。

### Composables and utilities

- `composables/useAutoHeightTransition.js`：JourneyView 與 ProjectCard 共用的 domain-agnostic DOM transition；提供 `beforeEnter`、`enter`、`afterEnter`、`beforeLeave`、`leave`，集中處理實際 `scrollHeight`、height、opacity、translateY、`inert` 與 `aria-hidden`。
- `composables/shell/useHomeSectionNavigation.js`：接收 reactive route與 Home main DOM ref，依既有 `#about` top spacing計算 Home／Journey／Projects hash位置，公開 `scrollToCurrentSection()`；不擁有 watcher、router instance或其他 shell state。
- `composables/shell/useHomeViewportMetrics.js`：接收 HomeSidebar／MobileFooter template refs，更新 `--header-height`、`--footer-height`、`--real-vh`，並擁有 mounted 初次量測與 resize listener cleanup；不使用 DOM selectors。
- `composables/shell/useMouseGlow.js`：全域 mousemove cursor glow；由 `App.vue` 使用。
- `composables/shell/useScrollProxy.js`：接收 main content template ref與 Home-layout `enabled` computed；mounted時註冊 non-passive window wheel listener，只在啟用時轉送相同 `deltaY` 並呼叫 `preventDefault()`，unmount時解除 listener，不使用 DOM selectors。
- `ProjectDetail.vue` 的 `safeArray` 是其 detail template 專用 local helper；沒有建立只有單一 consumer 的 composable 或 utility。
- `utils/journey/journeyLogos.js`：backend logo filename 到 Vite image imports 的固定 mapping。
- `utils/journey/timelineMath.js`：不依賴 Vue、DOM 或 module-level mutable state的 Timeline 純函式；負責年月索引、Journey bounds、Event 是否完整落在單一 Journey，以及日期在 period 內的百分比位置。`Timeline.vue` 是目前唯一 consumer。
- `utils/projects/projectSearch.js`：Project public text collection、whole-token search、exact filters、dynamic option sorting。

### Frontend data and assets

- `data/home/*.json` — **runtime local preview data**：首頁 About、Journey、Projects；不經 backend。
- `assets/images/journey/*.png` — **bundled runtime assets**：Journey logos。
- `public/files/Adam_Tseng_Resume.pdf` — **copied static asset**：首頁 Resume link。
- `public/favicon*` — **copied static assets**：browser favicon。
- Project cover paths 預定在 `public/images/projects/covers/`，目前 tracked tree 尚無 cover files。

### Frontend build and deployment files

- `package.json` / `package-lock.json`：npm scripts、實際使用的 runtime/dev dependencies 與 reproducible install lockfile；HTTP 使用 browser Fetch，不依賴 Axios。
- `vite.config.js`：Vue plugin、development-only Vue DevTools plugin 與 `@` alias；production build 不載入 DevTools plugin。
- `eslint.config.js`：ESLint flat config。
- `.prettierrc.json`：formatting rules；format script只針對 `src/`。
- `jsconfig.json`：JavaScript tooling 與 alias；不是 TypeScript config。
- `.env.development` / `.env.production`：tracked build-time API base configuration；不要在文件記錄實際值。
- `nginx.conf`：production static server 與 SPA `try_files` fallback。
- `Dockerfile`：Node build stage 以 `npm ci` 按 lockfile 安裝，再由 Nginx runtime stage 提供 build output。
- `.dockerignore`：排除 local `node_modules`、`dist`、coverage、editor metadata、logs 與 npm/Vite caches，縮小 Docker build context。

## Data Flow

### About

```text
backend/data/portfolio/about/about.json
  → about_repository.read_about_with_timestamp()
  → about_service.get_about_v1()
  → AboutData / AboutResponse
  → GET /api/v1/about
  → frontend api/contentApi.getAbout()
  → AboutView.vue
  → AboutSection.vue
```

`App.vue` 也呼叫同一 API，但只使用 `meta.updated_at` 顯示首頁 Last updated。

### Journey

```text
backend/data/portfolio/journey/*.json
  → journey_repository.read_journey_items_with_timestamps()
  → journey_service JourneyItem validation + response aggregation
  → GET /api/v1/journey
  → frontend api/contentApi.getJourney()
  → JourneyView.vue
  → JourneySection.vue + JourneyDetail.vue + Timeline.vue
```

Journey service 依 `start_date` descending 確保 response order；repository 目前也維持相同既有讀取順序。Logo 圖片由 frontend `utils/journey/journeyLogos.js` 另行映射。

### Timeline Events

```text
backend/data/portfolio/timeline/events.json
  → timeline_repository.read_timeline_events_with_timestamp()
  → timeline_service TimelineEventsData discriminated-union validation
  → GET /api/v1/timeline-events
  → frontend api/contentApi.getTimelineEvents()
  → JourneyView.vue
  → Timeline.vue
```

Timeline Events 不建立 Journey Section/Detail；位置由 Timeline 依 Journey date bounds 計算。

### Projects

```text
backend/data/portfolio/projects/*.json
  → project_repository fixed PROJECT_FILES mapping
  → project_service ProjectItem validation + list/slug response handling
  → GET /api/v1/projects
  → frontend api/contentApi.getProjects()
  → ProjectView.vue
  → ProjectCard.vue
  → ProjectCover.vue + ProjectAction.vue + ProjectDetail.vue
```

首頁 Projects 不走此流程，而是讀取 `frontend/src/data/home/projects.json` 的 preview-only summary。

## API Structure

Backend resource routes 分別定義在 `backend/routers/v1/` 的 `about.py`、`journey.py`、`projects.py`、`timeline.py` 與 `health.py`；content HTTP API 僅保留 v1 surface。

### Versioned endpoints

| Endpoint | Response model | Frontend usage |
|---|---|---|
| `GET /api/v1/about` | `AboutResponse` | `AboutView.vue`；`App.vue` Last updated |
| `GET /api/v1/journey` | `JourneyResponse` | `JourneyView.vue` |
| `GET /api/v1/timeline-events` | `TimelineEventsResponse` | `JourneyView.vue` |
| `GET /api/v1/projects` | `ProjectsResponse` | `ProjectView.vue` |
| `GET /api/v1/projects/{slug}` | `ProjectItem` | 無目前 frontend consumer；可供單筆查詢 |
| `GET /api/v1/health` | plain status object | 無 frontend consumer；service probe |

四個 content collection responses 使用 `{data, meta:{updated_at,version}}`；Project slug 回傳 `ProjectItem`，health 回傳 plain status object。

### Infrastructure endpoints

- `GET /`：backend running message。
- `/docs`、`/redoc`、`/openapi.json`：FastAPI defaults。

## CSS Structure

所有自訂 CSS 都由 `frontend/src/main.js` 全域載入，沒有 Vue scoped styles。

| File | Current responsibility |
|---|---|
| `main.css` | Global design tokens、document/App shell、Home/Detail layout、Sidebar/footer、shared page state/header、Home section heading/link primitive、Journey/Project shared tags |
| `main-rwd.css` | App shell、shared detail layout、shared Home link 與 shared tag responsive behavior |
| `about.css` | Home Profile typography + `/about` sections、paragraphs、items |
| `about-rwd.css` | About/Home Profile responsive typography and spacing |
| `journey.css` | Home Journey preview + `/journey` Timeline、events、Section、Detail、transitions（不擁有跨 Home section/link 或 shared tag primitives） |
| `journey-rwd.css` | Journey/Timeline/Home preview responsive behavior；Mobile hides Timeline |
| `projects.css` | Home Project preview + `/project` cards、category、cover/action、details、search/filter toolbar；Project cover variables 保持 feature-owned |
| `projects-rwd.css` | Project preview/cards/tools 與 Project-only tag container/language tag responsive layouts |

CSS import order remains `main → main-rwd → projects → projects-rwd → about → about-rwd → journey → journey-rwd` and is part of current behavior. Styles remain global；ownership 由 actual consumers、feature boundary 與 selector convention 維持，而不是 module/scoped isolation。`.project-category` 已歸 Projects；`.tag`／`.tag-tool` 因 JourneyDetail 與 ProjectDetail 共用而歸 main；`.home-section`、`.section-heading`、`.home-journey-link` 因跨 Home About／Journey／Projects 使用而歸 main。

第一輪 consumer scan 已移除 verified dead `.code-btn`、`.tag-lang`、`.see-more-wrapper`、`.see-more-btn`、`.section-footer-link`、`.exp-gpa` 與 mobile `#exp` rules，包含其 hover 與 responsive variants；Transition、Vue Router 與 Timeline dynamic modifier selectors均保留。這次沒有搬移 ownership、改 declaration 或調整 import order。

## Deployment and Automation Structure

```text
.github/workflows/
├── backend-deploy.yml
└── frontend-deploy.yml
```

- `backend-deploy.yml`：main branch 的 `backend/**` changes 觸發；安裝 Python dependencies、執行 content validation、build/push image、deploy `fastapi-backend` to Cloud Run。
- `frontend-deploy.yml`：main branch 的 `frontend/**` changes 觸發；build/push image、deploy `vue-frontend` to Cloud Run。
- 兩個 workflows 使用 Google auth、Artifact Registry 與 mutable `latest` image tag。
- Root documentation-only changes不會觸發 deployment。

## Known Technical Debt

以下皆為目前程式或 tracked structure 可直接確認的狀態；本文件只記錄，不執行修正。

- **Global CSS coupling**：八個 custom CSS 仍全域載入並依 cascade/import order 生效；ownership 已建立，但 selector convention 無法提供 scoped isolation。
- **Deferred CSS cleanup**：第一輪 verified dead selectors已移除；仍待處理重複 media query、`!important`、breakpoint normalization、hardcoded accent/surface/motion values、token inventory 與 `.home-journey-link` naming debt。
- **Large orchestration files**：Timeline date／position math與共用 height transition已抽離，Project detail rendering亦已從 ProjectCard分離；`JourneyView.vue` 仍集中管理 row lifecycle與 sibling coordination，`Timeline.vue` 仍集中管理同軸 presentation rendering。後續只應在測試證明收益時再拆責任，不以行數作為依據。
- **App shell coupling**：Sidebar、Mobile Footer、重複 link data、viewport resize lifecycle、Home section scroll implementation與 scroll proxy selector coupling已抽離；`App.vue` 仍同時管理 route-aware layout、Last updated、route watcher、global effects 與 RouterView。
- **No frontend stores/types/tests**：沒有 store、TypeScript types、unit/component/E2E test directories；資料 shape 主要由 backend schema、JSON 與 runtime property access約束。
- **API naming**：frontend 沒有 `services/`；`contentApi.js` 實際扮演 service layer，而 `client.js` 保留唯一使用中的 low-level `requestRaw()` transport。
- **Synchronous JSON I/O**：每個 content request 都同步開檔、parse JSON、validate；沒有 cache。
- **Duplicated content responsibility**：首頁三份 local preview JSON 與 backend detail summary 需人工同步，可能產生文案、links、tags 漂移。
- **Rich HTML handling**：首頁 About preview 與 Journey detail 使用 `v-html`；沒有 frontend sanitization layer。
- **Router gaps**：沒有 catch-all 404 route；route URLs 使用既有 singular `/journey`、`/project` naming。
- **Build/deployment debt**：images 只推 mutable `latest` tag；Node build image 仍使用未固定 patch 的 `node:20`。
- **Environment configuration**：frontend environment files被 tracked，API base 在 build time寫入 bundle；任何環境切換都需 rebuild。
- **Documentation duplication**：root 有多份中英文 architecture/features/system-design/TODO 文件，內容可能彼此或與 runtime code不同步。
- **Generated local artifacts**：workspace 可見 `backend/venv/`、`__pycache__/`、`.DS_Store`，目前均未 tracked；仍可能增加掃描噪音。

## Refactor Candidates

這些是未來候選方向，不代表已核准的 implementation plan。

### Priority High

1. 建立 frontend/backend contract tests，覆蓋四組 v1 responses、404/error envelope 與 JSON validation。
2. 為 About、Journey、Projects 建立最小 component/E2E regression tests，保護 loading/error/empty/expanded/filter states。
3. 在既有 ownership 與第一輪 dead selector cleanup 基礎上，盤點可安全 token 化的重複 accent、surface 與 motion values，並另案處理 media query／breakpoint normalization。
4. 為 `v-html` content 建立可信來源規範與 sanitization policy。

### Priority Medium

1. 只有在 row lifecycle tests證明收益時，才將 `JourneyView.vue` 的 expanded／leaving row coordination抽成 `useJourneyRows`；active sibling sync與 API loading仍留在 View。
2. 決定首頁 preview 與 backend summary 的 single-source-of-truth 或產生流程。
3. 補齊 request timeout、abort、non-JSON error handling與缺少 API base時的明確錯誤邊界。
4. 清理 placeholder directories/files。

### Priority Low

1. 抽出 Home/Detail layout components，降低 `App.vue` DOM responsibilities。
2. 補 catch-all 404 page 與 route-level metadata/SEO management。
3. 評估 TypeScript 或 runtime prop/schema validation策略，不應與 UI refactor綁定一次完成。
4. 收斂重複 root documentation，指定 `overview.md`、`structure.md` 與 feature specs的更新責任。
5. 改善 Docker reproducibility、immutable image tags、rollback artifacts與 production observability。
6. 測試層實際落地時再依 unit／component／E2E責任建立目錄，不預先建立空 test hierarchy。
7. 完成 token inventory並具備 visual regression coverage後，再評估 `tokens.css`／`layout.css` 或 selective scoped styles；不進行一次性 global CSS migration。
