# Writing Migration - Low-Level Design

**Created**: 2026-11-13
**Status**: Approved
**HLD Link**: [High-Level Design](../../high-level-design.md)

## Overview

This design defines the post model, list/detail rendering, and controlled
migration of all legacy writing. The migrated Markdown becomes the canonical
source; generated MkDocs HTML and theme assets are not copied.

## Content Structure

```text
content/posts/
├── _index.md
└── <slug>/
    ├── index.md
    └── local assets, when required
```

Page bundles are preferred because they keep any recovered diagrams, downloads,
or post-specific images beside their article. A post without local assets still
uses the same layout for consistency.

## Post Model

| Field | Type | Required | Description |
|---|---|---:|---|
| `title` | String | Yes | Display and metadata title |
| `date` | Date/time | Yes | Original publication date |
| `updated` | Date/time | No | Material revision date |
| `description` | String | Yes | Index excerpt and metadata description |
| `slug` | String | Yes | Stable route segment |
| `aliases` | String list | For changed routes | Legacy routes that redirect |
| `draft` | Boolean | Yes | Explicit publication state |
| `taxonomies.tags` | String list | No | Normalized topic labels |
| `extra.legacy_source` | String | During migration | Source filename/reference |
| `extra.related_technical` | String | No | Related Technical entry URL |

Author is site-wide and need not be repeated in every post.

## Routing and Listing

- Canonical article route: `/posts/<slug>/`.
- Posts index: `/posts/`, sorted by publication date descending.
- Legacy root route: `/<slug>/`, generated as an alias when it was previously
  public or is likely to have inbound links.
- The post index shows title, publication date, description, and optional tags.
- Individual posts show title, date, optional updated date, body, and a link
  back to the Posts index.

Pagination is deferred until the post count makes it useful. The initial
16-item corpus can render on one index page.

## Taxonomy Normalization

One `tags` taxonomy replaces the inconsistent legacy distinction between
categories and tags. Values will be lowercase slugs with human-readable display
names. Proposed normalization includes:

| Legacy value | Proposed tag |
|---|---|
| `Research`, `PhD Research` | `research` |
| `signalprocessing`, `Signal Processing` | `signal-processing` |
| `Math` | `mathematics` |
| `Python`, `Programming` | Retain as separate `python` and `programming` tags when both are meaningful |
| `Travel` | `travel` |
| `Misc`, `Uncategorized` | Omit unless a specific useful tag can be inferred |

Tags are navigation aids, not an obligation. A post may have no tags.

## Migration Inventory

| Legacy source | Date | Target slug | Notes |
|---|---|---|---|
| `optimum-array-paper-submitted-to-jasa.rst` | 2011-09-03 | `optimum-array-paper-submitted-to-jasa` | External paper link |
| `uasp-2011.rst` | 2011-10-14 | `uasp-2011` | Conference links |
| `nth-prime-number.rst` | 2011-10-14 | `nth-prime-number` | Code formatting review |
| `rmtool-for-polynomial-method-the-bottleneck.rst` | 2011-11-09 | `rmtool-for-polynomial-method-the-bottleneck` | Technical links |
| `rsa-public-key-cryptography-algorithm-project-on-abstract-algebra.rst` | 2011-12-26 | Existing slug | Math conversion and GitHub link |
| `spectrgram-view-of-the-v-34-start-up-signalling.rst` | 2012-03-29 | Existing legacy slug | Preserve misspelled legacy alias; recover spectrogram |
| `traceroute-to-nepal.rst` | 2012-05-03 | `traceroute-to-nepal` | Recover external image |
| `poster-session-at-ieeessp12.rst` | 2012-09-17 | `poster-session-at-ieeessp12` | Recover or validate poster PDF |
| `memorial.rst` | 2014-06-01 | `memorial` | Recover external travel images |
| `phase-of-product-of-complex-circular-gaussian-random-variables.rst` | 2015-03-14 | Existing slug | Validate notebook/source link |
| `unit-circle-mvdr-beamformer-for-icassp-2015.rst` | 2015-03-14 | Existing slug | Recover or validate paper/poster PDFs |
| `resources-on-kalman-filters-for-tracking-applications.rst` | 2016-08-14 | Existing slug | External resource audit |
| `we-choose-to-go-to-the-moon.rst` | 2016-08-23 | `we-choose-to-go-to-the-moon` | Convert malformed YouTube markup to a link |
| `provincetown-visit.rst` | 2017-06-03 | `provincetown-visit` | Recover external travel images |
| `Bayesian_Learning_Part1/index.html` | Unknown | `bayesian-learning-part-1` | Recover source/date; classify as post or Technical companion |
| `beamforming_fft/index.html` | Unknown | `beamforming-with-fft` | Recover missing output images/source; likely Technical companion |

“Existing slug” means the complete slug from the legacy front matter will be
retained without abbreviation.

## Conversion Pipeline

1. Record the source item in a migration checklist.
2. Use Pandoc or a small conversion script only as a first-pass aid.
3. Manually normalize front matter, headings, links, code, equations, and image
   references.
4. Replace WordPress-specific `$latex ...$` syntax with Zola-compatible math
   delimiters.
5. Recover important remote assets into the page bundle when licensing and
   source availability permit; otherwise retain a validated HTTPS link or
   document the omission.
6. Add the canonical route and legacy aliases.
7. Compare rendered source and destination side by side.
8. Mark the checklist item complete only after build, link, and visual review.

Automated conversion must never overwrite a manually reviewed destination file.

## Legacy Asset Policy

Legacy post illustrations are distinct from the discarded photography-gallery
feature. Images and PDFs necessary to understand an article should be preserved
with that article where practical.

| Asset state | Action |
|---|---|
| Available and owned | Store locally in the post bundle, optimized without discarding the source-quality meaning |
| Available only remotely | Download/re-host when permitted; otherwise keep a validated HTTPS URL |
| Missing but recoverable from a source repository | Restore from the authoritative repository |
| Missing and unrecoverable | Add a visible editorial note only when its absence materially affects the article |
| Third-party copyrighted asset | Link to the source rather than copying unless reuse is permitted |

## Markup Rules

- Preserve the original authorial meaning and publication date.
- Correct conversion artifacts and obvious broken markup.
- Record substantive editorial rewrites with an `updated` date.
- Use fenced code blocks with a language when known.
- Use semantic Markdown headings beginning below the template-rendered title.
- Give every local informative image meaningful alt text.
- Use descriptive link text instead of raw “here” links when a mechanical
  rewrite does not alter meaning.
- Render equations with page-opt-in MathJax 3.2.2; do not mix several libraries.

## Error Handling and Edge Cases

| Condition | Handling |
|---|---|
| Unknown date for generated technical page | Keep unpublished until date is recovered or an explicit migration date policy is approved |
| Duplicate dates | Use stable secondary ordering by title or slug |
| Broken external link | Find an authoritative replacement or archived target; record unresolved links |
| Alias collides with another output path | Fail validation and resolve explicitly |
| Unsupported RST directive | Convert manually; do not expose raw directive text |
| Missing image | Do not render a broken image element |
| Very long title/slug | Preserve the slug for compatibility; allow wrapping in templates |

## Validation

Each migrated item must pass:

- Manual required-front-matter review.
- Zola build/check.
- Internal link and alias verification.
- Manual review of external links and any failures reported by Zola.
- Visual review at phone and desktop widths.
- Math, code, media, and download review where applicable.
- Comparison against the migration inventory to ensure all 16 items have a
  documented disposition.

## Dependencies

- Site Foundation templates and metadata behavior.
- Legacy source at `/Users/saurav/Documents/sauravrt.github.io-main`.
- Original notebooks/repositories or archives for missing technical assets.
- An agreed math rendering approach.

## Requirements

- [Post Publishing EARS](./post-publishing-EARS.md)
- [Legacy Migration EARS](./legacy-migration-EARS.md)
- [Redirects EARS](./redirects-EARS.md)

## Related Documents

- [High-Level Design](../../high-level-design.md)
- [Site Foundation LLD](../site-foundation/LLD.md)
- [Technical Library LLD](../technical-library/LLD.md)
- [Publishing and Deployment LLD](../publishing-deployment/LLD.md)
