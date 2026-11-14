# Technical Library - Low-Level Design

**Created**: 2026-11-13
**Status**: Approved
**HLD Link**: [High-Level Design](../../high-level-design.md)

## Overview

The Technical library catalogs static marimo and Jupyter notebook exports
without forcing them into the blog-post format. Each entry has a lightweight
Zola page for description and provenance, plus an independently addressable
HTML artifact.

## Structure

```text
content/technical/
├── _index.md
└── <slug>.md

static/labs/
└── <slug>/
    ├── index.html
    └── export-specific assets
```

The catalog page is `/technical/`, entry pages are
`/technical/<slug>/`, and standalone exports are `/labs/<slug>/`.

The separation prevents export HTML, CSS, or JavaScript from affecting the main
site shell and allows readers to understand an artifact before loading it.

## Technical Entry Model

| Field | Type | Required | Description |
|---|---|---:|---|
| `title` | String | Yes | Catalog and entry title |
| `date` | Date/time | Yes | Initial publication date |
| `updated` | Date/time | No | Latest material update |
| `description` | String | Yes | Concise purpose and audience |
| `slug` | String | Yes | Stable catalog/artifact identifier |
| `draft` | Boolean | Yes | Publication state |
| `extra.format` | Enum | Yes | `marimo` or `jupyter` |
| `extra.artifact_url` | String | Yes | Site-relative `/labs/<slug>/` URL |
| `extra.source_url` | String | No | Source notebook/repository |
| `extra.related_post` | String | No | Related post URL |
| `extra.exported_at` | Date/time | No | Export generation time |
| `extra.size` | String | No | Human-readable warning for large artifacts |

The entry body may include prerequisites, a short abstract, environment notes,
and limitations. It must not duplicate the full notebook narrative.

## Catalog Behavior

The Technical index lists entries by publication/update date and displays:

- Title.
- Description.
- Format label.
- Publication or update date.
- Link to the descriptive entry page.

The entry page provides a prominent “Open notebook” link and optional “View
source” and related-post links. Exports are never loaded in iframes on catalog
or entry pages.

## Export Contract

An export is publishable when:

1. It opens from its final `/labs/<slug>/` path after a production build.
2. All required local assets use relative paths beneath the artifact directory.
3. Any CDN dependencies use HTTPS and are documented.
4. It contains no secrets, access tokens, private file paths, private outputs,
   or unintended personal data.
5. Its title and visible content identify the artifact without relying on the
   catalog page.
6. The corresponding catalog entry exists and points to it.

Fully self-contained HTML is allowed, but large file size must be considered.
Directory exports are preferred when separating assets materially improves
caching or maintainability.

## Authoring Workflow

### Marimo

1. Keep the `.py` notebook in its authoritative project repository.
2. Run the selected marimo static export command in that environment.
3. Copy the reviewed export to `static/labs/<slug>/`.
4. Preview through Zola so path assumptions match production.
5. Create or update the Technical entry metadata.

### Jupyter

1. Keep the `.ipynb` notebook in its authoritative project repository.
2. Clear unintended or sensitive outputs.
3. Export with a pinned `nbconvert` environment or another documented static
   exporter.
4. Copy HTML and required assets to `static/labs/<slug>/`.
5. Preview and create/update the matching Technical entry.

The website repository stores publication artifacts, not the only copy of
notebook source.

## Legacy Technical Material

| Legacy item | Proposed handling |
|---|---|
| `Bayesian_Learning_Part1` | Locate the original notebook/source, reconstruct a clean export, and add a Technical entry; optionally retain a related post if the prose stands alone |
| `beamforming_fft` | Locate the original notebook and missing generated images, produce a clean export, and redirect the old route to its Technical entry or companion post |
| Complex-circular Gaussian post | Keep as a post and link to the authoritative notebook or a new Technical entry if republished locally |

Generated MkDocs page chrome must not be copied into the new export.

## Security and Privacy Review

Before publication, inspect both source text and rendered output for:

- Credentials, tokens, internal hostnames, and private URLs.
- Local absolute paths and usernames.
- Embedded datasets or outputs that should not be public.
- Active third-party scripts.
- Forms, network calls, or browser storage not required by the material.

Notebook code is treated as public source once included in the export. Static
hosting does not make active notebook execution available.

## Error Handling and Edge Cases

| Condition | Handling |
|---|---|
| Catalog entry has no artifact | Keep it as draft until manual review confirms the artifact exists |
| Artifact has no catalog entry | Add its entry or omit the artifact before publication |
| Export depends on missing relative asset | Fix the asset during browser review before publication |
| Export is unusually large | Show size on entry page and optimize/split where practical |
| Export requires internet access | Disclose the dependency; core explanatory content should remain understandable |
| Interactive feature cannot survive static export | Explain the limitation or link to an appropriate external runtime |
| Slug changes | Add an alias for the catalog page and a static redirect for the old artifact route if already public |

## Validation

- Manually match every published Technical entry to one artifact directory.
- Check every artifact entry point and local asset.
- Open exports in a clean browser session at production-like paths.
- Test at narrow and wide widths; horizontal scrolling is acceptable only
  within technical elements that genuinely require it.
- Review the browser console for missing assets and unexpected network errors.
- Record the exporter and version in authoring documentation or adjacent
  provenance metadata.

## Dependencies

- Site Foundation templates and metadata.
- Export tools maintained in each notebook's source environment.
- Static hosting through the Publishing and Deployment design.
- Original source repositories for legacy technical pages.

## Requirements

- [Technical Catalog EARS](./catalog-EARS.md)
- [Artifact Publishing EARS](./artifact-publishing-EARS.md)

## Related Documents

- [High-Level Design](../../high-level-design.md)
- [Site Foundation LLD](../site-foundation/LLD.md)
- [Writing Migration LLD](../writing-migration/LLD.md)
- [Publishing and Deployment LLD](../publishing-deployment/LLD.md)
