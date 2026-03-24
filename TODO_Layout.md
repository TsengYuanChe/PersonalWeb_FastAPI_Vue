PORTFOLIO RWD / LAYOUT TODO

Goal:
Improve layout consistency, responsiveness, and UX stability
while preserving current visual design.

--------------------------------------------------

[IMPLEMENTATION STRATEGY]

- Apply changes ONE at a time
- After each change:
  - verify desktop layout
  - verify mobile layout
  - check scroll behavior
  - run production build
- Do NOT combine multiple layout changes in one step

--------------------------------------------------

[HIGH PRIORITY]

1. ✅ Unify shell width model

What:
- Remove fixed width: 1300px
- Replace with max-width + responsive padding
- Align grid column width with sidebar width

Why:
- Prevent layout overflow and misalignment
- Improve behavior on mid-size screens

Where:
- frontend/src/assets/css/main.css
  - .layout-container
  - .sidebar
  - .main-content

--------------------------------------------------

2. ✅ Constrain wheel proxy behavior

What:
- Disable or limit useScrollProxy on mobile/touch devices
- Avoid global preventDefault on window

Why:
- Prevent scroll conflicts
- Improve accessibility and UX

Where:
- frontend/src/composables/useScrollProxy.js
- frontend/src/App.vue

--------------------------------------------------

[MEDIUM PRIORITY]

3. ✅ Stabilize mobile spacing and tap targets

What:
- Reduce DOM injection side effects
- Ensure layout dimensions are calculated before render

Why:
- Reduce layout shift (CLS)
- Improve visual stability

Where:
- frontend/src/composables/useMobileFooter.js
- frontend/src/App.vue
- frontend/src/assets/css/main-rwd.css

--------------------------------------------------

4. Introduce design tokens (spacing & typography)

What:
- Define shared spacing variables (e.g. --space-1, --space-2)
- Define typography scale

Why:
- Consistent layout rhythm
- Easier global adjustments

Where:
- frontend/src/assets/css/main.css
- section CSS files

--------------------------------------------------

5. Reduce !important usage

What:
- Refactor CSS specificity and load order

Why:
- Improve maintainability
- Reduce override conflicts

Where:
- frontend/src/assets/css/*-rwd.css

--------------------------------------------------

6. Standardize reusable UI primitives

What:
- Extract shared styles for:
  - cards
  - titles
  - tags

Why:
- Reduce duplication
- Improve consistency

Where:
- about.css
- exp.css
- projects.css

--------------------------------------------------

7. Add motion accessibility support

What:
- Respect prefers-reduced-motion

Why:
- Improve accessibility

Where:
- main.css
- useMouseGlow.js
- useSmoothScroll.js

--------------------------------------------------

[LOW PRIORITY]

8. Fix class naming issues

What:
- Correct typos (e.g. text-secondry)
- Remove unused styles

Why:
- Prevent silent UI bugs

Where:
- frontend/src/App.vue
- related CSS files

--------------------------------------------------

[OPTIONAL IMPROVEMENTS]

9. Move to mobile-first CSS

What:
- Switch from max-width to min-width strategy

Why:
- Cleaner responsive logic

--------------------------------------------------

10. Component-level responsive rules

What:
- Define responsive behavior per component

Why:
- Better scalability

--------------------------------------------------

11. Introduce container queries (optional)

What:
- Apply to cards/components

Why:
- More flexible layout behavior

--------------------------------------------------

[IMPORTANT RULES]

- Do NOT redesign UI
- Do NOT change visual identity
- Focus only on layout/system improvements
- Keep changes incremental and testable

--------------------------------------------------
