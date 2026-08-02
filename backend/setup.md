# Backend Setup

## Requirements

- Python 3.13 (the container currently uses Python 3.13.9)
- `venv` and `pip`

Run all commands in this guide from the `backend/` directory.

## Local Development

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

On Windows PowerShell, activate it with:

```powershell
venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Start the API locally:

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8080
```

The local API is available at `http://127.0.0.1:8080`. FastAPI documentation is available at `/docs`, `/redoc`, and `/openapi.json`.

## Content Validation

Validate all Portfolio JSON files before starting or deploying the backend:

```bash
python scripts/validate_content_schema.py
```

The script discovers the current JSON files, selects the appropriate Pydantic resource schema, and fails when content is missing, unknown, or structurally invalid.

## API

- `GET /api/v1/about`
- `GET /api/v1/journey`
- `GET /api/v1/projects`
- `GET /api/v1/projects/{slug}`
- `GET /api/v1/timeline-events`
- `GET /api/v1/health`

The content APIs are public, read-only endpoints. Collection responses use the existing `data` and `meta` envelope.

## Data Update Workflow

1. Update the relevant JSON under `data/portfolio/`.
2. When adding a Journey, add a new JSON file under `data/portfolio/journey/`; the repository scans this directory automatically.
3. When adding a Project, add its JSON under `data/portfolio/projects/`, then register its slug/path in `repositories/project_repository.py` and its validation mapping in `scripts/validate_content_schema.py`.
4. Run `python scripts/validate_content_schema.py`.
5. Start the API and verify the affected endpoint response.
6. Deploy through the existing backend workflow after review.

Do not place secrets, credentials, private URLs, customer data, or confidential infrastructure details in Portfolio JSON.

## Container Check

From the `backend/` directory:

```bash
docker build -t fastapi-backend .
docker run --rm -p 8080:8080 fastapi-backend
```

The container runs Uvicorn on `0.0.0.0:8080`, matching the current Cloud Run port configuration.
