# Migration checklist

## Current status

- Zola 0.23.6 site and shared templates implemented.
- Flickr: <https://www.flickr.com/photos/sauravrt/>.
- Fourteen dated posts are included in production.
- Two undated technical pages are preserved as drafts, not silently discarded.
- The Technical page lists document titles linking directly to their artifacts.
  Its first publication is **TDOA HGDoP Exploration**, a marimo WASM notebook.
- GitHub Pages is configured for Actions publishing and the initial site has
  been deployed successfully.

## Content and redirect inventory

The 14 RST filenames correspond to the `extra.legacy_source` field in each post.
Each public root route below redirects to `/posts/<same-slug>/`.

| Legacy source / root route | Target | Status / notes |
|---|---|---|
| `optimum-array-paper-submitted-to-jasa.rst` | `/posts/optimum-array-paper-submitted-to-jasa/` | Converted; DOI retained |
| `uasp-2011.rst` | `/posts/uasp-2011/` | Converted |
| `nth-prime-number.rst` | `/posts/nth-prime-number/` | Converted; historical Python 2 indentation restored and disclosed |
| `rmtool-for-polynomial-method-the-bottleneck.rst` | `/posts/rmtool-for-polynomial-method-the-bottleneck/` | Converted; old resource links retained |
| `rsa-public-key-cryptography-algorithm-project-on-abstract-algebra.rst` | `/posts/rsa-public-key-cryptography-algorithm-project-on-abstract-algebra/` | Converted; WordPress math cleaned; educational-code notice added |
| `spectrgram-view-of-the-v-34-start-up-signalling.rst` | `/posts/spectrgram-view-of-the-v34-start-up-signalling/` | Converted; both spellings aliased; two figures recovered |
| `traceroute-to-nepal.rst` | `/posts/traceroute-to-nepal/` | Converted; image recovered; WordPress caption markup removed |
| `poster-session-at-ieeessp12.rst` | `/posts/poster-session-at-ieeessp12/` | Converted; poster PDF recovered |
| `memorial.rst` | `/posts/memorial/` | Converted; two photos recovered; doubled URL schemes corrected |
| `phase-of-product-of-complex-circular-gaussian-random-variables.rst` | `/posts/phase-of-product-of-complex-circular-gaussian-random-variables/` | Converted; nbviewer link updated |
| `unit-circle-mvdr-beamformer-for-icassp-2015.rst` | `/posts/unit-circle-mvdr-beamformer-for-icassp-2015/` | Converted; poster and preprint recovered |
| `resources-on-kalman-filters-for-tracking-applications.rst` | `/posts/resources-on-kalman-filters-for-tracking-applications/` | Converted; resource headings and notebook URL cleaned |
| `we-choose-to-go-to-the-moon.rst` | `/posts/we-choose-to-go-to-the-moon/` | Converted; malformed YouTube markup removed; original quotation retained |
| `provincetown-visit.rst` | `/posts/provincetown-visit/` | Converted; six photos recovered; historical prices retained |
| `Bayesian_Learning_Part1/index.html` | Draft `/posts/bayesian-learning-part-1/` | Original date unknown; equations need editorial review; old alias becomes public only when draft is published |
| `beamforming_fft/index.html` | Draft `/posts/beamforming-with-fft/` | Date/source notebook unknown; two output figures absent; old alias becomes public only when draft is published |

The 14 posts retain original naive publication timestamps; no original timezone
was available. Light copy/markup corrections were made without treating the
migration as a new publication date.

## Recovered article assets

All 14 owned WordPress image/document URLs referenced by the public posts were
downloaded successfully. JPEG copies were resized to a maximum dimension of
1600 pixels at quality 85; PNG diagrams and PDFs were retained unchanged.
The original WordPress source URLs can be recovered from the legacy source
files. No external-image dependency remains in the public article bodies.

## Verification

- [x] `zola build` succeeds with the 14 public posts and About page.
- [x] `zola check --skip-external-links` succeeds.
- [x] Initial `zola check` completes without reporting external-link failures.
- [x] Generated HTML inspected for Flickr links, canonical URLs, code blocks,
  math delimiters, and feed entries.
- [x] Draft-inclusive build succeeds; Zola warns that the two undated drafts
  cannot appear in date-sorted indexes, but their direct preview routes work.
- [ ] Visually review phone/desktop layouts and both color palettes in a browser.
- [ ] Verify keyboard focus, skip link, image appearance, and rendered equations.
- [ ] Review each migrated article against the legacy source before launch.
- [ ] Approve biography and any desired copy changes.
- [ ] Recover/approve dates and missing technical assets.
- [x] Enable GitHub Actions publishing in repository Settings → Pages.
- [x] Verify the first remote build and deployed URLs.
- [x] Preview TDOA WASM locally in Chromium: plots render, a slider recomputes
  the geometry, and no JavaScript errors are reported.

## Implementation decisions

- Zola 0.23.6 uses Tera 2 components instead of Tera 1 macros. Reusable entry
  lists are in `templates/components/entries.html`.
- Syntax highlighting uses Zola's built-in light/dark highlighter.
- Math uses page-opt-in MathJax 3.2.2 from jsDelivr.
- CI runs only Zola's built-in checks/build; no custom tests were added.
- Redirects use Zola's stock aliases, including its no-JavaScript refresh
  fallback. No custom redirect framework was introduced.
- EARS checkboxes remain acceptance-review work items; they are not promises
  of one automated test per statement.
- Notebook artifact links explicitly preserve the trailing slash required for
  relative assets when served by Zola locally.
