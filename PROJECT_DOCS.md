# PROJECT_DOCS

## 1. Project Overview
This repository contains a personal portfolio website with a separated frontend and backend:

- Frontend: Vue 3 single-page app that renders profile, experience, and project content.
- Backend: FastAPI service that exposes JSON APIs for page content.
- Deployment: Both services are containerized with Docker and deployed independently to Google Cloud Run via GitHub Actions.

The site is designed as a recruiter-facing engineering portfolio with a strong focus on backend/full-stack experience.

## 2. Site Architecture
High-level architecture:

1. User opens the Vue frontend (Cloud Run + Nginx).
2. Frontend loads portfolio data from FastAPI endpoints.
3. FastAPI reads JSON files from `backend/data/`, adds file-modified timestamps, and returns API responses.
4. Frontend renders sections and computes a single "Last updated" date from backend timestamps.

Service boundaries:

- `frontend`: Presentation layer, routing, section navigation, UI behaviors, responsive layout.
- `backend`: Content API layer (read-only JSON source, no database currently).
- `.github/workflows`: CI/CD automation for image build, push to Artifact Registry, deploy to Cloud Run.

## 3. Page Structure
Current route structure:

- `/` -> main portfolio page (implemented in `frontend/src/App.vue`)

Main page sections (single-page scrolling layout):

1. Sidebar
2. Profile/About (`#about`)
3. Experiences (`#exp`)
4. Projects (`#projects`)
5. Tech stack summary (`#stack`)

Navigation behavior:

- Sidebar menu triggers smooth scroll to section anchors within `.main-content`.
- Desktop: sticky left sidebar + scrollable right content.
- Mobile: sidebar transforms into fixed top header, footer content is moved to a fixed mobile footer by JS.

Notes:

- `frontend/src/views/Home.vue` exists with an older axios example endpoint (`/api/index`) but is not used by the current rendered UI.

## 4. Features Implemented
Implemented frontend features:

- Dynamic content loading from backend APIs (`about`, `experience`, `projects`).
- Last-updated indicator derived from backend file timestamps.
- Smooth in-page section navigation.
- Mouse glow visual effect (desktop only).
- Scroll proxy behavior routing wheel scroll to main content panel.
- Responsive layout system with dedicated RWD styles per section.
- Social/contact links (GitHub, LinkedIn, Instagram, Facebook).
- Project cards with language/tool tags and optional external code links.

Implemented backend features:

- FastAPI app with CORS enabled.
- Three content APIs:
  - `GET /api/about`
  - `GET /api/experience`
  - `GET /api/projects`
- File-based content management via JSON in `backend/data/`.
- `updated_at` added dynamically from file modified time.

Implemented platform/devops features:

- Dockerfile for backend (Uvicorn).
- Dockerfile for frontend (Vite build + Nginx runtime).
- GitHub Actions workflows for separate frontend/backend deployments to Cloud Run.

## 5. Tech Stack
Frontend:

- Vue 3 (`script setup`, Composition API)
- Vue Router 4
- Vite
- Bootstrap 5 + Bootstrap Icons
- Custom CSS (section-specific + responsive files)
- Fetch API (runtime data fetching), axios dependency also present

Backend:

- Python 3.11+ / FastAPI
- Uvicorn
- JSON file storage (no database yet)

DevOps / Infrastructure:

- Docker
- Nginx (frontend container runtime)
- Google Cloud Run
- Google Artifact Registry
- GitHub Actions (`backend-deploy.yml`, `frontend-deploy.yml`)

## 6. Data Flow
Runtime data flow:

1. Vue app starts (`frontend/src/main.js`) and mounts `App.vue`.
2. `usePageData()` reads `VITE_API_BASE` and requests:
   - `/api/about`
   - `/api/experience`
   - `/api/projects`
3. FastAPI router (`backend/routers/main_api.py`) loads corresponding JSON file from `backend/data/`.
4. Backend appends `updated_at` from file modification timestamp and returns JSON.
5. Frontend stores data in reactive refs and renders sections.
6. `updatedTime` is computed as the most recent timestamp across the three responses and shown in sidebar/mobile footer.

Content management flow:

1. Update `backend/data/*.json`.
2. API response reflects new content and timestamp.
3. Frontend shows updated content without code changes.

Deployment flow:

1. Push to `main`.
2. Path-filtered workflow triggers for changed service.
3. GitHub Action builds Docker image, pushes to Artifact Registry.
4. Action deploys to Cloud Run service.

## 7. Folder Structure Explanation
Top-level:

- `backend/`: FastAPI service, API routes, JSON content, Python dependencies, backend Docker config.
- `frontend/`: Vue app source, styling, assets, frontend Docker + Nginx config, Node dependencies.
- `.github/workflows/`: CI/CD pipelines for independent service deployment.
- `AGENT.md`: repository guidance for AI-assisted maintenance.
- `README.md`: minimal root readme.

Backend structure:

- `backend/main.py`: FastAPI app entrypoint, CORS middleware, router registration.
- `backend/routers/main_api.py`: API endpoints and JSON loading utility.
- `backend/data/`: content source files:
  - `about.json`
  - `exp.json`
  - `projects.json`
- `backend/requirements.txt`: Python dependencies.
- `backend/Dockerfile`: backend container build/runtime.
- `backend/setup.md`: local/deployment operational notes.

Frontend structure:

- `frontend/src/main.js`: app bootstrap, plugin/style imports.
- `frontend/src/App.vue`: primary UI layout and section rendering.
- `frontend/src/router/index.js`: route definition (`/`).
- `frontend/src/composables/`: reusable UI/data behaviors:
  - `usePageData.js` (API fetch + state)
  - `useSmoothScroll.js`
  - `useScrollProxy.js`
  - `useMobileFooter.js`
  - `useMouseGlow.js`
- `frontend/src/assets/css/`: base + section-specific + responsive styles.
- `frontend/src/assets/images/exp/`: experience logos.
- `frontend/src/views/Home.vue`: currently non-primary view file (legacy/test-like API example).
- `frontend/vite.config.js`, `eslint.config.js`, `jsconfig.json`: tooling configuration.
- `frontend/Dockerfile`, `frontend/nginx.conf`: production container and serving configuration.

Non-source/dependency directories:

- `frontend/node_modules/`: npm dependencies (generated).
- `backend/venv/`: Python virtual environment (generated).
