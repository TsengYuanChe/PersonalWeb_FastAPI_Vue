# Features 文件

## 1. 功能總覽
此專案提供可用於正式環境的個人作品集網站，具備動態內容、responsive UI 與雲端部署自動化能力。

給審閱者的核心成果：
- 以 recruiter 為對象，清楚呈現個人簡介、經歷與專案。
- 透過 API 在執行期提供內容（非靜態硬編碼）。
- 桌面與行動裝置皆有清晰且具設計意圖的互動行為。
- 部署模型符合現代工程實務流程。

## 2. Frontend 功能
### 內容體驗
- 採用單頁式版面，並以錨點區塊組織內容：About、Experiences、Projects、Tech Stack。
- 透過 sidebar 進行頁內導覽，快速切換到目標區塊。
- 專案卡片包含 technology tags 與可選的 repository 連結。
- 提供社群個人連結（GitHub、LinkedIn、Instagram、Facebook）。

### 渲染與資料
- 使用 Vue 3 Composition API 與 reactive state。
- 在執行期自 backend 取得內容：
  - `GET /api/about`
  - `GET /api/experience`
  - `GET /api/projects`
- 根據 backend metadata 計算並顯示統一的「Last updated」日期。

### 響應式與互動
- 桌面版版面：sticky sidebar + 可獨立捲動的內容面板。
- 行動版版面：固定 header/footer 佈局，並搭配動態 viewport 尺寸調整。
- 在容器內進行平滑捲動以導向錨點區塊。
- 視覺效果：cursor glow（desktop）、卡片/tag/icon 的 hover 狀態。

## 3. Backend 功能
### API Surface
- `GET /api/about`
- `GET /api/experience`
- `GET /api/projects`
- `GET /`（service status message）

### 內容提供模型
- 從 `backend/data/` 以檔案方式載入 JSON 內容。
- 共用 endpoint utility 會以檔案 mtime 在每個回應附加 `updated_at`。
- 採用唯讀 API 行為，適合公開作品集發佈情境。

### Cross-Origin 存取
- 已啟用 FastAPI CORS middleware。
- 目前 policy 允許所有來源，以簡化 frontend/backend 整合。

## 4. 系統整合

frontend 與 backend 透過一小組 REST APIs 進行通訊。

流程：

1. Vue application 掛載並初始化 state。
2. `usePageData()` 從 backend endpoints 請求作品集內容。
3. FastAPI 讀取對應 JSON 檔案並附加 `updated_at`。
4. 回應以結構化 JSON 形式返回。
5. Vue 更新 reactive state 並渲染 UI。

此分層設計可在不修改 backend 邏輯的前提下演進 frontend UI。

## 5. 內容管理
作品集資料以可版本控管的 JSON 檔案管理：
- `backend/data/about.json`
- `backend/data/exp.json`
- `backend/data/projects.json`

更新生命週期：
1. 編輯 JSON 內容。
2. Backend 提供更新後 payload 與新的 `updated_at`。
3. Frontend 在載入時抓取並渲染最新內容。

此作法的適配性：
- 維運成本低。
- 在 git 中可進行簡單的 diff/review 流程。
- 內容更新不需要 schema migration 負擔。

## 6. DevOps / 平台功能
### Containerization
- Backend container 在 `8080` port 執行 FastAPI/Uvicorn。
- Frontend container 使用 multi-stage build（Node build -> Nginx runtime）。

### CI/CD 自動化
- Backend 與 frontend 使用獨立 workflows 部署。
- Path-based triggers 可避免不必要的 rebuild/deploy。
- Build -> push 到 Artifact Registry -> deploy 到 Cloud Run。

### 雲端部署
- Frontend 與 backend 以獨立 Cloud Run services 執行。
- 服務可獨立更新與擴縮。

## 7. UI/UX 行為
已實作的互動機制：
- 由 sidebar 控制的區塊平滑捲動。
- 透過 wheel-event proxy 維持預期的內容面板捲動行為。
- Sticky desktop 導覽模式，提供持續可見的上下文。
- 行動版 footer 的動態插入/重定位，並顯示即時時間戳。
- 針對 resize 的版面變數更新，降低行動裝置裁切與捲動問題。

## 8. 工程亮點

本專案的關鍵工程特性：

- 展示層與內容 API 層之間具備清楚分離。
- 服務皆為 containerized，且具獨立部署 pipeline。
- 採檔案式內容管理，可進行版本控管更新。
- 輕量化架構，針對低維運成本情境優化。
- 現代 SPA 架構，支援執行期資料載入。

這些設計選擇優先考量簡潔性、可維護性與開發者生產力。

## 9. 未來功能
目前設計可自然延伸的方向：
- 技術部落格與長篇案例研究發佈。
- 以資料庫或 CMS 為後端的內容管理。
- 專案/經歷搜尋與篩選。
- 具驗證機制的內容管理後台。
- 含防垃圾機制與通知路由的聯絡流程。
- API versioning 與 schema validation，以強化契約治理。
