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
│       ├── experience/
│       │   ├── ezoom.json
│       │   ├── nycu-master.json
│       │   └── nchu-bachelor.json
│       ├── projects/
│       │   ├── mris.json
│       │   ├── personal-portfolio.json
│       │   └── mamatoya.json
│       └── timeline/
│           └── events.json
├── repositories/
│   ├── __init__.py
│   ├── common.py
│   ├── about_repository.py
│   ├── experience_repository.py
│   ├── project_repository.py
│   └── timeline_repository.py
├── services/
│   ├── __init__.py
│   ├── about_service.py
│   ├── experience_service.py
│   ├── project_service.py
│   └── timeline_service.py
├── schemas/
│   ├── __init__.py
│   ├── common.py
│   ├── about.py
│   ├── experience.py
│   ├── project.py
│   └── timeline.py
├── routers/
│   ├── __init__.py
│   └── v1/
│       ├── __init__.py
│       ├── about.py
│       ├── experience.py
│       ├── projects.py
│       ├── timeline.py
│       └── health.py
└── scripts/
    └── validate_content_schema.py
```

### Backend entry and runtime

- `main.py` — **runtime**：建立 FastAPI app、設定 CORS、各註冊一次 About／Experience／Projects／Timeline／Health routers，提供 root endpoint、FastAPI 預設 docs/OpenAPI 與統一 JSON error envelopes。
- `requirements.txt` — **build/runtime dependency manifest**：FastAPI、Uvicorn、Pydantic 等 pinned dependencies。
- `Dockerfile` — **deployment build/runtime**：以 Python 3.13.9 建置；先複製並安裝 requirements，再複製 backend source；使用 Uvicorn 綁定 `0.0.0.0:8080`。
- `.dockerignore` — **deployment build context filter**：排除 local virtual environments、Python bytecode/cache、tool caches、logs 與 `.DS_Store`，避免 `COPY . .` 納入非 runtime artifacts。
- `setup.md` — **documentation**：backend environment、local server、validation、content update 與 container commands；不參與 runtime。

### `backend/data/portfolio/`

所有檔案均為 **runtime content source**，同時由 validation script 檢查：

- `about/about.json`：About legacy paragraphs 與結構化 `sections[{id,title,paragraphs,items}]`。
- `experience/*.json`：每段 Journey 一份 slug JSON；repository 動態掃描並以 `start_date` 新到舊排序。
- `projects/*.json`：每個 Project 一份 summary + detail JSON；目前 repository 以固定 mapping 控制三筆順序及 slug lookup。
- `timeline/events.json`：不屬於 Experience 的 point/duration Timeline Events。

### `backend/repositories/`

- `common.py` — **runtime shared data access utility**：定義 backend data root、同步讀取 JSON，並將 filesystem mtime 格式化為 `updated_at`；不包含 resource logic。
- `about_repository.py` — **runtime data access**：管理 About JSON path，回傳 raw About data 與 timestamp。
- `experience_repository.py` — **runtime data access**：管理 Experience directory、動態掃描 `*.json`，並維持既有 `start_date` descending ordering 與最新 timestamp。
- `project_repository.py` — **runtime data access**：管理 Project directory、固定 slug/file mapping、list ordering 與 single-project lookup。
- `timeline_repository.py` — **runtime data access**：管理 Timeline Events JSON path，回傳 raw event data 與 timestamp。
- `content_repository.py` 已移除；目前沒有 wrapper、dead function 或 runtime consumer。
- Repository 不進行 Pydantic validation；validation 位於 service layer。

### `backend/services/`

- `about_service.py` — **runtime application/content layer**：讀取並驗證 About，組裝 About v1 response 與 timestamp metadata。
- `experience_service.py` — **runtime application/content layer**：驗證 Experience list、依 `start_date` descending 確保排序，並組裝 Experience v1 response。
- `project_service.py` — **runtime application/content layer**：驗證 Project list、保留 repository ordering，並處理 slug lookup 與 404。
- `timeline_service.py` — **runtime application/content layer**：驗證 Point／Duration Timeline Events，組裝 Timeline v1 response。
- `content_service.py` 已移除；目前沒有 legacy response helper 或集中式 service runtime consumer。

### `backend/schemas/`

- `common.py` — **runtime validation/serialization**：`Meta`、通用 `ApiResponse`。
- `about.py` — **runtime validation/serialization**：About section、data 與 response models。
- `experience.py` — **runtime validation/serialization**：Experience item、list data 與 response models。
- `project.py` — **runtime validation/serialization**：Project summary/detail nested models、showcase、challenge、item、data 與 response。
- `timeline.py` — **runtime validation/serialization**：Point／Duration Timeline Event models、discriminated union、data 與 response。
- `content.py` 已移除；目前沒有 compatibility wrapper、dead model 或 runtime consumer。
- Resource schemas 同時供 runtime services/routers 與 content validation tooling 使用。

### `backend/routers/`

- `routers/v1/about.py` — **runtime HTTP routing**：只處理 `GET /api/v1/about`。
- `routers/v1/experience.py` — **runtime HTTP routing**：只處理 `GET /api/v1/experience`。
- `routers/v1/projects.py` — **runtime HTTP routing**：處理 Project collection 與 slug endpoints。
- `routers/v1/timeline.py` — **runtime HTTP routing**：只處理 `GET /api/v1/timeline-events`。
- `routers/v1/health.py` — **runtime HTTP routing**：只處理 `GET /api/v1/health`。
- 各 `__init__.py` 只標記 Python package。

### `backend/scripts/`

- `validate_content_schema.py` — **validation/tooling**：
  - 掃描 `backend/data/**/*.json`。
  - 驗證 About、Experience、Projects、Timeline Events。
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
│   │   ├── ExperienceView.vue
│   │   └── ProjectView.vue
│   ├── components/
│   │   ├── about/
│   │   │   └── AboutSection.vue
│   │   ├── experience/
│   │   │   ├── HomeJourneyItem.vue
│   │   │   ├── JourneySection.vue
│   │   │   ├── JourneyDetail.vue
│   │   │   └── Timeline.vue
│   │   ├── layout/
│   │   │   └── DetailPageHeader.vue
│   │   └── projects/
│   │       ├── HomeProjectPreview.vue
│   │       ├── ProjectAction.vue
│   │       ├── ProjectCard.vue
│   │       └── ProjectCover.vue
│   ├── composables/
│   │   ├── useMouseGlow.js
│   │   └── useScrollProxy.js
│   ├── utils/
│   │   ├── experienceLogos.js
│   │   └── projectSearch.js
│   ├── data/home/
│   │   ├── about.json
│   │   ├── experiences.json
│   │   └── projects.json
│   └── assets/
│       ├── css/
│       │   ├── main.css
│       │   ├── main-rwd.css
│       │   ├── about.css
│       │   ├── about-rwd.css
│       │   ├── exp.css
│       │   ├── exp-rwd.css
│       │   ├── projects.css
│       │   └── projects-rwd.css
│       └── images/exp/
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
- `src/App.vue` — **runtime application shell**：依 route meta 切換 Home／Detail layout；包含首頁 Sidebar、navigation、social links、Last updated API request、RouterView 與 mobile footer。
- `src/router/index.js` — **runtime routing**：history-mode `/`、`/about`、`/experience`、`/project`；route meta 指定 layout；route change 回到頂部。沒有 catch-all 404 route。

### Views

- `HomeView.vue` — **Home-only**：直接 import 三份 frontend local preview JSON，組裝 Profile、Journey、Projects previews。
- `AboutView.vue` — **About-only**：透過 `getAbout()` 載入 sections，處理 loading/error/empty/success，交給 `AboutSection` render。
- `ExperienceView.vue` — **Journey-only orchestration**：載入 Experience + Timeline Events、管理 active/expanded/leaving states、計算 Grid rows、協調 Timeline、JourneySection、JourneyDetail 與 dynamic-height transition。
- `ProjectView.vue` — **Projects-only orchestration**：載入 Projects、管理 search/filter/empty state 與單一 expanded slug，render ProjectCard list。

### Components

#### `components/about/`

- `AboutSection.vue` — **About page-specific**：顯示單一 API section 的 heading、paragraphs、optional items；無 API 或 state ownership。

#### `components/experience/`

- `HomeJourneyItem.vue` — **Home-specific**：精簡 Journey preview row。
- `JourneySection.vue` — **Experience page-specific**：永遠可見的 Experience header、logo、summary、metadata、More/Less toggle；不知道 Timeline。
- `JourneyDetail.vue` — **Experience page-specific**：展開後的 description、responsibilities、highlights、projects、skills/technologies、additional details；不知道 Timeline 或 expanded state。
- `Timeline.vue` — **Experience page-specific**：render Experience periods、date labels、nodes、active segments、connectors 與 static Timeline Events；接收 View 計算的 row mapping，不 render Journey content。

#### `components/projects/`

- `HomeProjectPreview.vue` — **Home-specific**：精簡 Project preview row，組合 ProjectCover、ProjectAction。
- `ProjectCard.vue` — **Project page-specific**：Project summary header、detail sections、dynamic-height transition 與 toggle events。
- `ProjectCover.vue` — **cross-page shared**：Home／Project Page 共用 160×100、16:10 image/placeholder/error fallback。
- `ProjectAction.vue` — **cross-page shared**：依 website/source URLs render Live、Source 或 non-clickable Internal。

#### `components/layout/`

- `DetailPageHeader.vue` — **detail-page shared**：About、Experience、Project 共用 breadcrumb、唯一 page `h1` 與 description。

### API layer

- `api/client.js`：
  - `requestRaw(path)` 組合 `VITE_API_BASE`、執行 Fetch、解析 JSON、正規化 API errors。
- `api/contentApi.js`：About、Experience、Timeline Events、Projects 的 feature-facing functions；將 v1 envelope 轉為 `{content, updatedAt}`。

### Composables and utilities

- `useMouseGlow.js`：全域 mousemove cursor glow；由 `App.vue` 使用。
- `useScrollProxy.js`：首頁 wheel event 轉送到 `.main-content`；由 `App.vue` 使用。
- `ProjectCard.vue` 的 `safeArray` 是其 detail template 專用 local helper；沒有建立只有單一 consumer 的 composable 或 utility。
- `experienceLogos.js`：backend logo filename 到 Vite image imports 的固定 mapping。
- `projectSearch.js`：Project public text collection、whole-token search、exact filters、dynamic option sorting。

### Frontend data and assets

- `data/home/*.json` — **runtime local preview data**：首頁 About、Journey、Projects；不經 backend。
- `assets/images/exp/*.png` — **bundled runtime assets**：Journey logos。
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

### Experience

```text
backend/data/portfolio/experience/*.json
  → experience_repository.read_experiences_with_timestamps()
  → experience_service ExperienceItem validation + response aggregation
  → GET /api/v1/experience
  → frontend api/contentApi.getExperience()
  → ExperienceView.vue
  → JourneySection.vue + JourneyDetail.vue + Timeline.vue
```

Experience service 依 `start_date` descending 確保 response order；repository 目前也維持相同既有讀取順序。Logo 圖片由 frontend `experienceLogos.js` 另行映射。

### Timeline Events

```text
backend/data/portfolio/timeline/events.json
  → timeline_repository.read_timeline_events_with_timestamp()
  → timeline_service TimelineEventsData discriminated-union validation
  → GET /api/v1/timeline-events
  → frontend api/contentApi.getTimelineEvents()
  → ExperienceView.vue
  → Timeline.vue
```

Timeline Events 不建立 Journey Section/Detail；位置由 Timeline 依 Experience date bounds 計算。

### Projects

```text
backend/data/portfolio/projects/*.json
  → project_repository fixed PROJECT_FILES mapping
  → project_service ProjectItem validation + list/slug response handling
  → GET /api/v1/projects
  → frontend api/contentApi.getProjects()
  → ProjectView.vue
  → ProjectCard.vue
  → ProjectCover.vue + ProjectAction.vue
```

首頁 Projects 不走此流程，而是讀取 `frontend/src/data/home/projects.json` 的 preview-only summary。

## API Structure

Backend resource routes 分別定義在 `backend/routers/v1/` 的 `about.py`、`experience.py`、`projects.py`、`timeline.py` 與 `health.py`；content HTTP API 僅保留 v1 surface。

### Versioned endpoints

| Endpoint | Response model | Frontend usage |
|---|---|---|
| `GET /api/v1/about` | `AboutResponse` | `AboutView.vue`；`App.vue` Last updated |
| `GET /api/v1/experience` | `ExperienceResponse` | `ExperienceView.vue` |
| `GET /api/v1/timeline-events` | `TimelineEventsResponse` | `ExperienceView.vue` |
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
| `main.css` | Design tokens、Home/Detail application layout、Sidebar、navigation、social links、detail container、shared page state、shared tags |
| `main-rwd.css` | Main layout Desktop/Laptop/Tablet/Mobile rules、Home Sidebar/footer behavior |
| `about.css` | Home Profile typography + `/about` sections、paragraphs、items |
| `about-rwd.css` | About/Home Profile responsive typography and spacing |
| `exp.css` | Home Journey preview + `/experience` Timeline、events、Section、Detail、transitions |
| `exp-rwd.css` | Journey/Timeline/Home preview responsive behavior；Mobile hides Timeline |
| `projects.css` | Home Project preview + `/project` cards、cover/action、details、search/filter toolbar |
| `projects-rwd.css` | Project preview/cards/tools responsive layouts |

CSS import order is part of current behavior. Feature files contain both Home and Detail styles, so selectors are namespaced by convention rather than module/scoped isolation.

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

- **Global CSS coupling**：八個 custom CSS 全域載入，約 2,200 行；Home/detail feature styles 混在同一檔案並依 cascade/import order 生效。
- **Large orchestration files**：`ExperienceView.vue`、`Timeline.vue`、`ProjectCard.vue` 都超過 200 行，同時負責多種狀態、rendering 或 transition concerns。
- **App shell coupling**：`App.vue` 同時管理 layout、Sidebar、navigation、social links、Last updated、DOM measurements、hash scrolling 與 RouterView。
- **No frontend stores/types/tests**：沒有 store、TypeScript types、unit/component/E2E test directories；資料 shape 主要由 backend schema、JSON 與 runtime property access約束。
- **API naming**：frontend 沒有 `services/`；`contentApi.js` 實際扮演 service layer，而 `client.js` 保留唯一使用中的 low-level `requestRaw()` transport。
- **Synchronous JSON I/O**：每個 content request 都同步開檔、parse JSON、validate；沒有 cache。
- **Duplicated content responsibility**：首頁三份 local preview JSON 與 backend detail summary 需人工同步，可能產生文案、links、tags 漂移。
- **Rich HTML handling**：首頁 About preview 與 Experience detail 使用 `v-html`；沒有 frontend sanitization layer。
- **Router gaps**：沒有 catch-all 404 route；route URLs 使用既有 singular `/experience`、`/project` naming。
- **Build/deployment debt**：images 只推 mutable `latest` tag；Node build image 仍使用未固定 patch 的 `node:20`。
- **Environment configuration**：frontend environment files被 tracked，API base 在 build time寫入 bundle；任何環境切換都需 rebuild。
- **Documentation duplication**：root 有多份中英文 architecture/features/system-design/TODO 文件，內容可能彼此或與 runtime code不同步。
- **Generated local artifacts**：workspace 可見 `backend/venv/`、`__pycache__/`、`.DS_Store`，目前均未 tracked；仍可能增加掃描噪音。

## Refactor Candidates

這些是未來候選方向，不代表已核准的 implementation plan。

### Priority High

1. 建立 frontend/backend contract tests，覆蓋四組 v1 responses、404/error envelope 與 JSON validation。
2. 為 About、Journey、Projects 建立最小 component/E2E regression tests，保護 loading/error/empty/expanded/filter states。
3. 建立 CSS ownership/token inventory，逐步隔離 Home 與 Detail feature selectors，降低全域 cascade 風險。
4. 為 `v-html` content 建立可信來源規範與 sanitization policy。

### Priority Medium

1. 拆分大型 Journey Timeline 計算、row orchestration 與 transition concerns，保留目前元件責任邊界。
2. 將 Project detail section rendering與 transition hooks從 `ProjectCard.vue` 適度拆分，但維持 card API。
3. 決定首頁 preview 與 backend summary 的 single-source-of-truth 或產生流程。
4. 補齊 request timeout、abort 與 non-JSON error handling。
5. 清理 placeholder directories/files。

### Priority Low

1. 抽出 Home/Detail layout components，降低 `App.vue` DOM responsibilities。
2. 補 catch-all 404 page 與 route-level metadata/SEO management。
3. 評估 TypeScript 或 runtime prop/schema validation策略，不應與 UI refactor綁定一次完成。
4. 收斂重複 root documentation，指定 `overview.md`、`structure.md` 與 feature specs的更新責任。
5. 改善 Docker reproducibility、immutable image tags、rollback artifacts與 production observability。
