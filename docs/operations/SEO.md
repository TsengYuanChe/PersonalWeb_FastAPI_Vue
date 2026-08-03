# SEO

## Current Status

This is the technical SEO foundation phase for the portfolio. It establishes site-wide discovery and sharing metadata while portfolio copy and project narratives continue to be refined separately.

## Implemented

- English document language, descriptive site title, meta description, viewport, and theme color
- Root canonical URL for `https://adamtseng.com/`
- Open Graph title, description, type, and URL
- Summary Twitter Card title and description
- Crawl policy in `robots.txt` with sitemap discovery
- Sitemap entries for Home, About, Journey, and Projects
- JSON-LD for the public Person and WebSite identities
- Existing ICO and 16×16／32×32 PNG favicons retained

No suitable Open Graph image currently exists in the public assets, so `og:image` and `twitter:image` are intentionally omitted rather than pointing to a placeholder.

## Current SEO Strategy

This is a personal software engineering portfolio. SEO prioritizes reliable identity discovery and clear professional presentation for Adam Tseng as a Software Engineer, with emphasis on full-stack, backend, and system development. Content quality and project-specific language will be improved separately as the portfolio content is finalized.

## Future Improvements

- Improve project-specific titles and descriptions after content refinement
- Review structured data after the public content is finalized
- Add route-specific metadata and canonical handling when page content stabilizes
- Create and publish a final Open Graph image
- Submit the sitemap to Google Search Console
- Run Lighthouse SEO verification against the production site

## Maintenance Rule

Routine portfolio content updates do not require changes to this document. Architecture changes belong in the canonical architecture documents. Update this file only when the SEO strategy, metadata implementation, crawl configuration, structured data, or verification workflow changes.
