# Publishing and Deployment - Low-Level Design

**Created**: 2026-11-13
**Status**: Approved
**HLD Link**: [High-Level Design](../../high-level-design.md)

## Overview

This design defines reproducible local builds, pull-request validation, and
deployment of the generated Zola site to the `sauravrt.github.io` GitHub Pages
user site.

## Environments

| Environment | Trigger | Output |
|---|---|---|
| Local preview | Author runs `zola serve` | Development server with reload |
| Local production check | Author runs `zola build`/`zola check` | `public/` |
| Pull request | GitHub Actions | Validation result; no deployment |
| Production | Push to `main` or manual dispatch | GitHub Pages deployment |

`public/` is generated and must not be committed.

## Version Pinning

One Zola version will be recorded in repository documentation and CI
configuration. Local development should use the same version. CI downloads the
specific release for Linux and verifies its published checksum before use.

GitHub Actions must be pinned at least to stable major versions; commit-SHA
pinning is preferred for third-party actions. The deployment path uses GitHub's
official Pages actions.

## Workflow Structure

One workflow builds pull requests and deploys successful production builds:

```text
.github/workflows/
└── deploy.yml
```

### `deploy.yml`

Triggers on pull requests, pushes to `main`, and manual dispatch. It:

1. Checks out the repository.
2. Installs the same pinned Zola release.
3. Builds with the production base URL.
4. Runs Zola's built-in checks.
5. For successful production-branch runs only, configures GitHub Pages, uploads
   `public/`, and deploys through the `github-pages` environment.

Pull-request runs build/check only and never deploy.

Deployment uses concurrency without canceling an active Pages deployment.

## Permissions

Validation requires read-only repository access. Deployment receives only:

```yaml
permissions:
  contents: read
  pages: write
  id-token: write
```

No deploy key, personal access token, Flickr credential, or notebook secret is
required.

## Build Contract

A production build must:

- Use `https://sauravrt.github.io` as `base_url`.
- Exclude drafts.
- Generate canonical URLs, feed, sitemap, 404 page, aliases, and static
  technical artifacts.
- Produce no broken internal links or missing local assets.
- Leave no absolute local filesystem paths in output.
- Complete from a clean checkout without files from the old-site directory.

The deployed artifact is the `public/` directory only.

## Lightweight Validation

Use `zola build` and `zola check` rather than custom validation scripts.
Zola's checks do not cover every exported HTML asset or editorial requirement.
Review those manually during publication:

- Open new pages and notebook exports and verify their links/assets.
- Preview core layouts at phone and desktop widths.
- Check keyboard navigation, focus visibility, and readable contrast.
- Review notebook exports for secrets and private outputs.
- Complete a one-time checklist covering the 16 legacy content items.

No test framework, browser automation, bespoke schema validator, automated
secret scanner, or accessibility CI gate is required. External-link failures
reported by Zola should be inspected rather than assuming every failure is a
permanent broken link.

## GitHub Pages Configuration

- Publishing source: GitHub Actions.
- Production branch: `main`.
- Site URL: `https://sauravrt.github.io`.
- Custom domain: none in the initial design.
- HTTPS: enforced by GitHub Pages.

No `gh-pages` branch or generated-output commit is required.

## Rollback and Failure Handling

| Condition | Behavior |
|---|---|
| Pull-request validation fails | Block merge through branch protection once enabled |
| Production build fails | Do not upload or deploy an artifact; current site remains active |
| Upload fails | Mark workflow failed; current site remains active |
| Deployment fails | Retain logs and rerun after correction; do not commit generated output |
| Bad content reaches production | Revert the responsible source commit through a normal commit/PR and redeploy |
| GitHub Pages outage | No application-side recovery; monitor GitHub status and wait/redeploy |

History is the rollback mechanism. Generated output is never manually edited.

## Repository Hygiene

`.gitignore` will exclude:

- `public/`
- Zola temporary/cache output, if any
- OS/editor artifacts
- Local notebook execution environments

The old generated MkDocs bundle will not be copied to this repository. Source
content and any deliberately preserved article assets are committed.

## Documentation

The repository README will document:

- Required Zola version and installation link.
- Local preview and production-check commands.
- How to add a post.
- How to add/update a Technical entry and export.
- Where profile links such as Flickr are configured.
- How deployment works and where failures are visible.

## Dependencies

- GitHub repository `sauravrt/sauravrt.github.io`.
- GitHub Actions and GitHub Pages.
- A pinned Zola release.
- Validation contracts from the Site Foundation, Writing Migration, and
  Technical Library designs.

## Requirements

- [Build Validation EARS](./build-validation-EARS.md)
- [GitHub Pages Deployment EARS](./github-pages-deployment-EARS.md)

## Related Documents

- [High-Level Design](../../high-level-design.md)
- [Site Foundation LLD](../site-foundation/LLD.md)
- [Writing Migration LLD](../writing-migration/LLD.md)
- [Technical Library LLD](../technical-library/LLD.md)
