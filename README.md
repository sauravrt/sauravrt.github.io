# Saurav writes

A minimal personal website built with **Zola 0.23.6**, local Tera templates, and
plain CSS. No Node build step, theme dependency, or custom test suite.

## Preview

Install [Zola](https://www.getzola.org/documentation/getting-started/installation/)
0.23.6, then run:

```sh
zola serve
```

Open the local URL printed by Zola. To include migration drafts:

```sh
zola serve --drafts
```

## Build and check

```sh
zola check --skip-external-links
zola build
```

These are the same commands used in CI. Output goes to ignored `public/`.

For an occasional historical external-link audit, run `zola check`. External
failures are warnings: inspect them manually, since old sites may be unavailable,
rate-limited, or reject automated requests.

Before publishing, open changed pages at phone and desktop widths, check
keyboard navigation, and verify images, equations, links, and downloads.

## Edit your profile

- `content/about.md`: biography.
- `content/_index.md`: home-page title and metadata; the homepage lists all posts.
- `config.toml`: title, description, author, GitHub, and Flickr URLs.

Flickr is a simple external profile link. No gallery, embed, or API is used.

## Add a post

Create `content/posts/my-post/index.md`:

```toml
+++
title = "My post"
date = 2026-11-13
description = "A short summary."
slug = "my-post"
draft = false
[taxonomies]
tags = ["python"]
+++

Write the post in Markdown here.
```

Store article-specific images beside `index.md` and reference them with
`![Meaningful alternative text](image.jpg)`. Use `draft = true` while writing.
Add `updated` only for a material content revision, not a mechanical migration.

For equations add `[extra]` with `math = true` in front matter and write
`\\(x^2\\)` inline or `\\[x^2\\]` on a separate line for display math. Double
backslashes preserve MathJax delimiters through Markdown. MathJax 3.2.2 loads
from jsDelivr only on pages opting into math; other pages have no JavaScript.

## Publish a notebook

1. Export from the notebook's own environment.
2. Copy the HTML entry point to `static/labs/my-notebook/index.html`, keeping
   related assets in that directory.
3. Add `content/technical/my-notebook.md`:

```toml
+++
title = "My notebook"
date = 2026-11-13
description = "What the reader will learn."
slug = "my-notebook"
draft = false
[extra]
format = "marimo"
artifact_url = "labs/my-notebook/"
source_url = "https://github.com/OWNER/REPO"
# size = "8 MB"
# related_post = "posts/my-post/"
+++

Optional prerequisites, provenance, and limitations.
```

Use `format = "jupyter"` for a Jupyter export. The Technical page is a title-only
list whose links open standalone exports directly, not in iframes. Artifact
directory links must preserve their trailing slash so relative assets resolve.
Do not place unfinished exports in `static/`: static files are copied even when
their catalog entry is a draft.

Typical export commands (run in the source environment, not this repository):

```sh
marimo export html notebook.py -o index.html
marimo export html-wasm notebook.py -o output_dir --mode run
jupyter nbconvert --to html notebook.ipynb --output index.html
```

`export html` creates a read-only snapshot; `export html-wasm` keeps controls
interactive by executing Python in the browser. WASM exports require internet
access to download the runtime and packages unless explicitly bundled offline.

Record the exporter version and source revision in publication documentation.
The TDOA publication uses marimo **0.25.2**; see
[`notebooks/README.md`](notebooks/README.md) for its pinned browser dependencies
and reproducible export command. Open exports from their final preview URLs,
check relative assets, and review them for credentials, private outputs,
filesystem paths, and unintended personal data before publication.

## Migration status

See [the migration checklist](docs/migration-checklist.md). Fourteen dated posts
are public. Two recovered technical pages remain drafts pending dates and
source/asset recovery. Fourteen illustrations/documents were recovered from
WordPress into their post bundles; JPEGs are resized to at most 1600 pixels.
They are article assets, not a new photo gallery.

## Deploy

The workflow in `.github/workflows/deploy.yml`:

- Builds/checks pull requests without deploying.
- Builds/checks `main`, then publishes `public/` through GitHub Pages.
- Supports manual deployment from `main`.

In GitHub **Settings → Pages**, select **GitHub Actions** as the publishing
source. No generated-output branch, deploy key, or personal access token is
needed. Deployment status and logs are in the repository's **Actions** tab.

The production URL is `https://sauravrt.github.io`. A failed build does not
deploy. To roll back published source, use a normal revert commit and let the
workflow rebuild.
