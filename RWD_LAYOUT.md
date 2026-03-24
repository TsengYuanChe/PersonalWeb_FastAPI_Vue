# RWD & Layout Optimization Notes

## Current Layout Analysis

### Desktop shell (updated)
- `.layout-container` is now fluid:
  - `width: 100%`
  - `max-width: 1200px`
  - centered with `margin: 0 auto`
  - responsive horizontal padding via `padding-inline: clamp(16px, 2vw, 24px)`
- Grid columns are aligned with sidebar width:
  - `grid-template-columns: 320px minmax(0, 1fr)`
  - `.sidebar { width: 320px; box-sizing: border-box; }`
- `.main-content` remains readable and fluid:
  - `width: 100%`
  - `max-width: 1000px`
  - `margin: 0 auto`
  - `min-width: 0` to reduce overflow risk

### Mobile shell
- Existing mobile system remains unchanged:
  - fixed header/footer pattern under `max-width: 768px`
  - scroll container remains `.main-content`
  - dynamic CSS vars (`--header-height`, `--footer-height`, `--real-vh`) still drive mobile height.

## Responsive Design Issues (remaining)

- Wheel proxy still globally intercepts scroll input (`useScrollProxy.js`), which may cause accessibility/UX friction in some contexts.
- Mobile header/footer relies on runtime DOM injection (`useMobileFooter.js`), which adds maintenance complexity and potential layout-shift risk.
- High `!important` usage in `*-rwd.css` can make overrides harder to maintain.
- Spacing/typography scales are still section-local rather than tokenized globally.

## Change Record (High Priority #1)

- Implemented shell fluid-width model in `frontend/src/assets/css/main.css`.
- Removed fixed-width canvas behavior (`width: 1300px`).
- Resolved grid/sidebar width mismatch (`280px` vs `350px`) by unifying to `320px`.
- Maintained desktop visual structure while improving mid-size adaptability.
