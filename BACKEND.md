# Backend Architecture and Maintenance Guide

## Backend Overview

The backend is a small, read-only FastAPI service for portfolio content. JSON files are the content source of truth; Pydantic models validate them before FastAPI serializes a response. The application does not use a database, authentication, write endpoint, or administration UI.

The architecture is intentionally resource-oriented. About, Journey, Projects, and Timeline Events each have their own router, service, repository, and schema module. This keeps routine content updates separate from application code changes.

## Architecture

The request and content flow is:

```text
HTTP request
    ↓
Resource Router
    ↓
Resource Service
    ↓
Resource Repository
    ↓
Portfolio JSON
    ↓ raw data
Resource Schema Validation
    ↓
data + meta response
```

### Router

Files in `backend/routers/v1/` own HTTP paths, response models, and delegation to the matching service. Routers do not read files or implement content validation.

### Service

Files in `backend/services/` coordinate repository reads, invoke Pydantic validation, preserve resource ordering, prepare the v1 response envelope, and handle resource-specific behavior such as Project slug 404 responses.

### Repository

Files in `backend/repositories/` own filesystem paths and raw JSON access. They return raw data and file modification timestamps. `repositories/common.py` contains only the shared JSON reader, data root, and timestamp formatting.

### Schema

Files in `backend/schemas/` define the data contract. Resource schemas validate About, Journey, Project, and Timeline Event structures. `schemas/common.py` contains the shared `Meta` and `ApiResponse` models.

## Directory Structure

```text
backend/
├── main.py                         # FastAPI app, middleware, routers, errors
├── requirements.txt                # Pinned runtime dependency set
├── setup.md                        # Local setup and content workflow
├── Dockerfile                      # Cloud Run container runtime
├── .dockerignore                   # Backend build-context exclusions
├── routers/v1/                     # HTTP endpoints by resource
├── services/                       # Validation orchestration and responses
├── repositories/                   # Filesystem JSON data access
├── schemas/                        # Pydantic contracts by resource
├── data/portfolio/                 # Runtime portfolio content
└── scripts/
    └── validate_content_schema.py  # Fail-closed JSON validation
```

## API Reference

| Endpoint | Purpose | Data source |
|---|---|---|
| `GET /api/v1/about` | Complete About sections | `backend/data/portfolio/about/about.json` |
| `GET /api/v1/journey` | Complete Journey entries | `backend/data/portfolio/journey/*.json` |
| `GET /api/v1/projects` | Ordered complete Project list | `backend/data/portfolio/projects/*.json` through the Project mapping |
| `GET /api/v1/projects/{slug}` | One complete Project or 404 | Project slug mapping in `project_repository.py` |
| `GET /api/v1/timeline-events` | Point and duration Timeline Events | `backend/data/portfolio/timeline/events.json` |
| `GET /api/v1/health` | Runtime health response | No content file |

The backend also exposes `GET /` as a basic running message and FastAPI's default `/docs`, `/redoc`, and `/openapi.json` endpoints.

## Data Management

```text
backend/data/portfolio/
├── about/
│   └── about.json
├── journey/
│   └── {journey-slug}.json
├── projects/
│   └── {project-slug}.json
└── timeline/
    └── events.json
```

### Updating About

Edit `about/about.json` and preserve the current section-based schema. The About repository uses this fixed path.

### Adding or Updating Journey

Edit an existing file or add one JSON file per Journey under `journey/`. The Journey repository scans `*.json` automatically, and the response is ordered by `start_date` descending.

### Adding or Updating a Project

Project content uses one JSON file per slug, but Project discovery is intentionally ordered rather than automatic. For a new Project:

1. Add `projects/{slug}.json`.
2. Add its slug/path to `PROJECT_FILES` in `backend/repositories/project_repository.py` at the intended display position.
3. Add the file to the validation mapping in `backend/scripts/validate_content_schema.py`.
4. Run validation and test both the collection and slug endpoints.

### Updating Timeline Events

Edit `timeline/events.json`. Point and duration events use a discriminated Pydantic union and must retain their existing JSON shapes.

Never add secrets, tokens, credentials, internal hostnames, private infrastructure details, confidential customer data, or proprietary source code to public portfolio content.

## JSON Validation

Run from `backend/`:

```bash
python scripts/validate_content_schema.py
```

The validator:

- validates About, Journey, Project, and Timeline JSON with their resource schemas;
- rejects missing expected files;
- rejects JSON files without an explicit schema mapping;
- verifies nested structures and Timeline Event discriminator rules;
- exits non-zero so deployment can stop before building an invalid content image.

Validation does not replace an API smoke test. After content changes, start FastAPI and inspect the affected response.

## Local Development

From `backend/`:

```bash
python -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python scripts/validate_content_schema.py
uvicorn main:app --reload --host 127.0.0.1 --port 8080
```

Use `http://127.0.0.1:8080/docs` for interactive API documentation. Windows activation and container commands are documented in `backend/setup.md`.

## Deployment

`backend/Dockerfile` builds the backend with Python 3.13.9, installs `requirements.txt`, copies the filtered backend context, and starts Uvicorn on `0.0.0.0:8080`. `backend/.dockerignore` prevents local environments, bytecode, caches, logs, and OS metadata from entering the image.

The backend is deployed as a separate Cloud Run service. The current container and Cloud Run configuration expect port 8080. Deployment automation also runs the JSON validation script before building the image. Detailed CI/CD credentials and production configuration are intentionally outside this guide.

## Maintenance Guide

### Content Update

Most future maintenance should only change `backend/data/portfolio/`:

- revise About paragraphs or items;
- update Journey details;
- update Project descriptions and metadata;
- add public Timeline Events.

Always validate JSON and smoke-test the affected endpoint before deployment.

### Code Change

Backend code normally needs to change only when:

- adding or changing an API endpoint;
- changing an API response contract;
- introducing a new JSON schema or data type;
- changing discovery, ordering, validation, or error behavior;
- adding a new Portfolio resource.

Keep the resource boundary consistent across router, service, repository, and schema layers. Do not create a second JSON loader or bypass Pydantic validation.

### Documentation Sync

When architecture or responsibility changes, update:

- `BACKEND.md` for backend maintenance behavior;
- `backend/setup.md` for executable local commands;
- `overview.md` for whole-project architecture and risk;
- `structure.md` for the actual repository tree and file responsibilities.

If documents disagree with executable code, verify the code and validation path first, then correct the documents.
