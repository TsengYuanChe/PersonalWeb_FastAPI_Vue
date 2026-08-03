# Frontend System Design

## Frontend Overview

The frontend is a Vue single-page application organized around route-driven Views and component composition. The application shell selects the appropriate Home or Detail layout, Vue Router selects the active View, and each View coordinates the data and interaction state required by its page.

The frontend intentionally uses two content strategies. Home preview content is bundled as small local JSON so the first screen does not wait for the backend. Detail pages consume complete backend-owned content through the frontend Content API facade. These flows serve different presentation and loading requirements and are not competing sources for complete detail content.

State remains local to the application shell or owning View. There is no global state management layer because the current pages do not share mutable domain state, authentication state, or a coordinated client cache. Rendering is component-based, with shared components introduced only where current reuse establishes a stable responsibility.

This document defines the frontend system design, architectural responsibilities, ownership boundaries, and long-term maintenance principles. It is the design authority for frontend responsibility decisions and should change only when those responsibilities or boundaries change. Refer to `overview.md` for whole-project architecture and page behavior, `structure.md` for the current repository tree and exact file ownership, and `FRONTEND_REVIEW.md` for the historical architecture review rather than current design authority.

## Design Principles

- **Route-level ownership**: each route delegates page-specific loading, state, and orchestration to its View.
- **Component composition**: Views assemble focused layout and feature components instead of embedding every rendering concern directly.
- **View-owned orchestration**: a View coordinates page data, loading states, filters, expansion state, and interactions that span multiple child components.
- **Stateless presentation components**: components receive data and state through props and communicate intent through events; they do not duplicate page state or fetch data unless that responsibility explicitly belongs to them.
- **Local Home previews**: Home uses small bundled preview data to remain immediately renderable and independent of backend availability for its primary content.
- **Backend-owned detail content**: complete About, Journey, Timeline Event, and Project detail content remains owned by the backend and is not duplicated as full frontend data.
- **Rendering and domain logic separation**: templates and components own presentation, while deterministic calculations and normalization remain outside rendering markup.
- **Evidence-based sharing**: a UI primitive or abstraction becomes shared only when real consumers have the same semantics and should evolve together.
- **Composable and utility distinction**: composables own Vue reactivity, lifecycle, or DOM integration; utilities remain deterministic and independent of Vue.
- **Predictable maintenance boundaries**: content, orchestration, presentation, interaction, and domain calculations change in the layer that owns them rather than through parallel implementations.

## Architecture

The frontend is organized through explicit ownership relationships:

```text
App
├── Vue Router
│   └── Route View
│       ├── Feature Components
│       ├── Composables
│       ├── Utilities
│       └── Content API
├── Layout Components
└── Shell Composables
```

App owns the route-aware application shell without absorbing page responsibilities. Vue Router selects the owning View. The View coordinates its feature boundary and composes components, composables, utilities, and content access according to their respective contracts. Layout components and shell composables remain owned by App because their responsibilities span the application shell rather than a single feature.

### Application Shell

The application shell owns route-aware Home and Detail layout selection, the shared render outlet, shell-level data, and global effects. It composes shell children and supplies the refs or state required by shell composables without transferring shell ownership into presentation components.

The application shell does not own page-specific loading, filtering, Timeline coordination, or detail expansion state.

### Vue Router

Vue Router maps navigation to the owning View and supplies layout metadata consumed by the application shell. It does not own feature data or page interaction state.

### View

Views are page-level orchestrators. A View owns the state and lifecycle associated with one route, selects the appropriate content source, coordinates feature components, and handles loading, error, empty, and success states where backend data is involved.

A View should not absorb presentation details that can be expressed by a focused component, nor move route-local state into a global store without a cross-route requirement.

### Component

Components own rendering and interaction within a defined UI responsibility. Props provide data and state; emitted events report user intent to the owner. Components do not create parallel API clients, duplicate authoritative content, or retain independent copies of state that must be coordinated by a parent View.

### Composable and Utility

Composables and utilities support Views and components without replacing their ownership. Composables encapsulate reusable Vue-aware behavior. Utilities encapsulate pure calculations and mappings. Domain-independent behavior may be shared across features only when its contract is genuinely the same.

### Content API

The frontend Content API is a small, single facade over the backend content service. It normalizes backend responses into the shape expected by Views and centralizes transport error handling. Resource-specific page behavior remains in Views rather than creating a second frontend service hierarchy that only mirrors the backend.

## Component Architecture

### App

App is the route-aware application shell. It owns layout selection, shell composition, the shared render outlet, shell-level content, route coordination, and global effects. Shell DOM measurement, navigation, and scroll behavior may be delegated to focused composables while App remains their owner and supplies explicit inputs.

### Views

Views own route-local orchestration:

- Home composes preview sections from local content.
- About coordinates backend content states and section rendering.
- Journey coordinates Journey content, Timeline Events, Timeline presentation, active state, and single-detail expansion.
- Projects coordinates backend content, search and filters, empty results, and single-project expansion.

These responsibilities stay at View level because they coordinate multiple components or represent page-level state.

### Layout Components

Layout components render stable shell or detail-page structure. They receive presentation data through props and do not fetch content, inspect unrelated feature state, or own application lifecycle. Shared layout rendering remains separate from route-specific feature components.

### Feature Components

Feature components belong to About, Journey, or Projects and render domain-specific content. Summary and detail responsibilities may be separated when they change independently or have distinct state boundaries. Project detail rendering follows the canonical content sequence defined in `overview.md`, while its View retains page orchestration. Feature components remain unaware of neighboring feature architecture unless an explicit shared contract exists.

### Shared Components

Shared components represent behavior or presentation that has multiple real consumers with matching semantics. Sharing is based on responsibility, not visual similarity alone. A shared component retains a narrow contract and does not become a generic renderer for unrelated features.

## Data Flow

The frontend intentionally supports two presentation strategies. Home uses small bundled preview data so its primary content remains immediately available and independent of backend startup. That data is presentation-focused and is not a second source for complete detail content.

Detail pages use backend-owned structured content. Their Views own page-level orchestration while feature components render the prepared content. These strategies coexist because Home optimizes preview availability and detail pages preserve authoritative content ownership.

Detailed request paths, normalization boundaries, Timeline processing, and rendering flows are defined in `DATAFLOW.md` rather than duplicated in this system design document.

## State Management

The frontend does not use Pinia or Vuex. Current mutable state is local and has an identifiable owner:

- shell state belongs to App;
- request and page interaction state belongs to the route View;
- presentation components receive state through props;
- child intent returns through emitted events.

This keeps state close to the behavior that changes it and avoids a global dependency for unrelated routes. A global store becomes appropriate only when multiple routes require the same mutable state, coordinated caching and invalidation, authentication state, or a cross-page workflow. Shared constants or static configuration alone do not justify global state management.

## Utility and Composable Design

### Composable

A composable is Vue-aware. It may own reactive state, computed values, lifecycle registration, event listeners, DOM interaction, or reusable behavior that depends on Vue component lifetime. Its inputs should be explicit, especially for element refs and enablement state, so it does not rely on hidden selector or route coupling.

A composable should not exist merely to wrap a pure function or to give a single local helper a reusable-sounding name.

### Utility

A utility is a pure JavaScript module. Given the same inputs, it produces the same outputs. It does not import Vue, access the DOM, read global runtime state, perform API requests, or retain mutable module state. This makes domain calculations, search normalization, and stable mappings independently understandable and testable.

Presentation-specific reactive mapping remains with the component or View; only deterministic domain logic belongs in a utility.

## Styling Architecture

Frontend styling follows the same ownership boundaries as rendering. Global styles own application-wide foundations, shell behavior, and primitives with genuine cross-feature semantics. Feature styles own the presentation and responsive behavior of their feature. A rule becomes shared only when multiple consumers have the same responsibility and should evolve together; visual similarity alone does not establish shared ownership.

Styles remain globally loaded, so responsibility boundaries and predictable cascade behavior must be preserved when rules change. Exact stylesheet and selector-level ownership belongs in `structure.md`; whole-project styling context and risks belong in `overview.md`.

## Maintenance Guide

### Content Changes

Most Home content maintenance should remain in the local preview JSON and the presentation components that consume it. Complete detail content remains a backend responsibility and should be changed through the backend portfolio content source rather than duplicated in frontend files.

Routine visual or copy changes should preserve the existing ownership boundary: Views orchestrate, components render, composables manage Vue-aware behavior, utilities provide pure logic, and the Content API remains the backend-facing facade.

### Architecture Changes

Frontend architecture should change when introducing a new page, a new feature with its own ownership boundary, a genuinely shared component, reusable Vue-aware behavior, or deterministic domain logic that should be independent of rendering.

Keep changes aligned across the affected layers:

- a new page receives a route-level View owner;
- cross-component page state remains with the View;
- reusable presentation receives a focused component contract;
- lifecycle, reactivity, or DOM behavior belongs in a composable;
- pure calculations belong in a utility;
- backend content access continues through the Content API facade.

Do not create abstractions solely to mirror backend folders, reduce file length, or anticipate consumers that do not exist.

### Documentation Sync

When frontend architecture or responsibility changes:

- update `FRONTEND.md` for system design, ownership boundaries, and maintenance principles;
- update `overview.md` for whole-project architecture, page behavior, data flow, and risk;
- update `structure.md` for the actual repository tree and file-level ownership.

`FRONTEND_REVIEW.md` remains a historical review and planning artifact rather than the source of current architecture. Avoid copying detailed file inventories or operational instructions into this document. If documentation disagrees with executable code, verify the current code and update each document within its stated responsibility.

## Out of Scope

`FRONTEND.md` intentionally does not document:

- file-by-file or selector-level ownership, which belongs in `structure.md`;
- runtime data movement and transformation paths, which belong in `DATAFLOW.md`;
- deployment and operational context, which belong in `overview.md` and the relevant operational documentation;
- build configuration and implementation artifacts, which are recorded by `structure.md` and their owning configuration files;
- API contracts and backend resource design, which belong in `overview.md`, `structure.md`, and `BACKEND.md` according to scope;
- implementation history, review findings, and refactor planning, which remain in `FRONTEND_REVIEW.md`.

This document should remain stable through ordinary content and implementation updates. It changes when frontend system design, architectural responsibilities, or ownership boundaries change.
