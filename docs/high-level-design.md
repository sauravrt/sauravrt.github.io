# Saurav's Personal Website - High-Level Design

**Created**: 2026-11-13
**Status**: Approved

**Validation scope**: Use Zola's built-in build/check commands, manual
mobile/desktop review, and a one-time migration checklist. No custom test suite,
browser-test framework, or automated accessibility gate is required.

## Problem Statement

The existing personal website is an incomplete generated MkDocs snapshot rather
than a maintainable source project. Its writing is split between
reStructuredText files and generated HTML, its images depend on old external
WordPress URLs, and it has no maintainable notebook-publishing workflow.

The replacement should be a small, durable Zola site that presents Saurav,
collects his writing, links to his photography on Flickr, and publishes
technical notebook exports without requiring a server-side application.

## Existing Content Inventory

The migration source at `/Users/saurav/Documents/sauravrt.github.io-main`
currently contains:

- 14 reStructuredText posts dated from 2011 through 2017.
- 2 generated technical pages: `Bayesian_Learning_Part1` and
  `beamforming_fft`.
- A minimal generated About page.
- Images and documents referenced primarily through external WordPress URLs.
- A generated MkDocs asset bundle that should not be carried into the new
  source project.

The destination repository is currently empty and is configured to publish the
GitHub Pages user site `sauravrt.github.io`.

## Goals

1. **Minimal personal presence** - Provide a fast, readable About/home page
   that introduces Saurav and links to the site's main sections.
2. **Maintainable writing** - List posts in reverse chronological order and
   give every post a stable, readable page.
3. **Complete legacy migration** - Convert all 14 RST posts and both technical
   HTML pages while retaining dates, titles, useful taxonomy, links, math, and
   old URLs where practical.
4. **Photography link** - Direct interested visitors to Saurav's existing
   Flickr profile without duplicating or embedding its gallery.
5. **Technical library** - Provide a dedicated index for static marimo and
   Jupyter exports, with direct, shareable pages and links to related writing or
   source code.
6. **Low operational burden** - Build deterministically with Zola and deploy to
   GitHub Pages through CI without a database or application server.
7. **Quality by default** - Support mobile layouts, keyboard navigation,
   semantic HTML, accessible color contrast, metadata, feeds, and a useful 404
   page.

## Non-Goals

- A content management system or browser-based editing interface.
- User accounts, comments, analytics, or other server-side features in the
  initial release.
- Full-text client-side search in the initial release; the content volume does
  not justify its weight yet.
- A JavaScript-heavy single-page application.
- Automatic execution of notebooks on the website.
- A local photo gallery, Flickr feed, or photo synchronization.
- Preserving the generated MkDocs theme, navigation, or asset bundle.
- Editing or modernizing the substance of old posts during mechanical
  migration, beyond clearly identified typo, markup, and broken-link fixes.

## Target Users

- **Prospective collaborator or employer** - Wants a concise introduction and
  examples of Saurav's technical interests and work.
- **Technical reader** - Wants readable posts, equations, code, and standalone
  notebook material.
- **Photography viewer** - Wants a clear route to Saurav's Flickr profile.
- **Saurav as author** - Wants a simple Git-based workflow for adding Markdown,
  profile links, and exported notebooks.

## Information Architecture

The primary navigation will remain intentionally small:

| Route | Purpose |
|---|---|
| `/` | Concise introduction, selected/recent work, and links onward |
| `/about/` | Longer biography, interests, and contact/profile links |
| `/posts/` | Reverse-chronological writing index |
| `/posts/<slug>/` | Individual article |
| `/technical/` | Marimo/Jupyter export library |

Flickr will be an external profile link rather than a local route. Its final
placement will be chosen with the other social/profile links in the Site
Foundation LLD.

Standalone notebook exports may live beneath a separate static path such as
`/labs/<slug>/`; the Technical page will provide the consistent human-facing
catalog. Final paths and whether each export also has a descriptive wrapper
page will be settled in the Technical Library LLD.

Old public slugs will be retained where they fit this structure. Zola aliases
or small redirect pages will cover changed routes so migration does not
needlessly break inbound links.

## Architecture Overview

```text
Authoring inputs
├── Markdown + TOML front matter (About, posts, library)
├── External profile links, including Flickr
├── Static marimo/Jupyter HTML exports
└── Local templates, CSS, fonts/icons as needed
                    │
                    ▼
               Zola build
       ┌────────────┼────────────┐
       │            │            │
       ▼            ▼            ▼
  HTML pages    RSS/Atom +    Static exports
                sitemap       and site assets
       └────────────┼────────────┘
                    ▼
        GitHub Actions validation/build
                    ▼
             GitHub Pages CDN
                    │
                    ▼
                 Readers
```

The public site remains fully static. Core navigation and reading must work
without JavaScript. JavaScript embedded by a notebook export is isolated to
that standalone technical artifact rather than loaded site-wide.

## Content Model

### About

A regular Zola page containing the biography and optional structured profile
links. The home page will reuse a shorter introduction rather than duplicating
the full biography.

### Posts

A Zola section containing one Markdown file or page bundle per article.
Required metadata includes title, publication date, and description. Optional
metadata includes updated date, tags, aliases, hero image, and related
technical artifact.

Legacy categories and tags will be normalized into a small taxonomy rather
than copying inconsistent values such as `Research`, `PhD Research`,
`signalprocessing`, and `Uncategorized` verbatim.

### External Profiles

Profile links, including Flickr, will be maintained as site configuration or
structured page metadata. Flickr content will not be fetched, embedded, or
copied into the site.

### Technical Library

Each catalog entry will record a title, summary, publication/update date,
format, export URL, optional source repository, and related post. Exported
marimo and Jupyter HTML remains static and directly addressable. The catalog,
site navigation, and metadata remain visually consistent with the main site
even when an export's internal presentation is self-contained.

## Key Design Decisions

### Decision 1: Zola with local minimal templates

**Choice**: Use Zola as the static site generator and build a small local Tera
template/CSS layer instead of installing a third-party Zola theme.

**Rationale**: The requested site has few page types. Local templates provide
exactly those types without inherited theme features, dependency upgrades, or
hard-to-remove styling. Zola still supplies content parsing, routing,
taxonomies, feeds, sitemap generation, and the production build.

**Alternatives considered**:

- Adopt a packaged Zola theme: faster visual bootstrap, but adds a larger
  customization surface and an external upgrade dependency.
- Keep MkDocs: optimized for documentation rather than the desired personal
  site and mixed publishing formats.

### Decision 2: Progressive enhancement and near-zero site JavaScript

**Choice**: Render all primary pages and navigation as semantic HTML/CSS,
without requiring site-wide JavaScript.

**Rationale**: This supports speed, accessibility, longevity, and a minimal
visual identity. Notebook exports may use their own scripts without imposing
that cost on the rest of the site.

### Decision 3: Flickr remains the photography destination

**Choice**: Link to Saurav's Flickr profile instead of building a local gallery
or integrating with the Flickr API.

**Rationale**: Flickr already provides photo hosting and gallery browsing. A
simple external link meets the current need while keeping the website focused
and avoiding photo metadata, synchronization, and display complexity.

### Decision 4: Technical exports as a dedicated library

**Choice**: Give notebook exports a dedicated Technical index and publish each
export as a static artifact rather than treating every notebook as a normal
blog post.

**Rationale**: Long-form articles and executable-notebook exports have
different reading and build characteristics. A distinct catalog makes the
difference clear while allowing cross-links in both directions.

### Decision 5: Migrate source content, not generated presentation

**Choice**: Convert the RST material to Markdown and reconstruct the two
technical pages from the best available source or clean content, rather than
copying generated MkDocs HTML and assets.

**Rationale**: Generated output is difficult to maintain and contains obsolete
theme code. Content-level migration produces a clean long-term source of truth.

### Decision 6: GitHub Actions deployment

**Choice**: Validate and build the Zola site in GitHub Actions, then publish the
generated output to GitHub Pages.

**Rationale**: The repository already targets the `sauravrt.github.io` user
site. CI gives reproducible builds and prevents broken content from being
published.

## Migration Strategy

1. Establish the Zola project, local design tokens, shared templates, and
   responsive navigation.
2. Implement About, Posts, and Technical section structures, including the
   Flickr profile link.
3. Convert and validate all legacy RST posts, preserving original publication
   dates and slugs.
4. Recover source material and missing local outputs for the two technical
   pages; rebuild them as posts, library entries, or exports according to their
   content.
5. Audit every external WordPress image/document URL, then either retain,
   replace, or archive it deliberately.
6. Add redirect aliases and verify internal links, media, math, code blocks,
   feed, sitemap, metadata, and 404 behavior.
7. Configure CI deployment and perform a pre-launch comparison against the
   content inventory.

Migration work should use a checklist with one row per legacy item so omissions
and unresolved assets are visible.

## Quality Attributes

- **Performance**: Small global CSS and no global framework JavaScript.
- **Accessibility**: Semantic landmarks, visible focus states, skip link,
  keyboard-operable controls, meaningful alt text, sufficient contrast, and
  respect for reduced-motion preferences.
- **Responsive design**: Readable from narrow phones through large displays
  without horizontal overflow.
- **Durability**: Markdown and straightforward templates remain the canonical
  source; external integrations are minimized.
- **Discoverability**: Descriptions, canonical URLs, social metadata, feed, and
  sitemap generated from source content.
- **Security**: No secrets in the public build; third-party scripts avoided on
  core pages; notebook exports reviewed before publication.

## Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Old WordPress images or documents disappear | Inventory and download/re-host important assets before launch; record replacements during migration |
| Generated technical pages reference missing local images or lost notebooks | Locate original repositories/notebooks; otherwise mark missing outputs explicitly rather than silently dropping them |
| RST-to-Markdown conversion changes equations, code, or links | Perform rendered side-by-side review and use Zola's built-in checks |
| Flickr profile URL changes | Keep the URL in one configuration location and verify it during launch review |
| Large notebook exports slow pages | Keep exports outside the global page bundle, show size/format where useful, and avoid iframe-loading them from index pages |
| Old inbound links break | Preserve slugs where possible and test an explicit redirect/alias map |
| Minimal design becomes visually sparse or hard to navigate | Use a constrained type scale, spacing system, clear section labels, and selected-content modules without adding decorative complexity |

## Success Criteria

- The production build contains a working home/About experience, post index,
  individual post pages, Flickr profile link, and Technical library.
- All 16 identified legacy content items are migrated or have a documented
  disposition.
- Old slugs selected for preservation resolve directly or redirect correctly.
- The site builds from a clean checkout through CI and deploys to GitHub Pages.
- Core pages remain fully usable without JavaScript and pass Zola's built-in
  checks plus manual review for accessibility basics and responsive layout.
- Adding a post or notebook export is documented and does not require modifying
  shared templates.

## Related Designs

The following detailed designs are planned but will be created only after this
high-level design is approved:

- [Site Foundation LLD](./designs/site-foundation/LLD.md)
- [Writing Migration LLD](./designs/writing-migration/LLD.md)
- [Technical Library LLD](./designs/technical-library/LLD.md)
- [Publishing and Deployment LLD](./designs/publishing-deployment/LLD.md)
