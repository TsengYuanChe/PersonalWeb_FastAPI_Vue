# 專案現況總覽與大幅改版前風險盤點

> 盤點日期：2026-07-26  
> 盤點範圍：實際檢查 repository 內的前端、後端、內容資料、Docker、Nginx、GitHub Actions、環境檔與既有技術文件；排除生成物 `frontend/node_modules/`、`backend/venv/`、`__pycache__/` 與 `.DS_Store` 的內部內容。  
> 文件目的：讓未讀過程式碼的工程師可快速建立正確心智模型，並作為後續大幅改版的規劃基線。

## 0. 閱讀標記

- **【已確認】**：可由目前 repository 的程式碼、設定或資料檔直接證明。
- **【推測】**：依程式碼結構、命名或文件推導，尚未由執行環境、雲端後台或產品負責人確認。
- **【文件宣稱】**：既有 Markdown 或頁面文字所述，但本次無法僅靠 repository 驗證外部狀態。

## 1. 一頁摘要

### 1.1 網站定位與功能

**【已確認】** 目前是 Adam Tseng／Yuan-Che Tseng 的英文個人軟體工程作品集，核心訊息是 Full-Stack、Cloud、Backend API、資料庫、部署自動化與工程經驗。主要受眾沒有寫在 UI 中，但內容明顯以求職作品展示為主。

**【已確認】** 實際網站只有一個可見的長捲動頁面，包含：

1. 左側個人簡介與區段導覽。
2. Profile（About）段落。
3. Experiences 經歷卡片。
4. Projects 專案卡片。
5. 網站技術棧說明。
6. GitHub、LinkedIn、Instagram、Facebook 與履歷 PDF 外部入口。
7. 桌面版滑鼠光暈、平滑捲動、卡片／標籤 hover；手機版固定 Header 與固定 Footer。

**【已確認】** 頁面內容不是寫死在 Vue template（網站標題、側欄文案、社群 URL 與技術棧說明除外），About、Experiences、Projects 會在瀏覽器 mount 後，從 FastAPI 的三個 v1 endpoint 依序取得。

**【推測】** 本次大改版的主要價值會是把現有「單一巨型根元件 + 分散 CSS + imperative DOM 操作」重整成可擴充的頁面／區塊／共用元件架構，同時補齊 loading、錯誤處理、SEO、測試與部署安全性。

### 1.2 關鍵架構圖

```text
Browser
  │
  ├─ GET / 及靜態資源
  ▼
Cloud Run: vue-frontend
Nginx :8080 → Vite build 的 SPA 檔案
  │
  ├─ 瀏覽器依 VITE_API_BASE 跨來源呼叫
  ▼
Cloud Run: fastapi-backend
Uvicorn :8080 → FastAPI
  │ router → service → repository
  ▼
backend/data/**/*.json（無資料庫）
```

**【已確認】** 前、後端是兩個獨立 container、兩個獨立 GitHub Actions workflow 與兩個 Cloud Run service；production API URL 在前端建置時由 `frontend/.env.production` 編入 bundle。

## 2. 技術棧與重要套件

### 2.1 前端

| 技術／套件 | 版本或範圍 | 實際用途 | 位置 |
|---|---:|---|---|
| Vue | `^3.5.18` | Composition API、reactive state、template rendering | `frontend/package.json`, `frontend/src/App.vue` |
| Vue Router | `^4.5.1` | 註冊 history-mode `/` route；但目前沒有渲染 `<router-view>` | `frontend/src/router/index.js`, `frontend/src/main.js` |
| Vite | `^7.0.6` | 開發伺服器與 production bundle | `frontend/vite.config.js` |
| Bootstrap | `^5.3.7` | Grid/flex、spacing、typography、顏色等 utility classes | `frontend/src/main.js`, `frontend/src/App.vue` |
| Bootstrap Icons | `^1.13.1` | 社群、履歷、GitHub、Demo icon | 同上 |
| Fetch API | 瀏覽器內建 | 正式內容 API client | `frontend/src/api/client.js` |
| Axios | `^1.11.0` | 只被未實際渲染的舊 `Home.vue` 使用 | `frontend/src/views/Home.vue` |
| Vue DevTools Vite plugin | `^8.0.0` | 開發工具 plugin；目前沒有按 mode 限制 | `frontend/vite.config.js` |
| ESLint / eslint-plugin-vue | `9.x` / `~10.3.0` | JS/Vue lint；package script 會自動 `--fix` | `frontend/eslint.config.js`, `frontend/package.json` |
| Prettier | `3.6.2` | 格式化 `src/` | `frontend/.prettierrc.json` |

**【已確認】** `package-lock.json` 存在，但 Dockerfile 使用 `npm install` 而非 `npm ci`，所以容器安裝結果不如 lockfile 驅動的 frozen install 嚴格可重現。

### 2.2 後端

| 技術／套件 | 固定版本 | 實際用途 | 位置 |
|---|---:|---|---|
| Python | image `3.13.9` | backend runtime | `backend/Dockerfile` |
| FastAPI | `0.122.0` | HTTP API、OpenAPI、自訂 exception handler、CORS | `backend/main.py` |
| Uvicorn | `0.38.0` | ASGI server | `backend/Dockerfile` |
| Pydantic | `2.12.5` | v1 response model 與 JSON schema validation | `backend/schemas/`, `backend/scripts/validate_content_schema.py` |
| Starlette | `0.50.0` | FastAPI 基礎、CORS 與 HTTP exception | `backend/main.py` |
| python-multipart | `0.0.20` | 已安裝，但目前 endpoint 沒有表單／檔案上傳 | `backend/requirements.txt` |

其餘 `requirements.txt` 項目大多是上述框架的直接或間接 runtime dependency。**【已確認】** 專案名稱雖為 `PersonalWeb_Flask_Vue`，目前 backend 並未使用 Flask。

### 2.3 資料庫與資料持久化

**【已確認】** 目前沒有 application database、ORM、migration、連線字串或 CRUD 寫入 API。內容來源是三份隨 backend image 部署的唯讀 JSON；每次 request 都重新開檔並解析。

**【推測】** `.gitignore` 中的 SQLite 規則是通用 Python ignore，不代表本網站現況有 SQLite。若改版需要 CMS、後台編輯、草稿、排序或即時更新，才需要評估資料庫或 headless CMS。

## 3. 目錄結構

以下只列出有架構意義的檔案；虛擬環境、dependency、cache 與作業系統 metadata 不逐項展開。

```text
PersonalWeb_Flask_Vue/
├── .github/workflows/
│   ├── frontend-deploy.yml       # 前端：建 image、推 Artifact Registry、部署 Cloud Run
│   └── backend-deploy.yml        # 後端：schema 驗證後建置與部署
├── backend/
│   ├── main.py                   # FastAPI app、CORS、router、錯誤處理、根路由
│   ├── core/
│   │   ├── config.py             # 尚未實作的設定 placeholder
│   │   └── logging.py            # 尚未實作的 logging placeholder
│   ├── routers/v1/
│   │   ├── content.py            # legacy 與 v1 content endpoints
│   │   └── health.py             # health endpoint
│   ├── services/content_service.py
│   │                              # 組裝 legacy/v1 response envelope
│   ├── repositories/content_repository.py
│   │                              # 從 data/ 讀 JSON 與檔案 mtime
│   ├── schemas/
│   │   ├── common.py             # Meta、通用 ApiResponse
│   │   └── content.py            # About、Experience、Project schemas
│   ├── data/
│   │   ├── profile/about.json
│   │   ├── profile/experience.json
│   │   ├── portfolio/projects.json
│   │   └── content/.gitkeep      # 預留但未使用的 namespace
│   ├── scripts/validate_content_schema.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── setup.md                  # 本機／手動 GCP 操作筆記
├── frontend/
│   ├── index.html                # SPA HTML shell、favicon、title
│   ├── src/
│   │   ├── main.js               # Vue app bootstrap、router 與全域 CSS import
│   │   ├── App.vue               # 目前所有實際可見 layout 與 section
│   │   ├── views/Home.vue        # 舊測試頁；router 指向它但實際未渲染
│   │   ├── router/index.js       # 唯一 `/` route
│   │   ├── api/
│   │   │   ├── client.js         # fetch + error/envelope normalization
│   │   │   └── contentApi.js     # about/experience/projects API functions
│   │   ├── composables/          # 資料、專案篩選、捲動、光暈、手機 footer
│   │   └── assets/
│   │       ├── css/              # main/about/exp/projects 及各自 RWD CSS
│   │       └── images/exp/       # 三張經歷 logo
│   ├── public/
│   │   ├── files/Adam_Tseng_Resume.pdf
│   │   └── favicon*              # 原樣複製至 build root
│   ├── .env.development          # 本機 FastAPI base URL
│   ├── .env.production           # deployed FastAPI base URL
│   ├── package.json / package-lock.json
│   ├── vite.config.js            # Vue + devtools + `@` alias
│   ├── eslint.config.js / .prettierrc.json / .editorconfig
│   ├── Dockerfile                # Node build stage + Nginx runtime stage
│   ├── nginx.conf                # :8080 與 SPA fallback
│   └── setup.md                  # 本機／手動 GCP 操作筆記
├── AGENTS.md                     # 本 repository 的 agent／產品方向規範
├── README.md                     # 僅一行，不能代表真實架構
├── ARCHITECTURE*.md              # 既有中英文架構文件
├── FEATURES*.md                  # 既有中英文功能文件
├── SYSTEM_DESIGN*.md             # 既有中英文設計文件
├── PROJECT_DOCS.md               # 既有專案說明
├── TODO.md / TODO_Layout.md       # 技術與 layout 待辦
└── overview.md                   # 本文件
```

## 4. 頁面、路由、區段、元件與資料來源

### 4.1 真正的頁面與 URL route

| URL / route | 程式位置 | 實際狀態 | 內容來源 |
|---|---|---|---|
| `/`（及 Nginx fallback 到 SPA 的任意前端 path） | `frontend/src/App.vue` | 唯一實際顯示頁面 | static template + 三個 v1 API |
| Vue Router `/`, name `Home` | `frontend/src/router/index.js` → `frontend/src/views/Home.vue` | **已註冊但未渲染**；`App.vue` 沒有 `<router-view>` | 舊的 hard-coded `http://127.0.0.1:5000/api/index` |
| `#about`, `#exp`, `#projects` | `frontend/src/App.vue` | DOM section selector，不是 router route；點擊時對 `.main-content` smooth scroll | 見下表 |
| `#stack` | `frontend/src/App.vue` | 有 section id，但 navigation 未提供入口 | template hard-coded |

**【已確認】** `createWebHistory(import.meta.env.BASE_URL)` 已建立，但目前 router 不影響畫面。Nginx `try_files $uri /index.html` 已支援未來 history-mode route refresh。

### 4.2 頁面區塊與主要 UI

| 區塊 | 主要 DOM／邏輯 | 資料來源 | 重要行為／依賴 |
|---|---|---|---|
| 全域 Shell | `.cursor-glow`, `.app-wrapper`, `.layout-container` | CSS + template | 桌面二欄 layout；光暈由 `useMouseGlow()` 直接更新 transform |
| Sidebar / Header | 姓名、職稱、簡介、Navigation | 全部 hard-coded in `frontend/src/App.vue` | 桌面為左欄；≤768px 變 fixed mobile header |
| Navigation | ABOUT / EXPERIENCES / PROJECTS | hard-coded | `useSmoothScroll()` 查詢 `.main-content` 與 section selector |
| Social / Resume / Last Updated | 五個外部／檔案連結、日期 | URL hard-coded；日期取三個 API `meta.updated_at` 的最新日期 | `useMobileFooter()` 在手機複製 sidebar HTML 並注入新 DOM |
| Profile | `aboutData.paragraphs` | `GET /api/v1/about` → `backend/data/profile/about.json` | 以 `v-html` render 每段 HTML |
| Experiences | `expData.experience` cards | `GET /api/v1/experience` → `backend/data/profile/experience.json` | details 用 `v-html`；logo filename 映射至 `src/assets/images/exp/` |
| Projects | `displayProjects` cards | `GET /api/v1/projects` → `backend/data/portfolio/projects.json` | 顯示第一個 featured + 前兩個 normal；featured 顯示完整欄位，normal 只預覽前兩項 engineering |
| See more projects | button/link | hard-coded GitHub repositories URL | 新分頁外連 |
| Tech Stack | 一段說明文字 | hard-coded template | 宣稱 Vue/FastAPI/Docker/Cloud Run/GitHub Actions |

### 4.3 Vue 元件現況

**【已確認】** 沒有 `src/components/`，也沒有拆出的 Header、Footer、Layout、Card、Tag、Button 等 Vue 共用元件。所有實際 markup 集中在 `frontend/src/App.vue`（279 行）。Bootstrap utilities 與 CSS class 是目前唯一的 UI reuse 機制。

Composables：

- `usePageData.js`：依序抓三個 API、保存四組 refs、挑最新日期、組 logo URL。
- `useProjectHelpers.js`：array guard、featured 判斷、normal engineering preview、link accessor。
- `useProjectView.js`：決定只顯示 1 featured + 2 normal。
- `useSmoothScroll.js`：對內層 `.main-content` 做 smooth scroll。
- `useScrollProxy.js`：攔截整個 window 的 wheel、`preventDefault()`，再代理到 `.main-content`。
- `useMouseGlow.js`：監聽 window mousemove，直接操作 `.cursor-glow`。
- `useMobileFooter.js`：用 `matchMedia`、`innerHTML`、DOM append/remove 建立手機 footer。

## 5. 全域樣式、視覺系統、RWD 與動畫

### 5.1 樣式載入順序

**【已確認】** `frontend/src/main.js` 依序載入 Bootstrap、Bootstrap Icons，再載入：

1. `main.css`
2. `main-rwd.css`
3. `projects.css`
4. `projects-rwd.css`
5. `about.css`
6. `about-rwd.css`
7. `exp.css`
8. `exp-rwd.css`

所有自訂 CSS 都是 global，沒有 `<style scoped>`、CSS Modules、Sass 或 CSS-in-JS。

### 5.2 顏色與字體

核心 root tokens 只有三個：

| Token | 值 | 用途 |
|---|---|---|
| `--site-bg` | `#0c1a2b` | body、layout、sidebar、main 深藍背景 |
| `--site-text` | `#e4e9f0` | 主文字 |
| `--site-secondary` | `#8fa3bd` | 次要文字 |

其餘顏色直接散落於 CSS：navigation / action blue（如 `#0d6efd`, `#1e88ff`）、project cyan/green、experience purple，以及大量白色 alpha、陰影與 glass-like background。

**【已確認】** 專案沒有自訂 `font-family`、`@font-face` 或 web font；實際字體沿用 Bootstrap 的 system font stack。HTML 的 `lang` 是空字串，title 是 `Adam's Website`，未見 meta description、Open Graph 或結構化資料。

### 5.3 Layout 與 breakpoints

| 範圍 | 行為 |
|---|---|
| `>1024px` | `.layout-container` 固定 `1300px × 100vh`、grid columns `280px 1fr`；sidebar 自身寬 `350px`；main 內層捲動 |
| `≤1024px` | container 改 `width: 100%`；about/experience/project typography 與 padding 部分縮小 |
| `≤768px` | grid 改 block；sidebar 變 fixed header；JS 注入 fixed footer；main 高度依 JS CSS variables 計算並內層捲動；隱藏 cursor glow |

**【已確認】** 僅有 1024px 與 768px 兩組 max-width breakpoints。JS 也使用 `max-width: 768px`。`App.vue` runtime 設定 `--header-height`、`--footer-height`、`--real-vh`。

**【已確認且需注意】** `main.css` 的 grid column 是 280px，但 `.sidebar` width 是 350px；既有 `TODO_Layout.md` 把「unify shell width model」標為完成，但現況程式仍保留固定 1300px 與不一致的 280/350px。該 TODO 狀態與程式碼不一致。

### 5.4 動畫與互動

- HTML `scroll-behavior: smooth`，navigation 另使用 `scrollTo({ behavior: 'smooth' })`。
- navigation、social icon、tooltip、experience card、project card、buttons、skills/tags 使用 0.2–0.3s CSS transitions 與位移／縮放。
- 400×400px cursor glow 每次 mousemove 更新 transform，CSS transition 0.008s；手機隱藏。
- 手機 CSS 關閉 project card 與 tag 的強位移 hover，但沒有全域 `prefers-reduced-motion`。
- 沒有 CSS `@keyframes`。

## 6. 資料與靜態資產位置

| 類型 | 位置 | 消費者／備註 |
|---|---|---|
| About JSON | `backend/data/profile/about.json` | `/api/about`, `/api/v1/about`; 內含允許直接 render 的 HTML |
| Experience JSON | `backend/data/profile/experience.json` | legacy/v1 experience endpoints；logo 欄位對應前端檔名 |
| Projects JSON | `backend/data/portfolio/projects.json` | legacy/v1 projects endpoints；目前 5 筆，UI 只顯示 3 筆 |
| Experience logo | `frontend/src/assets/images/exp/{ezoom,nchu,nycu}.png` | 經 Vite asset URL 使用 |
| Resume | `frontend/public/files/Adam_Tseng_Resume.pdf` | 瀏覽器 `/files/Adam_Tseng_Resume.pdf`，1 頁 PDF |
| Favicon | `frontend/public/favicon*` | `frontend/index.html` |
| UI hard-coded content | `frontend/src/App.vue` | identity、職稱、sidebar 文案、nav、social URL、tech-stack 文案 |
| 舊 mock-like API URL | `frontend/src/views/Home.vue` | 指向 Flask-style localhost:5000；實際未接線 |

**【已確認】** 沒有前端本地 JSON、mock server、uploads 目錄、analytics SDK 或第三方 CMS。圖片不由 backend API 回傳；API 只回 logo filename。

## 7. Backend API 完整盤點

### 7.1 Endpoints

所有 application endpoints 都是無認證、無 query/path parameter、無 request body 的 `GET`。

| Method | Path | Response | Model / 備註 |
|---|---|---|---|
| GET | `/` | `{"msg":"FastAPI backend running!"}` | 無 response model |
| GET | `/health` | `{"status":"ok"}` | Cloud Run workflow 未設定 health probe，但可供外部檢查 |
| GET | `/api/about` | 原始 About object + top-level `updated_at` | legacy；無 Pydantic response model |
| GET | `/api/experience` | 原始 Experience object + `updated_at` | legacy |
| GET | `/api/projects` | 原始 Projects object + `updated_at` | legacy |
| GET | `/api/v1/about` | `{data, meta}` | `AboutResponse` |
| GET | `/api/v1/experience` | `{data, meta}` | `ExperienceResponse` |
| GET | `/api/v1/projects` | `{data, meta}` | `ProjectsResponse` |
| GET | `/openapi.json` | generated OpenAPI schema | FastAPI 預設，未關閉 |
| GET | `/docs` | Swagger UI | FastAPI 預設，未關閉 |
| GET | `/redoc` | ReDoc UI | FastAPI 預設，未關閉 |

### 7.2 v1 response envelope

```json
{
  "data": "resource-specific object",
  "meta": {
    "updated_at": "YYYY-MM-DD HH:MM:SS",
    "version": "v1"
  }
}
```

`updated_at` 是 container filesystem 中 JSON 檔的 local-time mtime，不是資料內明確維護的發布時間。前端只顯示日期部分，並取三個 resource 的最大值。

### 7.3 Resource models / schemas

```text
AboutData
└── paragraphs: string[]

ExperienceData
└── experience: ExperienceItem[]
    ├── details: string[]
    ├── duration: string
    ├── location: string
    ├── position: string
    ├── skills: string[]
    ├── logo?: string | null
    └── gpa?: string | null

ProjectData
└── projects: ProjectItem[]
    ├── title: string
    ├── type: "featured" | "normal"
    ├── category: string
    ├── overview: string
    ├── features: string[] = []
    ├── engineering: string[] = []
    ├── architecture: string
    ├── tradeoffs: string[] = []
    ├── future: string[] = []
    ├── tech: string[]
    └── links: { github?: string | null, demo?: string | null }
```

定義位置：`backend/schemas/common.py`、`backend/schemas/content.py`。`ApiResponse.data` 的 base type 是 `Any`，各 concrete response subclass 再覆寫成特定 data model。

### 7.4 Error response

```json
{
  "error": {
    "code": "CONTENT_NOT_FOUND | NOT_FOUND | HTTP_<status> | INTERNAL_ERROR",
    "message": "human-readable message",
    "details": null
  }
}
```

- JSON 檔不存在：404 / `CONTENT_NOT_FOUND`。
- HTTP 404：404 / `NOT_FOUND`；其他 HTTPException：原 status / `HTTP_<status>`。
- 未處理 exception（包含 malformed JSON）：500 / `INTERNAL_ERROR`。
- 前端 `requestRaw()` 會先呼叫 `res.json()`；如果 proxy／server 回非 JSON，會在狀態判斷前拋出 JSON parse error。

### 7.5 Backend layering 與資料流

```text
backend/main.py
  → routers/v1/content.py
    → services/content_service.py
      → repositories/content_repository.py
        → backend/data/<relative path>.json
```

**【已確認】** v1 route 有 response validation；legacy route 沒有。schema validation script 會掃描 `backend/data/**/*.json`，未知 JSON、缺少預期 JSON 或 schema mismatch 都會使 CI 失敗。

## 8. 環境變數與環境設定

### 8.1 Frontend

| Mode | 檔案 | 變數用途 |
|---|---|---|
| development | `frontend/.env.development` | `VITE_API_BASE` 指向本機 `127.0.0.1:8000` |
| production | `frontend/.env.production` | `VITE_API_BASE` 指向已命名的 Cloud Run FastAPI HTTPS URL |

本文件刻意不重錄實際 production URL；它目前並非 secret，但屬部署綁定資訊。Vite 的 `VITE_*` 變數會進入瀏覽器 bundle，不能存 secret。

**【已確認】** API base 是 build-time config，不是 Nginx／Cloud Run runtime substitution。修改 backend URL 必須重新 build/deploy frontend。未設定時會組出 `undefined/api/...`。

### 8.2 Backend 與 CI/CD secrets

**【已確認】** backend application 本身沒有讀取 `.env` 或任何環境變數；Dockerfile 雖宣告 `PORT=8080`，啟動命令仍 hard-code `--port 8080`。

GitHub Actions 引用但 repository 內未存值的 secrets：

- `GCP_SA_KEY`：Google Cloud service account credential JSON。
- `GCP_PROJECT_ID`：GCP project identifier。
- `CLOUD_RUN_REGION`：Cloud Run deployment region。

**【已確認】** Artifact Registry hostname／region 在 workflow hard-code 為 `asia-east1-docker.pkg.dev`；Cloud Run region 則由 secret 決定。Frontend production API URL 所示 backend region 與 Artifact Registry region 不同；這本身可行，但需要確認是否為刻意配置。

## 9. 建置、啟動、測試與部署

### 9.1 本機啟動

Frontend（於 `frontend/`）：

```bash
npm install
npm run dev
```

Backend（於 `backend/`，先安裝 `requirements.txt`）：

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

兩者需同時啟動；`.env.development` 會讓瀏覽器向 port 8000 取內容。

### 9.2 Build / lint / content validation

```bash
# frontend/
npm run build
npm run preview
npm run lint        # 注意：此 script 帶 --fix，會修改檔案
npm run format      # 會改寫 src/

# repository root
python backend/scripts/validate_content_schema.py
```

**【已確認】** 沒有 unit/integration/E2E test framework、test files、coverage script 或 frontend test script。唯一自動驗證是 backend JSON-to-Pydantic schema script。

本次盤點實際驗證：

- `backend/venv/bin/python backend/scripts/validate_content_schema.py`：三份 JSON 均 PASS。
- `npm exec -- eslint .`：執行超過 60 秒仍無任何輸出且未結束，本次中止；因此不能宣稱 lint 通過或失敗，需另查本機 dependency/process 狀態。
- 為遵守「不修改既有檔案」要求，未執行帶 `--fix` 的 `npm run lint`。

### 9.3 Containers

- Frontend `frontend/Dockerfile`：`node:20` builder → `npm install` → Vite build → `nginx:stable-alpine-slim`；Nginx 監聽 8080，提供 SPA fallback。
- Backend `backend/Dockerfile`：`python:3.13.9` → pip install → copy source → Uvicorn 監聽 0.0.0.0:8080。
- 沒有 root-level Docker Compose；本機整合需分別啟動兩個服務。

### 9.4 自動部署

**【已確認】** push 到 `main` 時依 path filter 獨立觸發：

- `frontend/**` 或 frontend workflow 變更 → frontend workflow。
- `backend/**` 或 backend workflow 變更 → backend workflow。

共同流程：checkout → GCP service-account auth → setup gcloud → configure Artifact Registry Docker auth → build `:latest` → push → `gcloud run deploy`。

Backend 額外先用 Python 3.13 安裝 requirements 並執行 content schema validation。Frontend workflow 沒有 lint、test 或獨立 build verification step（Docker build 內才執行 build）。兩個部署命令都沒有在 workflow 明示 `--allow-unauthenticated`、revision traffic、resource limits、env vars、service account、health checks 或 rollback policy；實際值可能沿用 Cloud Run service 既有設定，需進雲端後台確認。

**【文件宣稱】** 網站部署於 Google Cloud Run，domain 為 `adamtseng.com`。Repository 可確認 workflow 與 project JSON 的 demo URL，但無法確認目前 DNS、custom domain mapping、服務可用性或最新 revision 是否部署成功。

## 10. 已知問題、未完成項目、假資料與技術債

### 10.1 高優先問題

1. **Router 與實際 UI 斷線**：`main.js` 安裝 Vue Router、`/` 指向 `Home.vue`，但 `App.vue` 沒有 `<router-view>`。目前 router 是 dead architecture；`Home.vue` 又呼叫不存在於目前 FastAPI 的 Flask-style `/api/index` port 5000。
2. **API failure 會造成未捕捉錯誤**：`usePageData()` 沒有 try/catch/finally、loading、error 或 fallback；而且三個 request 依序執行，前一個失敗會阻止後續資料載入。
3. **XSS 信任邊界**：About paragraphs 與 experience details 用 `v-html`，JSON 中確實包含 HTML links/strong。內容目前由受控 repository 提供，但若未來接 CMS／使用者輸入而未 sanitize，會形成 stored XSS。
4. **全域 wheel interception**：`useScrollProxy()` 對所有 viewport 一律攔截 window wheel 並 `preventDefault()`；註解與 `TODO_Layout.md` 宣稱應限制／已完成，但實作仍未限制 mobile/touch 或 event target，可能影響 accessibility、nested scroll、trackpad 與 browser 行為。
5. **Mobile footer 直接注入 HTML**：`useMobileFooter()` 複製 `innerHTML`，繞過 Vue virtual DOM，造成 state、event、cleanup、accessibility 與未來 component refactor 風險。
6. **Resize listener 未清除**：`App.vue` 在 `onMounted` 註冊 anonymous-scope `resize` listener，沒有 `onBeforeUnmount` cleanup。現況根元件通常不卸載，因此短期不明顯，但 refactor／HMR／測試時可能累積。
7. **CORS 配置不相容且過寬**：`allow_origins=["*"]` 同時 `allow_credentials=True`；網站目前沒 credentials，但安全語意不清且不應作 production 最終設定。
8. **無前端自動化品質閘門**：CI 沒有 lint/test；本次唯讀 lint 也出現長時間不結束。

### 10.2 Layout / design-system 技術債

- `App.vue` 同時負責 Layout、Header、Footer、Navigation、About、Experience、Projects、Tech Stack 與組裝所有 composables，改任何一區都容易碰到共用 DOM selector／CSS。
- 固定 1300px shell、280px grid column 與 350px sidebar 不一致，main 又有 `padding: 30px 120px`；中等寬度容易 overflow／擠壓。
- 手機 main height 依 DOM 測量與三個 runtime CSS variables；字體、內容、safe area、orientation、dynamic browser chrome 都可能影響計算。
- CSS global 且載入順序敏感；RWD 中大量 `!important`，about/experience/projects 有重複 card/title/tag values。
- design tokens 只有三個顏色，spacing、typography、radius、shadow、motion 未 token 化。
- Bootstrap `.text-secondary` 的 class name 被自訂全域 rule 覆寫，但 Bootstrap 某些 utilities 使用 `!important`，實際 cascade 可能不是作者預期。
- 沒有 `prefers-reduced-motion`；滑鼠光暈 z-index 9999 且每個 mousemove 做 DOM query + layout read (`offsetWidth/Height`)。

### 10.3 Content / product debt

- 頁面沒有獨立 Home/Projects/System Design/Blog/Resume route；所有內容都塞在一頁。AGENTS.md 所要求的 system-design case studies 與可選 blog 尚未成為頁面。
- Project JSON 有 5 筆，但 UI 固定只顯示 3 筆；「See more」直接導向 GitHub，未提供站內完整專案列表。
- `category` 有 schema、有資料，但目前 UI 不顯示。
- normal project 的 features、architecture、tradeoffs、future 雖有完整資料，UI 都不顯示，只預覽兩項 engineering。
- Header 身份文案、社群 URL、網站 tech-stack 文案不在 JSON，改內容需同時找 frontend 與 backend data。
- `position` 中有 `Software Developnment Engineer` 拼字錯誤（來源：`backend/data/profile/experience.json`）。
- `updated_at` 依檔案 mtime，不是 Git commit time 或內容發布時間；container build/copy 行為可能讓日期代表 image 內檔案時間，而非使用者理解的最後更新。
- `Home.vue` 可視為舊測試／假資料接線；但目前沒有真正 mock dataset。
- `backend/data/content/.gitkeep`、`backend/core/config.py`、`backend/core/logging.py` 是未實作 placeholder。

### 10.4 SEO、accessibility 與 security debt

- Client-side mount 後才有主要內容，沒有 SSR/SSG/prerender；搜尋引擎與分享 preview 能力有限。
- `index.html` 缺 `lang` 值、description、canonical、Open Graph、Twitter card、structured data。
- navigation 使用沒有 `href` 的 `<a>`，只靠 click handler；鍵盤、複製連結與無 JS fallback 較弱。
- 外部 `target="_blank"` links 沒有 `rel="noopener noreferrer"`。
- logo alt 固定為 `logo`，缺乏具體替代文字；social icons 主要靠 tooltip，沒有明示 `aria-label`。
- fixed header/footer、內層 scroll container 與全域 wheel proxy 可能影響 focus visibility、鍵盤捲動與 screen reader flow。
- 沒有 CSP、security headers、rate limiting 或 explicit cache headers。

### 10.5 部署與操作 debt

- workflow 只用 mutable `latest` tag，缺 immutable commit SHA tag，追蹤與 rollback 困難。
- frontend production backend URL 編入 tracked `.env.production`，環境切換需要 commit/build；沒有 staging 設定。
- frontend Docker 使用寬泛 `node:20`、`npm install`；backend 使用完整 Python image，均可再提升 reproducibility／image size，但大改版時不宜與 UI 重構一次混做。
- GitHub Actions actions 以 major tag（`@v2`, `@v4`, `@v5`）而非 commit SHA pinning。
- setup 文件含特定 GCP project 操作筆記，且 `frontend/setup.md` 開頭誤放 backend uvicorn 指令；應視為參考，不能當唯一 runbook。

## 11. 高耦合區域與大改版影響面

| 高耦合區 | 為何耦合 | 改動時容易連帶影響 |
|---|---|---|
| `frontend/src/App.vue` | 所有可見 UI 與 composable 組裝都在此 | section DOM id/class、navigation、mobile layout、資料 shape、links |
| DOM selectors + CSS class | composables 用 `.main-content`, `.cursor-glow`, `.sidebar`, `.social-icons`, `.bottom-area`, `.profile-part`, `.mobile-footer` 查 DOM | class rename 看似純樣式改動，實際會破壞 JS 行為 |
| Mobile layout trio | `App.vue` 測量 + `useMobileFooter.js` 注入 + `main-rwd.css` 計算高度 | Header/Footer redesign、內容高度、breakpoint、orientation、scroll |
| JSON ↔ Pydantic ↔ Vue template | 同一欄位跨 data/schema/API/composable/template | 欄位 rename、新 project type、可選欄位、rich text strategy |
| Experience logo mapping | backend JSON 只存 filename，frontend hard-code asset directory | 換 CDN、API image URL、檔名或 Vite asset handling |
| Project selection | `type` literal + `find(featured)` + `slice(0,2)` | 排序、多 featured、專案列表頁、category filter |
| API base / deploy | production URL build-time baked into frontend | backend service rename/region/domain、staging、多環境 |
| Global CSS + Bootstrap | selector specificity與 import order共同決定視覺 | 元件拆分、class rename、Bootstrap 升級、改 design tokens |

## 12. 建議改版順序

以下順序刻意先建立可驗證基線，再處理結構，最後才換視覺；避免同時改 API、layout 與 deployment 後無法定位 regression。

### Phase 0：凍結基線與產品決策

1. 擷取 desktop/tablet/mobile 現況 screenshots，列出主要內容與外連清單。
2. 確認改版 information architecture：維持單頁，或新增 Projects、Project Detail、System Design、Resume 等 routes。
3. 確認內容 ownership：繼續 Git-managed JSON、導入 CMS，或 database/admin。
4. 從 Cloud Run／GitHub 實際確認 domain、regions、public access、secrets、last successful revision 與 rollback 方法。

驗證：baseline screenshots、route/content inventory、外部連結與 resume download 都有人工核對紀錄。

### Phase 1：先補安全網，不改視覺

1. 建立 frontend unit/component tests（至少 API normalization、project selection、loading/error state）。
2. 建立 backend endpoint/contract tests，保留 legacy endpoint 前先確認是否有 consumer。
3. 在 CI 加 frontend `npm ci`、不帶 fix 的 lint、build、tests；backend 加 endpoint tests。
4. 加 smoke test：`/health`、三個 v1 endpoint、frontend root 與 assets。

驗證：乾淨 checkout 可重現安裝、build、schema validation 與 tests；CI 不會自動改檔。

### Phase 2：解開前端結構耦合

1. 先決定 Router：若採多頁，讓 `App.vue` 成為 `<RouterView>` shell；若維持單頁，移除 dead router/Home/axios。
2. 拆出 `AppLayout`, `SiteHeader`, `SiteNav`, `SiteFooter`, `AboutSection`, `ExperienceSection`, `ProjectsSection`, `ProjectCard`, `TagList`。
3. 把手機 footer 改為 Vue declarative rendering，不複製 `innerHTML`。
4. 把 scroll/mouse listeners 變成有 target、有 cleanup、可測試並尊重 reduced motion 的 composables。
5. 補 loading/error/partial-success/retry，三個獨立 API 可平行載入。

驗證：component tests、keyboard navigation、desktop/mobile scroll、viewport resize/orientation、API 單點失敗測試。

### Phase 3：建立內容契約與設計系統

1. 盤點 hard-coded 文案與 JSON，定義單一內容來源。
2. 決定 rich text：若保留 HTML，backend/CMS sanitize 並建立允許清單；否則改結構化 rich-text model。
3. version schema／OpenAPI contract；如要更名欄位，先加相容層再移除 legacy。
4. 建 design tokens：colors、type scale、spacing、container、breakpoints、radius、shadow、motion。
5. 消除 global selector 與 `!important` 依賴，再建立 reusable UI primitives。

驗證：schema fixture、contract tests、visual regression、WCAG contrast、reduced-motion 與 breakpoint matrix。

### Phase 4：實作新 IA 與視覺

1. 依 recruiter-first 優先級完成 Hero、Experience、featured projects、architecture/system-design case studies、resume CTA。
2. 若新增 routes，逐頁補 title/meta/canonical/OG、404 與 Nginx refresh smoke test。
3. Projects detail 顯示現有但被隱藏的 architecture、tradeoffs、future、category；再決定是否新增 diagram data model。
4. 圖片做尺寸／格式／lazy-loading 策略，避免直接把大圖當小 logo 傳送。

驗證：真實內容 review、Lighthouse、Core Web Vitals、responsive visual diff、所有 internal/external links。

### Phase 5：部署硬化與漸進上線

1. 使用 commit SHA image tags、記錄 revision、建立 staging／preview environment。
2. 將 frontend API base 改為更明確的環境配置策略；production CORS 限制正式 domain。
3. 補 security headers、cache policy、observability、error reporting 與 uptime check。
4. 先以 Cloud Run no-traffic revision 或 staging 驗證，再切流；保留可立即 rollback 的舊 revision。

驗證：container smoke tests、staging E2E、Cloud Run logs/metrics、DNS/custom-domain、rollback drill。

## 13. 改版驗證矩陣

| 面向 | 最低驗證項目 |
|---|---|
| Routes | `/`、新增 routes、直接 refresh、404、hash/section navigation |
| API | `/health`、三個 v1 success、404、malformed content、partial outage、CORS |
| Content | schema validation、所有專案／經歷欄位、HTML sanitization、updated date semantics |
| Viewports | 320/375/768/1024/1300+ px、portrait/landscape、zoom 200% |
| Input | mouse、trackpad、touch、keyboard-only、screen reader basic flow |
| Motion | normal、`prefers-reduced-motion: reduce` |
| Assets | resume、favicon、logos、broken image fallback、external links |
| Quality | lint、unit/component/contract/E2E、production build、visual regression |
| Performance/SEO | Lighthouse、bundle size、LCP/CLS/INP、meta/OG/canonical/structured data |
| Deployment | immutable image、staging smoke、health、logs、custom domain、rollback |

## 14. 仍需外部確認的推測與問題

以下無法只靠 repository 得出結論，規劃大改版前應向 owner 或雲端環境確認：

1. **【推測】** `adamtseng.com` 是正式 domain，但 custom-domain mapping 與 DNS 現況未知。
2. **【推測】** legacy `/api/*` endpoints 已無 consumer；刪除前仍應查 access logs。
3. **【推測】** repository JSON 是 production 的唯一內容來源；需確認是否有人在部署外手動改 Cloud Run image／設定。
4. **【推測】** 現有 project/experience 內容可公開；仍需 owner 再做保密與履歷一致性 review。
5. **【推測】** Cloud Run frontend/backend 是公開服務；workflow 沒有明示 unauthenticated policy。
6. **【推測】** 大改版希望強化 recruiter-first 的 backend/system-design 定位；需確認是否仍要保留 Instagram/Facebook 等個人社群。
7. GitHub Actions secrets、IAM scope、Cloud Run resource limits、autoscaling、logs、billing、alerts 與最近部署狀態，都必須到外部平台確認。

---

本文件描述的是盤點日期當下的 repository 現況。若程式碼與既有 README／TODO／架構文件互相矛盾，本文件以實際可執行程式碼與 deployment workflow 為準，並將矛盾列為技術債，而不是依文件推測程式已完成。
