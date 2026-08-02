# Frontend System Design

## Frontend Overview

The frontend is a Vue single-page application organized around route-driven Views and component composition. The application shell selects the appropriate Home or Detail layout, Vue Router selects the active View, and each View coordinates the data and interaction state required by its page.

The frontend intentionally uses two content strategies. Home preview content is bundled as small local JSON so the first screen does not wait for the backend. Detail pages consume complete backend-owned content through the frontend Content API facade. These flows serve different presentation and loading requirements and are not competing sources for complete detail content.

State remains local to the application shell or owning View. There is no global state management layer because the current pages do not share mutable domain state, authentication state, or a coordinated client cache. Rendering is component-based, with shared components introduced only where current reuse establishes a stable responsibility.

This document describes frontend architecture, ownership boundaries, design principles, and maintenance philosophy. Refer to `overview.md` for whole-project architecture and page behavior, `structure.md` for the current repository tree and exact file ownership, and `FRONTEND_REVIEW.md` for the historical architecture review rather than current design authority.

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

The primary responsibility flow is:

```text
User
  ↓
Vue Router
  ↓
View
  ├─→ Components
  ├─→ Composable / Utility
  └─→ Content API → Backend API
                       ↓
                 Normalized response
                       ↓
                     View
```

The flow is coordinated by the View rather than treated as a strict rendering pipeline. Components render and emit intent, composables support reactive or lifecycle behavior, utilities provide pure calculations, and the Content API hides transport-envelope details from feature code.

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

Feature components belong to About, Journey, or Projects and render domain-specific content. Summary and detail responsibilities may be separated when they change independently or have distinct state boundaries. Feature components remain unaware of neighboring feature architecture unless an explicit shared contract exists.

### Shared Components

Shared components represent behavior or presentation that has multiple real consumers with matching semantics. Sharing is based on responsibility, not visual similarity alone. A shared component retains a narrow contract and does not become a generic renderer for unrelated features.

## Data Flow

### Home Preview Content

```text
Home View
  ↓
Local Preview JSON
  ↓
Preview Components
  ↓
Home Rendering
```

Home preview content is intentionally small and bundled with the frontend. It supports immediate rendering without waiting for backend startup and contains only the summary information required by Home. Preview wording, selection, and ordering are frontend presentation responsibilities.

Local preview data is not a second store for complete About, Journey, or Project details. Fields that represent the same public summary may require deliberate synchronization, while preview-specific wording may remain intentionally shorter.

### Detail Content

```text
Detail View
  ↓
Content API
  ↓
Backend
  ↓
Normalized response
  ↓
View orchestration
  ↓
Feature Components
```

Detail pages request complete resource content from the backend. The Content API normalizes the backend response, the View owns request and page state, and feature components render the resulting content. Complete detail JSON is not maintained in the frontend.

The two flows intentionally coexist: Home prioritizes bundled preview availability, while detail pages prioritize backend-owned structured content and maintainable resource contracts.

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

Frontend styles remain globally loaded and are organized through documented ownership rather than scoped modules. Global styles own design tokens, document and application shell rules, shared page primitives, and genuinely shared UI primitives. Feature styles own About, Journey, and Projects presentation respectively. Each responsive stylesheet owns only the responsive behavior of its matching global or feature responsibility.

Shared styling is based on actual cross-feature consumers with the same semantics. Similar-looking feature surfaces, controls, or interactions remain separate when they represent different responsibilities. Feature-specific variables remain with the owning feature; global variables are reserved for values shared by the application shell or multiple features.

Because styles participate in one global cascade, import order and selector convention remain part of current behavior. Exact file ownership, responsive organization, and current risks are documented in `structure.md` and `overview.md`; this document does not duplicate a selector inventory.

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
