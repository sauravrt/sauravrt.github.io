# Post Publishing - EARS

**Parent LLD**: [Writing Migration LLD](./LLD.md)

## Post Metadata

- [ ] **WRIT-POST-001**: Every published post shall define a title, publication date, description, slug, and explicit draft state.
- [ ] **WRIT-POST-002**: Where a post has been materially revised, the post shall define and display its updated date.
- [ ] **WRIT-POST-003**: Where a post has tags, the site shall render normalized tags from the configured `tags` taxonomy.
- [ ] **WRIT-POST-004**: Before publication, each post shall undergo a manual required-metadata review.

## Post Routes and Views

- [ ] **WRIT-POST-010**: The site shall publish each non-draft post at `/posts/<slug>/`.
- [ ] **WRIT-POST-011**: The Posts index shall list all non-draft posts in descending publication-date order.
- [ ] **WRIT-POST-012**: Each Posts-index item shall display the post title, publication date, and description.
- [ ] **WRIT-POST-013**: Each post page shall display its title, publication date, body, and link to the Posts index.
- [ ] **WRIT-POST-014**: While the post count is within the initial migrated corpus, the Posts index shall display the complete list without pagination.
- [D] **WRIT-POST-015**: The Posts index shall paginate the post list.

## Article Content

- [ ] **WRIT-POST-020**: When a post contains a fenced code block with a known language, the site shall render language-appropriate syntax highlighting.
- [ ] **WRIT-POST-021**: When a post contains supported mathematical notation, the site shall render the notation without exposing legacy WordPress `$latex` markup.
- [ ] **WRIT-POST-022**: Before publication, each post shall undergo rendered review for missing local assets.

## Related Documents

- [Writing Migration LLD](./LLD.md)
