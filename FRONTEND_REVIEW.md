# Frontend Architecture Review

> 盤點日期：2026-08-02  
> 依據：`frontend/` 的 tracked files、實際 imports、routes、component consumers、runtime state、API calls、local JSON、CSS selectors/import order、package lock、Vite、Docker 與 Nginx 設定。  
> Review scope：Vue 3 SPA architecture、ownership、coupling、build/deployment boundaries 與分階段 refactor candidates。  
> 本次只新增此 review 文件，沒有修改任何 frontend runtime code、content、style、dependency 或 deployment file。
> 後續現況同步：Journey domain rename 已更新本文件中的 runtime paths、symbols 與 route names；原始 review 的判斷與階段性建議語氣仍保留。

## Current Architecture

### Runtime flow

```text
index.html
  → src/main.js
  → createApp(App) + Vue Router
  → App.vue route-aware application shell
  → RouterView
  → HomeView / AboutView / JourneyView / ProjectView
  → local Home JSON or contentApi.js
  → feature components
```

`main.js` owns application bootstrap and global CSS order. `App.vue` stays mounted across route changes and selects Home/detail layout from route meta. Views own page data and page-local interaction state. Components receive domain objects through props; there is no global store.

### Runtime ownership by directory

| Location | Current responsibility | Coupling/change boundary |
|---|---|---|
| `src/api/` | Fetch transport and the four v1 content calls | Shared by App and detail Views; no component performs fetch directly |
| `src/views/` | Route-level loading, state, empty/error handling and feature orchestration | Correct page boundary; Journey has materially more orchestration than other Views |
| `src/components/about/` | Rendering one backend About section | About-specific and stateless |
| `src/components/journey/` | Home Journey row, detail Journey header/detail, Timeline rendering | Home and detail components are separated; Timeline owns both rendering and date/event calculations |
| `src/components/projects/` | Shared cover/action, Home preview and detail Project card | `ProjectCover` and `ProjectAction` are genuinely cross-page; other components are page-specific |
| `src/components/layout/` | Shared detail page heading/breadcrumb | Cross-detail-page shared component |
| `src/composables/` | Global DOM side effects plus one misclassified pure helper collection | Only `useMouseGlow` and `useScrollProxy` are lifecycle composables |
| `src/utils/` | Journey logo lookup and pure Project search/filter helpers | Pure, deterministic logic with high unit-test value |
| `src/data/home/` | Bundle-time Home preview content | Intentionally independent from backend runtime availability |
| `src/assets/css/` | Global tokens, layouts, feature styles and responsive overrides | All eight files are global; ownership is conventional rather than enforced |
| `src/assets/images/` | Imported Journey logos | Vite fingerprints these assets |
| `public/` | Resume and favicon files served with stable public paths | No bundler import or hashing |
| `src/router/` | Four routes, layout meta and document scroll reset | Home inner scrolling is additionally handled by App |
| Build/deploy files | Vite, ESLint, aliases, tracked env config, Docker/Nginx | API base is build-time; Nginx provides SPA fallback |

### Route and data matrix

| Route | View | Data source | Page state owner |
|---|---|---|---|
| `/` | `HomeView.vue` | Static imports from `src/data/home/*.json` | No runtime page state |
| `/about` | `AboutView.vue` | `GET /api/v1/about` | `AboutView` |
| `/journey` | `JourneyView.vue` | Journey + Timeline Events APIs | `JourneyView` |
| `/project` | `ProjectView.vue` | Projects API | `ProjectView` |

## Intentional Architecture Decisions

### Home Preview data is a performance boundary

`src/data/home/about.json`, `journey.json`, and `projects.json` are intentionally imported into the Home bundle. This means:

- Home preview content renders without waiting for the backend.
- A Cloud Run backend cold start does not leave Profile, Journey, or Projects blank.
- The payload is small and the preview covers are not requested while `image_ready` is false.
- Full detail content remains backend-owned and is loaded only on detail routes.

The trade-off is manual summary synchronization, not an architectural defect by itself. Removing local JSON or replacing it with runtime fetching would weaken the explicit first-screen strategy and is not recommended without a new performance requirement.

`App.vue` does request About metadata for “Last updated,” but that asynchronous request does not block Home preview rendering; the fallback remains `—`.

### Other intentional decisions worth preserving

- Timeline is hidden below 768px rather than compressed into Journey content. Mobile retains a readable single-column Journey.
- Page interaction state stays in its View. There is no demonstrated cross-page state requiring Pinia or Vuex.
- `contentApi.js` is a small content facade that normalizes the same v1 envelope for four resources.
- Feature CSS is globally imported but uses recognizable `about-*`, `journey-*`, `project-*`, and layout selector conventions.
- `ProjectCover` owns one shared 160×100 (16:10) specification for Home and Project cards, including placeholder and image failure behavior.
- `ProjectAction` centralizes Live → Source → Internal precedence across Home and Project.
- `DetailPageHeader` centralizes detail breadcrumb semantics and header hierarchy.
- Detail routes use one full-width shell while only Home uses Sidebar + Main Content.

## App.vue Review

### Current responsibilities

`App.vue` currently owns:

- route access and `meta.layout` interpretation;
- Home versus detail shell classes;
- complete Home Sidebar markup and navigation;
- duplicated desktop/mobile social and resume links;
- About API request for Last updated;
- `RouterView` placement;
- fixed Mobile footer markup;
- Home hash scrolling in the inner `.main-content` container;
- measurement of profile/footer/viewport and three root CSS variables;
- global mouse glow and wheel proxy composables;
- resize listener and route watcher lifecycle.

The problem is not its 188-line size by itself. The coupling comes from shell rendering, content/config duplication, backend metadata, DOM queries, scrolling, responsive measurement and global effects changing for different reasons in the same file.

### Responsibility decisions

| Responsibility | Recommendation | Reason / proposed location |
|---|---|---|
| Route meta + top-level shell selection | Keep in `App.vue` | This is the root application concern |
| `RouterView` | Keep in `App.vue` | No benefit from wrapping it solely for symmetry |
| Cursor glow element + activation | Keep initially | It is global; later pass an element ref to `useMouseGlow` to remove repeated selector lookup |
| Sidebar profile/navigation markup | Extract | `src/components/layout/HomeSidebar.vue`; cohesive Home-shell UI |
| Desktop/mobile social links | Extract shared renderer | `src/components/layout/SocialLinks.vue` plus `src/config/siteLinks.js`; removes duplicated URLs and labels |
| Mobile footer | Extract after SocialLinks | `src/components/layout/MobileFooter.vue`; owns footer markup, receives `updatedTime` |
| Last updated loading | Keep in App during first shell split | Both desktop and mobile shell consume it; a one-purpose composable is optional only if retry/loading policy grows |
| Hash/inner scroll behavior | Move to focused composable | `useHomeSectionNavigation({ route, containerRef })`; currently route and DOM scrolling ownership is split between Router and App |
| Header/footer/viewport measurements | Move to focused composable | `useHomeViewportMetrics({ headerRef, footerRef })`; owns resize listener and CSS variables |
| Wheel proxy | Keep as composable, revise API later | Accept a content ref and an enabled computed value instead of global DOM queries |
| Layout components `HomeLayout`/`DetailLayout` | Defer | With only two simple shells, introducing route slots/nested layouts now adds indirection before the concrete Sidebar/DOM concerns are isolated |

### Recommended final App ownership

After a minimal shell refactor, `App.vue` should own route/layout selection, shared Last updated state, root global effect activation, and `RouterView`. Home-specific markup and duplicated link data should be children; DOM measurement and hash scrolling should be composables with explicit inputs. A wholesale App rewrite or nested-route conversion is not justified.

## Views Review

### HomeView.vue

- **Responsibilities:** compose Profile, three Journey previews and three Project previews; render detail links.
- **State/loading:** none. All three JSON files are static ES-module imports.
- **Logic:** only `v-for` mapping and stable display keys.
- **Assessment:** clean route composition. It should remain a View rather than split into three wrapper components with no state or reuse.
- **Possible improvement:** if section markup grows, `HomeProfilePreview` could become useful, but current 65-line View does not justify it.

### AboutView.vue

- **Responsibilities:** fetch About, normalize sections defensively, render loading/error/empty/success, compose `DetailPageHeader` and `AboutSection`.
- **State:** `sections`, `loading`, `error`.
- **Lifecycle:** one `onMounted` request.
- **Assessment:** responsibility is cohesive and small. A generic page-loader composable would abstract only a few lines while obscuring page-specific messages and shapes.
- **Recommendation:** keep as-is; prioritize tests over decomposition.

### JourneyView.vue

- **Data loading:** concurrently loads Journey and Timeline Events, then owns both arrays and the combined error/loading state.
- **Interaction state:** `expandedJourneySlug`, `leavingDetailSlugs`, and `activeJourneySlug`.
- **Row calculation:** `detailRowSlugs`, `journeyRows`, and `timelineRows` keep Timeline and content on shared CSS Grid rows while preserving a leaving detail row.
- **Coordination:** maps section hover/focus to Timeline active slug and coordinates one-expanded behavior.
- **DOM/animation:** owns dynamic-height enter/leave hooks, `scrollHeight`, inline height/opacity/transform, `inert`, and `aria-hidden`.
- **Template:** composes header rows, conditional detail rows, Timeline props and transition completion.

The View correctly owns cross-component orchestration; moving all of it into `JourneySection` or `Timeline` would recreate coupling. Two boundaries are still valuable:

1. `useJourneyRows(journeyItems)` — pure/reactive row-state coordination.
   - **Input:** `journeyItems` ref.
   - **Owns:** `expandedJourneySlug`, `leavingDetailSlugs`.
   - **Outputs:** `detailRowSlugs`, `journeyRows`, `rowBySlug`, `toggleJourney(slug)`, `finishDetailLeave(slug)`.
   - **DOM dependency:** none.
   - **Benefit:** row lifecycle can be tested without rendering Timeline.
2. `useAutoHeightTransition()` — shared DOM transition hooks.
   - **Outputs:** `beforeEnter`, `enter`, `afterEnter`, `beforeLeave`, `leave`.
   - **Consumers:** `JourneyView` and `ProjectCard`.
   - **Benefit:** removes duplicated height/inert behavior and creates one reduced-motion/animation contract.

`activeJourneySlug` and activate/deactivate focus coordination should stay in the View because they synchronize sibling components. API loading should also stay at the route boundary.

### ProjectView.vue

- **Responsibilities:** fetch Projects, own search/category/technology filters, derive options/results, enforce one expanded Project, clear hidden expansion, render tool/empty/card states.
- **State:** projects/loading/error, expanded slug, three filter values.
- **Computed:** category options, technology options, filtered projects, active-filter flag.
- **Watch:** closes an expanded card only when filtering removes it.
- **Utility ownership:** tokenization and exact matching already live in pure `projectSearch.js`.
- **Assessment:** cohesive and sufficiently clean. A `useProjectFilters` composable would mostly relocate straightforward page-local state and is not currently justified.
- **Recommendation:** keep filtering and expansion in the View; add utility tests first.

## Components Review

| Component | Consumers | Props / emits | Owned behavior | Assessment |
|---|---|---|---|---|
| `AboutSection.vue` | `AboutView` | `section`; no emits | Semantic section/paragraph/list rendering | Correct, page-specific, stateless; no split needed |
| `HomeJourneyItem.vue` | `HomeView` | `journey`; no emits | Logo lookup + compact row | Name matches responsibility; Home-specific |
| `JourneySection.vue` | `JourneyView` | `journey`, `expanded`; emits `toggle(slug)` | Header, toggle semantics, logo mapping | Correct boundary: does not know Timeline or detail rendering |
| `JourneyDetail.vue` | `JourneyView` | `journey`; no emits | Conditional detail sections and skill/technology dedupe | Cohesive page-specific renderer; no further split needed at three records |
| `Timeline.vue` | `JourneyView` | journeyItems/events/active slug/detail slugs/row map; emits activate/deactivate | Timeline DOM, event placement, dates, focus/hover | Rendering boundary is correct; pure date/placement math is extractable |
| `HomeProjectPreview.vue` | `HomeView` | `project`; no emits | Compact summary using shared cover/action | Correct Home-specific component |
| `ProjectAction.vue` | Home preview + Project card | `project`, `name`; no emits | Link precedence and accessibility labels | Genuinely shared; name matches behavior |
| `ProjectCard.vue` | `ProjectView` | `project`, `expanded`; emits `toggle(slug)` | Summary, details, interaction and dynamic-height transition | Multiple responsibilities; a measured split can improve tests |
| `ProjectCover.vue` | Home preview + Project card | image/alt/ready; no emits | image-error state and placeholder | Genuinely shared and appropriately stateful |
| `DetailPageHeader.vue` | all three detail Views | current/headingId/title/description; no emits | Breadcrumb and page heading semantics | Correct cross-page layout component |

### Timeline.vue deep review

Keep in `Timeline.vue`:

- period/node/segment/event DOM;
- date and event labels as presentation output;
- active class application;
- hover/focus event emission;
- accessible node labels;
- connector and detail-row rendering semantics.

Extract to `src/utils/journey/timelineMath.js`:

- `monthIndex(value)`;
- journey bounds from start/end/current month;
- `eventFitsJourney()`;
- `datePosition()`;
- optionally `groupTimelineEvents(journeyItems, events, currentMonthIndex)`.

The utility should receive the current month as input rather than reading `new Date()` internally, making Present positioning deterministic in tests. Formatting can remain in the component unless it is also tested independently.

Do not split nodes, labels and event markers into several child components yet. Their DOM is tightly coordinated on one axis, they have no independent state, and additional prop/event plumbing would increase rather than reduce coupling.

### ProjectCard.vue deep review

Current concerns are summary header/toggle behavior, dynamic-height transition, conditional detail normalization and full detail rendering. Two changes are defensible:

- Share `useAutoHeightTransition()` with Journey.
- Extract `ProjectDetail.vue` only after that, passing one `project` prop. It would own conditional Overview/Responsibilities/Architecture/Challenges/Deployment/Lessons/Technology rendering; `ProjectCard` would retain header, expanded prop, toggle emit and Transition.

Benefit: detail rendering becomes component-testable and ProjectCard changes no longer mix header interaction with section markup. Cost: one more page-specific component and prop boundary. It is medium priority, not an urgent split based only on line count.

## API Layer Review

### client.js

`requestRaw(path)` owns API-base concatenation, Fetch, JSON parsing, HTTP-status checking and extraction of the backend error message. Current limitations:

- it calls `res.json()` before checking status, so HTML/plain-text gateway failures become JSON parse errors;
- no timeout or `AbortController` support;
- no caller signal, headers or request context;
- an absent `VITE_API_BASE` produces an invalid URL without an early configuration error.

`request(path)` only returns `json.data` and has zero consumers. It should either become the standard path used by `contentApi.js` with metadata handled deliberately, or be removed. Because consumers need `meta.updated_at`, adopting it as written would lose data; removal is the clearer Phase 0 choice.

### contentApi.js

The four functions use the same endpoint family and return the same `{content, updatedAt}` normalization. The file is small and cohesive.

Answers to the requested architecture questions:

1. **Split by resource?** No. Four tiny functions do not justify four files.
2. **Keep one Content API facade?** Yes. It gives Views a stable normalized boundary and hides the v1 envelope.
3. **Add `api/index.js`?** No. There is one facade; a barrel adds another import layer without simplifying ownership.
4. **`request()`?** Remove it unless a real data-only consumer appears. Do not keep dead alternatives.
5. **Add `services/`?** No. `contentApi.js` already performs the only frontend service-like adaptation needed. An additional pass-through layer would duplicate responsibility.

## Composables and Utilities Review

| File | Consumers | Nature | Findings / recommendation |
|---|---|---|---|
| `useMouseGlow.js` | `App.vue` | Vue lifecycle + global DOM side effect | Correct composable category; queries `.cursor-glow` and reads dimensions on every mousemove. Later accept an element ref and consider reduced-motion/coarse-pointer enablement |
| `useScrollProxy.js` | `App.vue` | Vue lifecycle + global wheel interception | Correct category but strongly selector-coupled. Accept the content ref/enabled state; review nested scroll and keyboard behavior before changing |
| `useProjectHelpers.js` | `ProjectCard` | Pure helper factory, no Vue API | Misclassified as composable. Only `safeArray` is consumed; `isFeaturedProject`, `previewEngineering`, `getGithubLink`, and `getDemoLink` are dead exports based on the complete import scan |
| `journeyLogos.js` | Home Journey + Journey Section | Pure asset mapping | Correct utility and shared consumer boundary |
| `projectSearch.js` | `ProjectView` | Pure domain utility | Correct location; strongest immediate unit-test target |

`safeArray` does not require a dedicated composable. The lowest-cost cleanup is a local helper in `ProjectDetail.vue` if that component is extracted, or a named pure export in a general utility only when a second consumer exists.

## State Management Review

Current state is route-local:

- About request state is used only by About.
- Journey API, hover, expansion and row state are used only by Journey.
- Project filters and expansion are used only by Projects.
- App owns only shell/route metadata and Last updated.

There is no cross-route writable domain state, shared cache, authentication state or multi-page workflow. Introducing Pinia would add dependency, conventions and indirection without solving an existing problem. **Do not introduce Pinia now.** Re-evaluate only if several routes need shared mutable state or client-side caching with coordinated invalidation.

## CSS Architecture Review

### Current structure and cascade

`main.js` imports Bootstrap, Bootstrap Icons, then these files in order:

```text
main.css → main-rwd.css
projects.css → projects-rwd.css
about.css → about-rwd.css
journey.css → journey-rwd.css
```

- Global tokens (`--site-bg`, text colors, layout widths) live in `main.css`.
- Project cover tokens live in a second `:root` block in `projects.css`.
- Shared shell, breadcrumb and page states live in `main.css`.
- Home and detail feature rules share the same About/Journey/Projects files.
- Breakpoints are consistently centered on 1024px and 768px, but rule ordering varies. For example, some mobile blocks precede tablet blocks and rely on `!important` or later duplicate mobile blocks.
- Shared `.tag` styles live in `projects.css` but are consumed by `JourneyDetail`, so actual ownership is broader than the filename suggests.
- `.home-journey-link` is defined in `journey.css` but used by Profile and Projects section headers as well.
- `.project-category` is in `main.css`, while its only current consumer is ProjectCard.
- Component-specific styles are not colocated; correctness depends on global import order and selector uniqueness.

### Confirmed cleanup candidates

Static template/import scan found no runtime consumers for these selectors:

- `.code-btn`
- `.tag-lang`
- `.see-more-wrapper`
- `.see-more-btn`
- `.section-footer-link`
- `.exp-gpa`
- mobile `#exp` (the current Home id is `#journey`)

They should be rechecked against any runtime-generated content before removal, but no Vue/JS consumer exists today.

### Hardcoded/shared styles

Accent/focus colors such as `#9bbcff` and `#4da4ff`, low-contrast borders, surface alpha, radius and transition durations recur across files instead of using tokens. Bootstrap utilities and custom rules coexist; responsive files contain multiple `!important` declarations because utilities/cascade otherwise win.

### Minimum-risk CSS plan

1. Remove only verified dead selectors, one feature file at a time.
2. Document selector ownership and stop adding cross-feature styles to feature files.
3. Add a small set of missing shared variables to the existing `main.css :root` rather than immediately introducing a ninth file.
4. Move shared tag/focus/link primitives only when both current consumers are regression-tested.
5. Normalize duplicate breakpoint blocks inside each feature without changing import order.

This avoids a global cascade migration during active visual work.

### Long-term CSS plan

If the site grows, introduce `tokens.css` first, imported before `main.css`, then separate `layout.css` from feature rules. Component CSS files or scoped styles can be adopted selectively for newly stable components, not through a one-shot conversion. Tailwind, Sass, CSS Modules and a new design system are not justified by current needs.

## Home Preview Data Review

### Current mapping and drift surface

| Home file | Home fields | Backend equivalents / notes |
|---|---|---|
| `about.json` | `paragraphs` | Deliberately shorter copy than backend structured sections; not expected to be identical |
| `journey.json` | logo, position, name, duration, short_description | logo, title, organization, period, summary |
| `projects.json` | name, image, image_alt, image_ready, introduction, tags, URLs | title, cover, cover_alt, cover_ready, summary, technologies, URLs |

Journey and Project previews currently match backend summary content semantically. Likely drift points are dates/period, title/organization, summary wording, cover path/readiness, technologies/tags and external URLs. MRIS uses an empty `website_url` in Home JSON while backend uses `null`; rendering is equivalent, but it demonstrates schema-convention drift.

Home-only concerns should stay local: preview wording, `short_description`/`introduction`, preview selection/order, and whether a preview image is ready. Full detail sections must remain backend-only.

### Validation/generation recommendation

With three fixed items, manual synchronization plus review is currently acceptable. A small build-time audit becomes worthwhile when content changes frequently. It could map Home records to backend records by a stable slug and verify shared fields without fetching at runtime. Full generation is not yet recommended because:

- Home preview copy is intentionally shorter;
- frontend and backend deploy independently;
- generated content would still require rebuilding the frontend;
- Project repository discovery is explicitly ordered.

Do not switch Home to runtime API loading or add SWR in the current architecture.

## Routing and Page Metadata Review

- Four routes are valid and stable: `/`, `/about`, `/journey`, `/project`.
- `meta.layout` is the only route metadata and is correctly consumed by App.
- Router `scrollBehavior()` resets document scroll; App separately manages Home's inner `.main-content` and hash offsets. This split should be consolidated during the shell refactor, not patched independently.
- There is no catch-all 404 route. A small Not Found View is a high-value, low-risk quality task after shell ownership is clearer.
- Singular `/journey` and `/project` naming is established and does not justify breaking links.
- All Views are eagerly imported. The production bundle is currently small; route-level lazy loading is optional, not urgent.
- `index.html` has an empty `lang`, a generic title, and no description/canonical/Open Graph/Twitter/structured metadata.
- Document title and metadata have no route owner.

Priority:

- **Now/cleanup:** set `lang` only in a dedicated metadata task; add 404 after shell work.
- **After shell refactor:** consolidate Home hash/scroll ownership.
- **SEO phase:** route-aware titles/descriptions, canonical, Open Graph and structured data.
- **Do not change:** existing route URLs solely for plural consistency.

## Dependencies and Build Review

### Dependencies

- Axios has no source import; Fetch is the only HTTP transport. Axios is a verified unused dependency candidate.
- Bootstrap CSS utilities are used broadly in templates; Bootstrap must remain unless those utilities are deliberately replaced.
- Bootstrap Icons are used in App and page error states.
- Vue and Vue Router are active core dependencies.
- No other declared runtime dependency is clearly unused.

### Vite and DevTools

`vite-plugin-vue-devtools` is included unconditionally in `vite.config.js`. It should be enabled only for development mode, or removed if the team does not use it. This is a build cleanup, not an application architecture requirement.

### Docker and Nginx

- Docker copies lockfiles first but runs `npm install`; production builds should use `npm ci` for lockfile fidelity.
- No frontend `.dockerignore` exists. Local `node_modules`, `dist`, logs and editor/cache files can enter the Docker build context even though not all reach the final Nginx stage.
- `node:20` is floating while package engines require a recent Node 20 or Node 22; pinning an appropriate image patch is deployment hardening.
- Nginx `try_files $uri /index.html` correctly supports direct SPA route refresh.
- Nginx and container both listen on fixed 8080, matching the current Cloud Run setup.

### Environment configuration

`VITE_API_BASE` is read at build time, and both development/production env files are tracked. This keeps runtime simple and explicit but requires a frontend rebuild to change backend location. It is acceptable for the current two-service deployment; runtime config is only worthwhile if one immutable frontend image must serve multiple environments.

Immediate cleanup candidates are Axios removal, devtools mode gating, `npm ci`, and `.dockerignore`. Node image pinning and runtime environment injection belong to deployment hardening.

## Testing Review

There are no frontend unit, component or E2E tests. A minimal risk-ordered strategy is:

1. **Pure utility tests (highest immediate value)**
   - Project whole-token search: `.NET`, `Vue.js`, hyphens, AND matching and substring rejection.
   - Category/technology exact filters and unique option sorting.
   - Extracted Timeline month/bounds/event-position calculations, including Present and invalid/cross-section events.
2. **API normalization tests**
   - v1 `{data, meta}` mapping.
   - JSON and non-JSON HTTP errors.
   - timeout/abort behavior after client hardening.
3. **Focused component/View tests**
   - About loading/error/empty/success.
   - Journey one-expanded state and leaving-row completion.
   - Project filters clearing a hidden expanded card.
   - Home local data renders without API calls.
4. **Small E2E smoke layer**
   - direct navigation/refresh for all four routes;
   - Home hash navigation on desktop/mobile;
   - Journey/Project keyboard expand and external-link behavior;
   - API failure states.

Do not begin with a broad snapshot suite. Protect domain calculations and state transitions first.

## Proposed Target Structure

### Minimal Refactor Target

Only add these files when their phase is implemented:

```text
frontend/src/
├── App.vue
├── api/
│   ├── client.js
│   └── contentApi.js                 # remains a single facade
├── components/
│   ├── layout/
│   │   ├── DetailPageHeader.vue
│   │   ├── HomeSidebar.vue           # from App sidebar markup
│   │   ├── MobileFooter.vue          # from App mobile footer
│   │   └── SocialLinks.vue           # shared desktop/mobile links
│   └── projects/
│       └── ProjectDetail.vue         # optional Phase 2 extraction
├── composables/
│   ├── useAutoHeightTransition.js    # shared Journey/Project hooks
│   ├── useHomeSectionNavigation.js   # App hash/inner scroll logic
│   └── useHomeViewportMetrics.js     # App DOM measurement lifecycle
├── config/
│   └── siteLinks.js                  # social/resume data source
└── utils/
    ├── journeyLogos.js
    ├── projectSearch.js
    └── timelineMath.js                # pure date/placement logic
```

No `store/`, `services/`, API resource files, layout framework or empty directory is proposed. `useJourneyRows` should be added only if row-state tests demonstrate value; it can remain in `JourneyView` until then.

### Long-term Target

Only if routes/features continue to grow:

```text
frontend/src/
├── layouts/
│   ├── HomeLayout.vue
│   └── DetailLayout.vue
├── assets/css/
│   ├── tokens.css
│   ├── layout.css
│   └── feature files
└── tests/
    ├── unit/
    ├── components/
    └── e2e/
```

Layouts become valuable only if more shells/routes appear. A separate tokens file becomes valuable when shared values have an inventory and visual regression coverage. TypeScript, Pinia, SSR/Nuxt, Tailwind and a UI library are not part of the evidence-based target.

## Refactor Plan

| Phase | Candidate | Risk | Value | Main files | Immediate? / expected benefit |
|---|---|---|---|---|---|
| 0 — Cleanup | Remove Axios and unused `request()`/Project helper exports | Low | Medium | package files, `client.js`, `useProjectHelpers.js`, `ProjectCard.vue` | Yes; removes dead alternatives and misleading ownership |
| 0 — Cleanup | Remove verified dead CSS selectors | Low–Medium | Medium | main/journey/projects CSS + RWD | Yes, in small reviewed batches; reduces cascade noise |
| 0 — Cleanup | Gate Vue DevTools by mode; add frontend `.dockerignore`; use `npm ci` | Low–Medium | Medium | Vite config, Dockerfile, new `.dockerignore` | Yes as a separate build cleanup |
| 1 — Application Shell | Extract Sidebar/SocialLinks/MobileFooter and link config | Medium | High | `App.vue`, new layout components/config | Yes; removes duplicate URLs and shell markup from root |
| 1 — Application Shell | Extract Home navigation and viewport metric composables with element refs | Medium | High | `App.vue`, current composables, new composables | Yes after shell components; reduces selector/lifecycle coupling |
| 1 — Application Shell | Introduce full Home/Detail layout components | Medium | Low–Medium | App/router/new layouts | Defer; only valuable if shells/routes grow |
| 2 — Complex Feature | Extract/test Timeline date and event-placement math | Medium | High | `Timeline.vue`, new `timelineMath.js` | Yes; deterministic domain logic and highest Timeline regression value |
| 2 — Complex Feature | Share dynamic-height transition hooks | Medium | Medium–High | `JourneyView`, `ProjectCard`, new composable | Yes with component regression checks; one animation/a11y contract |
| 2 — Complex Feature | Extract `ProjectDetail.vue` | Medium | Medium | `ProjectCard`, new component | After transition extraction; isolates detail rendering |
| 2 — Complex Feature | Extract all Project filters to composable | Low | Low | `ProjectView` | No; current View is already cohesive |
| 3 — CSS Ownership | Inventory tokens/shared primitives and normalize breakpoint ordering | Medium | High | all eight CSS files, `main.js` | Yes incrementally; reduces import-order surprises |
| 3 — CSS Ownership | Add `tokens.css`/`layout.css` or scoped CSS migration | High | Medium | global CSS/imports/components | Defer until inventory/tests exist; broad visual regression risk |
| 4 — Quality | Add pure utility and API tests | Low–Medium | High | test config + utilities/API | Yes; protects highest-risk logic cheaply |
| 4 — Quality | Add focused View/component and E2E smoke tests | Medium | High | Views/components/test config | Yes incrementally, not as a large suite |
| 4 — Quality | Add catch-all 404 and route metadata/SEO | Low–Medium | High | router, index, possible metadata composable | 404 after shell; metadata in dedicated SEO phase |
| 4 — Quality | Accessibility audit at 200% zoom, keyboard and reduced motion | Medium | High | shell, Journey, Projects, CSS | Yes after refactors stabilize |

## Keep / Defer Decisions

Keep as-is unless new evidence appears:

- Home local preview JSON strategy.
- One `contentApi.js` facade.
- View-local state and absence of Pinia.
- Existing route URLs.
- `ProjectCover`, `ProjectAction`, `DetailPageHeader`, Journey Section/Detail boundaries.
- Mobile-hidden Timeline.
- JavaScript rather than a TypeScript migration.

Defer:

- full layout framework;
- API files split by resource;
- global store;
- full scoped-CSS/CSS Modules/Tailwind/Sass conversion;
- SSR/Nuxt;
- broad component fragmentation;
- backend-driven Home runtime content;
- API contract changes.

These would currently add migration cost without addressing the observed coupling boundaries.
