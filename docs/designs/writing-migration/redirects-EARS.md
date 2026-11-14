# Redirects - EARS

**Parent LLD**: [Writing Migration LLD](./LLD.md)

## Legacy Routes

- [ ] **WRIT-REDIRECT-001**: Where a migrated post previously used a root-level slug, the site shall publish an alias from `/<legacy-slug>/` to `/posts/<slug>/`.
- [ ] **WRIT-REDIRECT-002**: Where a legacy slug contains a known misspelling, the site shall preserve the misspelled route as an alias even if the canonical slug is corrected.
- [ ] **WRIT-REDIRECT-003**: Where a legacy generated technical route is replaced, the site shall redirect that route to its approved post or Technical entry.
- [ ] **WRIT-REDIRECT-004**: Every generated alias shall resolve to exactly one canonical public route.

## Validation

- [ ] **WRIT-REDIRECT-010**: Before launch, the migration redirect map shall be manually reviewed for duplicate routes and aliases.
- [ ] **WRIT-REDIRECT-011**: Before launch, every alias target shall be verified to exist in the production output.
- [ ] **WRIT-REDIRECT-012**: Before launch, every route in the migration redirect map shall be opened and verified.

## Related Documents

- [Writing Migration LLD](./LLD.md)
