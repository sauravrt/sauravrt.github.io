# Site Foundation - Low-Level Design

**Created**: 2026-11-13
**Status**: Approved
**HLD Link**: [High-Level Design](../../high-level-design.md)

## Overview

The site foundation defines the Zola project structure, shared templates,
navigation, visual system, metadata, and accessibility behavior used by every
page. It deliberately uses local Tera templates and plain CSS rather than a
packaged theme or front-end framework.

## Project Structure

```text
.
├── config.toml
├── content/
│   ├── _index.md
│   ├── about.md
│   ├── posts/
│   │   └── _index.md
│   └── technical/
│       └── _index.md
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── page.html
│   ├── 404.html
│   ├── partials/
│   │   ├── head.html
│   │   ├── header.html
│   │   ├── footer.html
│   │   └── profile-links.html
│   └── components/
│       └── entries.html
└── static/
    ├── styles/site.css
    ├── images/
    └── favicon assets
```

Posts, technical entries, and exported artifacts add to this structure as
defined in their own LLDs.

## Site Configuration

`config.toml` is the canonical location for site-wide identity and external
profiles.

| Field | Required | Purpose |
|---|---:|---|
| `base_url` | Yes | `https://sauravrt.github.io` |
| `title` | Yes | Site title used in headers and metadata |
| `description` | Yes | Default search/social description |
| `default_language` | Yes | English (`en`) |
| `generate_feeds` | Yes | Enable the site feed |
| `feed_filenames` | Yes | Use one documented feed filename |
| `build_search_index` | Yes | Disabled for the initial release |
| `taxonomies` | Yes | Define the post `tags` taxonomy |
| `author` | Yes | Display, feed, and metadata author name |
| `extra.profiles` | Yes | Named external profile URLs |

The Flickr URL will be stored once under `extra.profiles` and rendered through
the shared profile-links partial. The supplied URL is
`https://www.flickr.com/photos/sauravrt/`.

## Page Types

| Page | Template | Main content |
|---|---|---|
| Home | `index.html` | Full reverse-chronological Posts list |
| About | `page.html` | Biography and profile links |
| Section index | Feature-specific section template | Chronological content list |
| Article | Feature-specific page template | Title, metadata, body |
| 404 | `404.html` | Brief error and links back to core sections |

`base.html` owns the document shell, skip link, header, main landmark, and
footer. Child templates replace named blocks and must not duplicate the shell.

## Navigation Contract

Primary navigation contains:

1. About
2. Posts
3. Technical

The site title and Posts navigation link lead to `/`, which lists all published
posts; `/posts/` remains available as a compatible index route. Flickr is an external profile link, not a primary
content section. It will appear with other profile links on About and in the
footer. External links must have visible names; icon-only links are not used.

The narrow-screen navigation will wrap or use a simple always-visible layout.
It will not depend on a JavaScript menu.

## Visual System

CSS custom properties in `static/styles/site.css` define:

- A system-font text stack and a system monospace stack.
- A restrained text, muted text, background, border, link, and focus palette.
- A small type scale and spacing scale.
- A readable content width of approximately `65ch` to `72ch`.
- A wider container only for indexes or technical material that requires it.

The initial implementation will support the browser's light and dark color
preferences through `prefers-color-scheme`, without a persisted theme toggle.
Motion is optional and disabled when `prefers-reduced-motion` is set.

No CSS preprocessor, web-font download, utility framework, or icon package is
required.

## Metadata Contract

The head partial resolves metadata in this order:

1. Page-specific title/description.
2. Section-specific title/description.
3. Site defaults.

Every public page receives:

- UTF-8 and responsive viewport declarations.
- A unique `<title>`.
- A meta description.
- Canonical URL.
- Feed discovery link.
- Basic Open Graph metadata.
- Favicon links.

Article pages additionally receive publication and modification metadata when
available. Structured data can be added only if it can be generated reliably
from existing content fields.

## Accessibility Contract

- A keyboard-visible skip link targets the main content.
- The current navigation item is exposed with `aria-current="page"`.
- Heading levels follow the page hierarchy and each page has one primary
  heading.
- Links are distinguishable without relying only on color.
- Focus indicators are never removed.
- Text and interactive controls meet WCAG AA contrast targets.
- Code, tables, equations, and long URLs do not force page-wide horizontal
  scrolling.
- External profile links remain understandable without icons or tooltips.

## Error and Empty States

| Condition | Behavior |
|---|---|
| Missing page | Render the custom 404 page with links to Home, Posts, and Technical |
| No posts yet | Render a short neutral message instead of an empty list |
| No technical entries yet | Render a short neutral message and retain section context |
| Optional profile missing | Omit that profile link; do not render an empty anchor |
| Missing description | Build validation reports it for content types that require it |

Zola/template errors should fail the build rather than silently render
placeholder text. Other metadata omissions are checked during manual review.

## Dependencies

- Zola, pinned by the deployment design.
- Browser-native HTML and CSS behavior.
- User-provided biography, profile URLs, and favicon/identity assets.

There are no runtime application dependencies.

## Open Inputs

- Final site title and default description.
- About-page biography and preferred contact/profile links.
- Whether both automatic light and dark palettes are desired; the current
  design assumes both with no manual toggle.

## Requirements

- [Navigation EARS](./navigation-EARS.md)
- [Page Rendering EARS](./page-rendering-EARS.md)
- [Accessibility EARS](./accessibility-EARS.md)
- [External Profiles EARS](./external-profiles-EARS.md)

## Related Documents

- [High-Level Design](../../high-level-design.md)
- [Writing Migration LLD](../writing-migration/LLD.md)
- [Technical Library LLD](../technical-library/LLD.md)
- [Publishing and Deployment LLD](../publishing-deployment/LLD.md)
