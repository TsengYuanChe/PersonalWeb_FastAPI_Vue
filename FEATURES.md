# Features Document

## 1. Feature Overview
The project delivers a production-ready personal portfolio with dynamic content, responsive UI, and cloud deployment automation.

Core outcomes for reviewers:
- Recruiter-facing presentation of profile, experience, and projects.
- Runtime content delivery from APIs (not static hardcoding).
- Clean desktop/mobile behavior with intentional interaction patterns.
- Deployment model consistent with modern engineering workflows.

## 2. Frontend Features
### Content Experience
- Single-page layout with anchored sections: About, Experiences, Projects, Tech Stack.
- Sidebar-based in-page navigation for fast section access.
- Project cards with technology tags and optional repository links.
- Social profile links (GitHub, LinkedIn, Instagram, Facebook).

### Rendering and Data
- Vue 3 Composition API app with reactive state.
- Runtime fetch of backend content from:
  - `GET /api/about`
  - `GET /api/experience`
  - `GET /api/projects`
- Computed display of unified “Last updated” date from backend metadata.

### Responsiveness and Interaction
- Desktop layout: sticky sidebar + independently scrollable content panel.
- Mobile layout: fixed header/footer model with dynamic viewport sizing.
- Smooth in-container scrolling to anchor sections.
- Visual effects: cursor glow (desktop), hover states for cards/tags/icons.

## 3. Backend Features
### API Surface
- `GET /api/about`
- `GET /api/experience`
- `GET /api/projects`
- `GET /` (service status message)

### Content Serving Model
- File-based JSON content loading from `backend/data/`.
- Shared endpoint utility appends `updated_at` per response using file mtime.
- Read-only API behavior suitable for public portfolio publishing.

### Cross-Origin Access
- FastAPI CORS middleware enabled.
- Current policy allows all origins to simplify frontend/backend integration.

## 4. System Integration

The frontend and backend communicate through a small set of REST APIs.

Workflow:

1. Vue application mounts and initializes state.
2. `usePageData()` requests portfolio content from backend endpoints.
3. FastAPI reads the corresponding JSON file and attaches `updated_at`.
4. The response is returned as structured JSON.
5. Vue updates reactive state and renders the UI.

This separation allows frontend UI evolution without modifying backend logic.

## 5. Content Management
Portfolio data is managed as versioned JSON files:
- `backend/data/about.json`
- `backend/data/exp.json`
- `backend/data/projects.json`

Update lifecycle:
1. Edit JSON content.
2. Backend serves revised payload and refreshed `updated_at`.
3. Frontend fetches and renders latest values on load.

Why this works well here:
- Low operational overhead.
- Simple diff/review workflow in git.
- No schema migration burden for content updates.

## 6. DevOps / Platform Features
### Containerization
- Backend container runs FastAPI/Uvicorn on port `8080`.
- Frontend container uses multi-stage build (Node build -> Nginx runtime).

### CI/CD Automation
- Separate workflows for backend and frontend deployment.
- Path-based triggers avoid unnecessary rebuild/deploy cycles.
- Build -> push to Artifact Registry -> deploy to Cloud Run.

### Cloud Deployment
- Frontend and backend run as independent Cloud Run services.
- Services can be updated and scaled independently.

## 7. UI/UX Behavior
Implemented interaction mechanics:
- Smooth section scrolling from sidebar controls.
- Wheel-event proxying to preserve intended content-pane scrolling behavior.
- Sticky desktop navigation pattern for persistent context.
- Mobile footer injection/repositioning with live timestamp display.
- Resize-aware layout variable updates to reduce mobile clipping/scroll issues.

## 8. Engineering Highlights

Key engineering characteristics of this project:

- Clear separation between presentation layer and content API layer.
- Containerized services with independent deployment pipelines.
- File-based content management enabling version-controlled updates.
- Lightweight architecture optimized for low operational overhead.
- Modern SPA architecture with runtime data loading.

These design choices prioritize simplicity, maintainability, and developer productivity.

## 9. Future Features
Natural extensions of the current design:
- Technical blog and long-form case-study publishing.
- Database- or CMS-backed content management.
- Project/experience search and filtering.
- Authenticated admin panel for content editing.
- Contact workflow with anti-spam and notification routing.
- API versioning plus schema validation for stronger contract governance.
