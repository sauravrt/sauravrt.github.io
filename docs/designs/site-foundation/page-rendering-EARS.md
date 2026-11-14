# Page Rendering - EARS

**Parent LLD**: [Site Foundation LLD](./LLD.md)

## Document Structure

- [ ] **SITE-RENDER-001**: Every site-rendered page shall contain a header, a `main` landmark, and a footer.
- [ ] **SITE-RENDER-002**: Every public site-rendered page shall contain exactly one primary page heading.
- [ ] **SITE-RENDER-003**: The site shall render Home, About, Posts, Technical, and 404 pages from shared local Tera templates.
- [ ] **SITE-RENDER-004**: While JavaScript is unavailable, the site shall render all primary written content and links.
- [ ] **SITE-RENDER-005**: The site shall constrain prose to a readable line length between approximately 65 and 72 characters at wide viewport sizes.

## Metadata

- [ ] **SITE-RENDER-010**: Every public page shall render a non-empty, page-specific HTML title.
- [ ] **SITE-RENDER-011**: Every public page shall render a non-empty meta description.
- [ ] **SITE-RENDER-012**: Every public page shall render one canonical URL derived from the production base URL.
- [ ] **SITE-RENDER-013**: Every public page shall expose the configured site feed through a discovery link.
- [ ] **SITE-RENDER-014**: Every public page shall render basic Open Graph title, description, URL, and type metadata.

## Presentation

- [ ] **SITE-RENDER-020**: The site shall use local CSS without requiring a CSS framework or downloaded web font.
- [ ] **SITE-RENDER-021**: Where the user's system requests a dark color scheme, the site shall render the dark design-token palette.
- [ ] **SITE-RENDER-022**: Where the user's system requests reduced motion, the site shall disable non-essential animation and smooth scrolling.
- [ ] **SITE-RENDER-023**: If optional content is absent, then the site shall omit its element instead of rendering placeholder or empty markup.
- [D] **SITE-RENDER-024**: The site shall provide a manual persisted color-scheme selector.

## Related Documents

- [Site Foundation LLD](./LLD.md)
