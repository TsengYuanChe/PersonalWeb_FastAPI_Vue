# Backend System Design

## Backend Overview

The backend is a small, read-only FastAPI content service for the portfolio. Portfolio JSON is the runtime content source, and Pydantic models define the contracts that all content must satisfy before it is returned to a consumer.

The backend is intentionally resource-oriented. About, Journey, Projects, and Timeline Events follow the same architectural boundaries while retaining resource-specific validation, ordering, and lookup behavior. Health is an infrastructure resource and does not read portfolio content.

This document describes backend architecture, responsibilities, maintenance principles, and design decisions. Refer to `overview.md` for whole-project architecture and runtime context, `structure.md` for the current repository tree and exact file ownership, and `backend/setup.md` for setup and runtime instructions.

## Design Principles

- **Read-only backend**: the service publishes portfolio content and does not provide content mutation, administration, authentication, or persistence workflows.
- **JSON as the source of truth**: public portfolio content is maintained as structured files rather than duplicated in application code or another storage layer.
- **Resource-oriented architecture**: each portfolio resource has a clear router, service, repository, and schema boundary.
- **Explicit schema validation**: Pydantic validation is mandatory; malformed or incomplete content must not become a successful response or deployable content set.
- **Thin routers**: routers own HTTP concerns and delegate application behavior to the matching service.
- **Service orchestration**: services coordinate repository reads, schema validation, resource rules, and response preparation.
- **Repository-owned filesystem access**: repositories alone own content paths, file discovery, JSON reads, and timestamps.
- **Schema-owned contracts**: schemas define accepted field names, nested structures, optionality, unions, and shared response metadata.
- **Predictable maintenance boundaries**: content changes should remain in portfolio JSON unless the contract or resource behavior changes.
- **No duplicated loading paths**: shared JSON and timestamp mechanics remain centralized, and no router or service creates a parallel JSON loader.

## Architecture

The primary responsibility flow is:

```text
Router
  ↓
Service
  ├─→ Repository → Portfolio JSON
  └─→ Schema validation
         ↓
Validated response
```

This preserves the architectural boundary commonly summarized as Router → Service → Repository, with Schema validation enforced by the Service before response preparation. Repository output is raw data; it is never treated as a validated contract by itself.

### Router

Files in `backend/routers/v1/` own transport-level concerns: resource routing, response model declaration, and delegation to the matching service. Routers stay thin and do not read files, implement ordering, or validate raw content directly.

### Service

Files in `backend/services/` own resource orchestration. A service requests raw content from its repository, validates it through the resource schema, preserves resource-specific behavior, and prepares the established response shape. Cross-resource convenience logic does not belong in a service when it weakens a resource boundary.

### Repository

Files in `backend/repositories/` own filesystem data access. They define resource paths, read raw JSON, handle file discovery or explicit mapping where required, and expose modification timestamps. Shared file-reading and timestamp behavior belongs in `repositories/common.py`; feature behavior does not.

Repositories do not own HTTP responses or Pydantic contracts.

### Schema

Files in `backend/schemas/` define Pydantic contracts by resource. They describe the accepted data shape and shared response metadata without performing file access or transport handling. Point and Duration Timeline Events remain a discriminated union, while nested About, Journey, and Project structures remain explicit models rather than unrestricted dictionaries.

`schemas/common.py` is reserved for models that are genuinely shared across resources.

## Directory Structure

Only architectural layers are shown here. See `structure.md` for the complete tracked tree and file-by-file responsibilities.

```text
backend/
├── routers/v1/          # HTTP routing by resource
├── services/            # Resource orchestration and response preparation
├── repositories/        # Filesystem JSON access and timestamps
├── schemas/             # Pydantic resource contracts
├── data/portfolio/      # Runtime portfolio content by page/resource
└── scripts/             # Fail-closed content validation tooling
```

Each layer is separated by responsibility rather than by implementation symmetry alone. Shared code is introduced only for behavior that is truly common; resource logic remains in its resource module.

## Backend Resources

Every resource follows the same Router → Service → Repository → Schema architecture while preserving its own domain-specific behavior.

- **About**: structured portfolio introduction and About sections from a single page-owned content source.
- **Journey**: independently maintained Journey entries aggregated into the established ordered collection.
- **Projects**: independently maintained Project summary and detail content, with deterministic collection order and slug lookup behavior.
- **Timeline Events**: Journey Timeline point and duration events maintained separately from Journey entries.
- **Health**: infrastructure status independent of portfolio JSON.

HTTP paths and current consumers are intentionally documented in `overview.md` and `structure.md`, not duplicated here.

## Data Management

Portfolio content is organized by page/resource under `backend/data/portfolio/`:

```text
portfolio/
├── about/
├── journey/
├── projects/
└── timeline/
```

About has one page-owned document. Journey and Projects use one JSON document per stable item or slug. Timeline Events remain a separate Journey-related data source because they are Timeline events, not Journey entries.

Content files contain public portfolio data only. Secrets, credentials, private infrastructure details, confidential customer information, and proprietary source code do not belong in this data source.

Adding a resource or changing a content contract is an architecture change: its router, service, repository, schema, validation coverage, and documentation must remain aligned. Routine content edits should not require a second data source or parallel loading path.

## Validation

All portfolio content is validated against its resource Pydantic schema. Validation is mandatory for About, Journey, Projects, and Timeline Events, including nested structures and discriminated event types.

Validation is fail-closed: missing expected content, unknown content outside the explicit validation mapping, or schema-invalid JSON blocks the deployment workflow. Runtime service validation remains necessary even though deployment validation exists; both enforce the same content contract at different boundaries.

Executable validation and smoke-test instructions belong in `backend/setup.md`.

## Deployment

The backend is deployed independently from the frontend so content API changes and frontend presentation changes retain separate runtime and release boundaries. Deployment implementation details are intentionally maintained outside this system design document; refer to `overview.md`, `structure.md`, and `backend/setup.md` for current operational context.

## Maintenance Guide

### Content Changes

Most maintenance should remain a content-only change under `backend/data/portfolio/`. Preserve the current resource schema, public-content rules, ordering semantics, and ownership boundary. Every content change must pass mandatory validation before release.

### Architecture Changes

Backend code changes are appropriate when introducing or changing a resource, contract, discovery rule, ordering rule, lookup behavior, error behavior, or response behavior. Keep the resource boundary consistent across router, service, repository, and schema modules.

Do not bypass a layer for convenience:

- routers do not read JSON;
- services do not create independent filesystem loaders;
- repositories do not construct HTTP responses;
- schemas do not perform I/O;
- raw JSON does not bypass Pydantic validation.

### Operational Guidance

Use `backend/setup.md` for environment setup, executable validation, local runtime, smoke testing, and other operational instructions.

### Documentation Sync

When backend architecture or responsibility changes:

- update `BACKEND.md` for system design, boundaries, and maintenance principles;
- update `overview.md` for whole-project architecture, runtime context, and risk;
- update `structure.md` for the actual repository tree and file ownership;
- update `backend/setup.md` only when executable setup, validation, or runtime instructions change.

Avoid copying detailed operational information into this document. If documentation disagrees with executable code, verify the current code and validation path, then update each document within its stated responsibility.
