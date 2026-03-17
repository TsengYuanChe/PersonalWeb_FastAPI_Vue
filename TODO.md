# Portfolio System TODO

This document tracks architectural and engineering improvements for a lightweight portfolio system:

- Frontend: Vue 3 SPA + Vite + Nginx
- Backend: FastAPI read-only APIs
- Data layer: JSON files in `backend/data`
- Deployment: Docker + GitHub Actions + Artifact Registry + Cloud Run

Goal: improve maintainability, engineering credibility, architectural clarity, and production-readiness without overengineering.

---

## 1. High Priority Improvements

### 1.1 ✅ Introduce API versioning and response standards
- Short explanation: stabilize API contracts and make future changes non-breaking.
- Current state: ✅ Implemented. Versioned endpoints (`/api/v1/about`, `/api/v1/experience`, `/api/v1/projects`) now return a standardized envelope (`data` + `meta`), and frontend consumption has been updated to use `/api/v1/...`.
- Suggested structure or code example:
```python
# backend/routers/v1/content.py
@router.get("/api/v1/about")
def get_about():
    return {"data": about_payload, "meta": {"updated_at": updated_at}}
```
```json
{
  "data": { "paragraphs": ["..."] },
  "meta": { "updated_at": "2026-03-10T12:00:00Z", "version": "v1" }
}
```
- Benefits of the change:
  - Safer API evolution
  - Cleaner frontend parsing logic
  - Stronger interview-level architecture narrative

### 1.2 ✅ Add backend layering (router -> service -> repository)
- Short explanation: separate HTTP concerns from business logic and data access.
- Current state: ✅ Implemented. Routers delegate to `services/content_service.py`, which delegates data access to `repositories/content_repository.py` (router -> service -> repository -> filesystem JSON).
- Suggested structure or code example:
```text
backend/
  routers/
  services/
    content_service.py
  repositories/
    content_repository.py
```
```python
# routers call service, not filesystem
payload = content_service.get_about()
```
- Benefits of the change:
  - Better testability
  - Lower coupling
  - Cleaner module boundaries

### 1.3 ✅ Add `/health` endpoint
- Short explanation: provide standard service health probe.
- Current state: ✅ Implemented. Dedicated health endpoint is available at `GET /health` via `backend/routers/v1/health.py` and is registered in `backend/main.py`.
- Suggested structure or code example:
```python
@app.get("/health")
def health():
    return {"status": "ok"}
```
- Benefits of the change:
  - Better operations readiness
  - Easier monitoring integration
  - Clear service status contract

---

## 2. Backend Architecture Improvements

### 2.1 Introduce Pydantic response models
- Short explanation: enforce schema consistency and type safety.
- Current state: raw dict responses from file data.
- Suggested structure or code example:
```python
from pydantic import BaseModel

class Meta(BaseModel):
    updated_at: str
    version: str = "v1"

class AboutData(BaseModel):
    paragraphs: list[str]

class ApiResponse(BaseModel):
    data: AboutData
    meta: Meta
```
- Benefits of the change:
  - Automatic validation
  - Better OpenAPI docs
  - Reduced runtime schema drift

### 2.2 ✅ Reorganize backend modules for domain clarity
- Short explanation: group code by responsibility and version.
- Current state: ✅ Implemented. Routes are organized under `backend/routers/v1/` (`content.py`, `health.py`) and placeholders exist for `backend/core/` and `backend/schemas/` modules.
- Suggested structure or code example:
```text
backend/
  main.py
  core/
    config.py
    logging.py
  routers/
    v1/
      content.py
      health.py
  services/
    content_service.py
  repositories/
    content_repository.py
  schemas/
    content.py
    common.py
```
- Benefits of the change:
  - Faster onboarding
  - Easier expansion (new domains/endpoints)
  - Clear architectural intent

### 2.3 ✅ Add centralized exception handling
- Short explanation: standardize API errors and avoid endpoint-specific ad-hoc handling.
- Current state: ✅ Implemented. Centralized handlers are registered in `backend/main.py` for `HTTPException` (including route-not-found 404), `FileNotFoundError` (404), and generic `Exception` (500), all returning a standardized error envelope response.
- Suggested structure or code example:
```python
@app.exception_handler(FileNotFoundError)
async def file_not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": {"code": "CONTENT_NOT_FOUND", "message": str(exc)}}
    )
```
- Benefits of the change:
  - Consistent client behavior
  - Cleaner observability
  - Stronger production posture

### 2.4 Enforce dependency direction
- Short explanation: enforce strict layering rules to keep backend architecture predictable.
- Current state: layering is planned but dependency direction is not explicitly enforced.
- Suggested structure or code example:
```text
Allowed dependency direction:
routers -> services -> repositories

Disallowed:
repositories -> services
repositories -> routers
services -> routers
```
```python
# Example boundary check idea (CI lint rule)
# fail if repositories import from services or routers modules
```
- Benefits of the change:
  - Cleaner architecture boundaries
  - Reduced coupling
  - Easier refactoring

---

## 3. Data Layer Improvements

### 3.1 Restructure `backend/data` by domain folders
- Short explanation: avoid flat-file sprawl and enable growth.
- Current state: `about.json`, `exp.json`, `projects.json` in one folder.
- Suggested structure or code example:
```text
backend/data/
  profile/
    about.json
    experience.json
  portfolio/
    projects.json
  content/
    # reserved for future domains
```
- Benefits of the change:
  - Cleaner data ownership
  - Easier repository abstraction
  - Better long-term organization

### 3.2 Reserve domain namespaces for future content
- Short explanation: predefine locations for growth areas without implementing features now.
- Current state: no folder strategy for new domains.
- Suggested structure or code example:
```text
backend/data/
  blog/
  case_studies/
  talks/
```
- Benefits of the change:
  - Smooth future extension
  - Clear content taxonomy
  - Better architectural storytelling

### 3.3 Add lightweight JSON schema checks in CI
- Short explanation: validate content shape before deployment.
- Current state: content correctness validated only at runtime.
- Suggested structure or code example:
```bash
# CI step example
python -m scripts.validate_content_schema
```
- Benefits of the change:
  - Fewer deployment-time surprises
  - Better content quality control
  - Improved reliability with minimal complexity

---

## 4. Frontend Architecture Improvements

### 4.1 Introduce `src/api` access layer
- Short explanation: isolate HTTP concerns from UI/state logic.
- Current state: composables fetch APIs directly.
- Suggested structure or code example:
```text
frontend/src/
  api/
    client.js
    contentApi.js
  composables/
    usePageData.js
```
```js
// src/api/contentApi.js
export const getAbout = () => api.get("/api/v1/about")
```
- Benefits of the change:
  - Better separation of concerns
  - Easier API mocking/tests
  - Reusable API client behavior

### 4.2 Keep composables state-focused
- Short explanation: composables should orchestrate state and lifecycle, not endpoint details.
- Current state: network calls and state updates are mixed in one file.
- Suggested structure or code example:
```js
// usePageData.js
import * as contentApi from "@/api/contentApi"
// composable manages loading/error/state only
```
- Benefits of the change:
  - Cleaner composables
  - Lower refactor cost when API changes
  - More maintainable frontend codebase

### 4.3 Add shared response/error normalization in frontend API client
- Short explanation: centralize envelope parsing and error mapping.
- Current state: no common adapter for responses/errors.
- Suggested structure or code example:
```js
// src/api/client.js
export async function request(path) {
  const res = await fetch(`${import.meta.env.VITE_API_BASE}${path}`)
  const json = await res.json()
  if (!res.ok) throw new Error(json?.error?.message || "Request failed")
  return json.data
}
```
- Benefits of the change:
  - Consistent frontend behavior
  - Simpler UI error handling
  - Reduced duplicated logic

---

## 5. Environment Configuration

### 5.1 Introduce environment-specific config files
- Short explanation: formalize runtime configuration per environment.
- Current state: API base usage exists, but environment conventions are limited.
- Suggested structure or code example:
```text
frontend/.env
frontend/.env.development
frontend/.env.production
backend/.env
```
```dotenv
# frontend/.env.production
VITE_API_BASE=https://fastapi-backend-xxxx.run.app
```
- Benefits of the change:
  - Predictable deployments
  - Clear local/staging/prod separation
  - Lower configuration risk

### 5.2 Centralize backend settings loading
- Short explanation: avoid scattered constants and hardcoded values.
- Current state: config values mainly in code.
- Suggested structure or code example:
```python
# backend/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_env: str = "development"
    cors_origins: list[str] = ["*"]
```
- Benefits of the change:
  - Single source of configuration truth
  - Easier secure config management
  - Better environment portability

---

## 6. API Design Improvements

### 6.1 Normalize resource naming (plural nouns)
- Short explanation: improve REST consistency and readability.
- Current state: mixed singular/plural semantics.
- Suggested structure or code example:
```text
/api/v1/about
/api/v1/experiences
/api/v1/projects
```
- Benefits of the change:
  - More intuitive API surface
  - Easier client integration
  - Better API design credibility

### 6.2 Standardize response envelope (`data` + `meta`)
- Short explanation: keep every success response structurally consistent.
- Current state: direct payloads with appended fields.
- Suggested structure or code example:
```json
{
  "data": { "items": [] },
  "meta": { "updated_at": "2026-03-10T12:00:00Z", "request_id": "abc123" }
}
```
- Benefits of the change:
  - Predictable client handling
  - Easier metadata expansion
  - Cleaner contract governance

### 6.3 Standardize error response format
- Short explanation: unify all error payloads across endpoints.
- Current state: no explicit global error schema.
- Suggested structure or code example:
```json
{
  "error": {
    "code": "CONTENT_NOT_FOUND",
    "message": "projects.json not found",
    "details": null
  }
}
```
- Benefits of the change:
  - Better debugging
  - Better frontend UX behavior
  - Easier log/alert integration

### 6.4 Introduce OpenAPI contract usage in workflow
- Short explanation: treat schema as a first-class contract artifact.
- Current state: OpenAPI auto-generated but not used in checks.
- Suggested structure or code example:
```bash
# example CI step
curl -s http://localhost:8000/openapi.json > openapi.json
```
- Benefits of the change:
  - Contract visibility
  - Regression detection
  - Stronger API discipline

### 6.5 API security hardening
- Short explanation: even public APIs should apply baseline hardening controls.
- Current state: API is public with permissive defaults and limited protective constraints.
- Suggested structure or code example:
```python
# Restrict CORS origins
allow_origins=["https://your-frontend-domain.com"]

# Enforce request validation via Pydantic models
# (already aligned with response-model TODO items)

# Apply payload size limit at app/proxy level
# e.g., Nginx/FastAPI request body constraints

# Optional rate limiting
# e.g., 60 requests/min per IP for public endpoints
```
- Benefits of the change:
  - Stronger security posture
  - Safer public API exposure
  - More production-like architecture

### 6.6 Introduce API contract testing
- Short explanation: validate endpoint behavior continuously against the OpenAPI contract in CI.
- Current state: schema generation exists, but response-contract checks are limited.
- Suggested structure or code example:
```bash
# CI contract test example
schemathesis run http://localhost:8000/openapi.json
```
- Benefits of the change:
  - Prevents accidental API breaking changes
  - Stronger CI guarantees
  - Improved API reliability

---

## 7. Optional Platform Improvements

### 7.1 Add structured logging and request correlation
- Short explanation: improve diagnosability with low complexity overhead.
- Current state: basic logs only.
- Suggested structure or code example:
```python
logger.info("request_completed", extra={"path": path, "request_id": request_id})
```
- Benefits of the change:
  - Faster troubleshooting
  - Better operational transparency
  - Improved production confidence

### 7.2 Add lightweight caching strategy
- Short explanation: reduce repeated file reads and improve latency.
- Current state: reads JSON on each request.
- Suggested structure or code example:
```python
# in-memory TTL cache for content payloads
cache_key = f"{domain}:{name}"
```
- Benefits of the change:
  - Lower response latency
  - Reduced backend load
  - Better scaling behavior

### 7.3 Add basic metrics exposure
- Short explanation: capture essential service indicators without full observability stack.
- Current state: no explicit metrics endpoint.
- Suggested structure or code example:
```text
metrics: request_count, error_count, p95_latency
```
- Benefits of the change:
  - Quantifiable reliability signals
  - Better engineering maturity
  - Easier performance tracking

### 7.4 Optional CDN caching for frontend static assets
- Short explanation: speed up global asset delivery.
- Current state: Nginx serving static files without explicit CDN layer.
- Suggested structure or code example:
```text
Cloud CDN (optional) -> Cloud Run frontend service
```
- Benefits of the change:
  - Faster first-load performance
  - Reduced origin traffic
  - Better user experience in remote regions

### 7.5 Introduce request tracing and correlation IDs
- Short explanation: attach a unique `request_id` to each request to correlate logs across the request lifecycle.
- Current state: logs exist but request-level correlation is not consistently enforced.
- Suggested structure or code example:
```python
import uuid

request_id = uuid.uuid4().hex
logger.info("request_start", extra={"request_id": request_id})
logger.info("request_end", extra={"request_id": request_id, "status_code": 200})
```
- Benefits of the change:
  - Easier debugging
  - Cross-request tracing
  - Improved log analysis

---

## 8. Long-Term Evolution

### 8.1 Migrate to database-backed content store (if needed)
- Short explanation: move beyond file-based storage when content/query complexity grows.
- Current state: JSON file repository is sufficient for current scale.
- Suggested structure or code example:
```text
Repository interface:
- JsonContentRepository (current)
- SqlContentRepository (future)
```
- Benefits of the change:
  - Better query flexibility
  - Stronger concurrency semantics
  - Scalable content operations

### 8.2 Introduce admin content editing workflow
- Short explanation: enable controlled non-code content updates.
- Current state: content changes require git edits.
- Suggested structure or code example:
```text
Admin UI -> Backend admin API -> Content store
```
- Benefits of the change:
  - Faster editorial updates
  - Better governance/workflow controls
  - Reduced developer bottleneck

### 8.3 Add search architecture for portfolio content
- Short explanation: support indexed retrieval when content volume increases.
- Current state: no search index.
- Suggested structure or code example:
```text
Indexer job -> search index -> /api/v1/search
```
- Benefits of the change:
  - Better discoverability
  - Cleaner information retrieval layer
  - Stronger UX at scale

### 8.4 Add analytics architecture
- Short explanation: collect usage signals for data-driven iteration.
- Current state: no analytics pipeline.
- Suggested structure or code example:
```text
Frontend events -> analytics endpoint -> storage/dashboard
```
- Benefits of the change:
  - Evidence-based improvements
  - Better portfolio impact visibility
  - Clearer product-engineering feedback loop
