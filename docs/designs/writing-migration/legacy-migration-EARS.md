# Legacy Migration - EARS

**Parent LLD**: [Writing Migration LLD](./LLD.md)

## Inventory

- [ ] **WRIT-MIGRATE-001**: The migration inventory shall track all 14 identified RST posts and both identified generated technical pages.
- [ ] **WRIT-MIGRATE-002**: Every legacy inventory item shall record its source, target route, migration status, and unresolved assets or links.
- [ ] **WRIT-MIGRATE-003**: Before launch, every legacy inventory item shall be marked migrated or shall have a documented disposition approved by the site owner.

## Content Preservation

- [ ] **WRIT-MIGRATE-010**: When an RST post is migrated, the system shall preserve its original title, publication date, authorial meaning, and legacy slug or alias.
- [ ] **WRIT-MIGRATE-011**: When legacy categories and tags are migrated, the system shall normalize them according to the taxonomy mapping in the Writing Migration LLD.
- [ ] **WRIT-MIGRATE-012**: When legacy WordPress math syntax is migrated, the system shall convert it to the site's selected math syntax.
- [ ] **WRIT-MIGRATE-013**: When malformed legacy link or media markup is migrated, the system shall replace it with valid semantic Markdown or HTML.
- [ ] **WRIT-MIGRATE-014**: If an automated conversion conflicts with manually reviewed content, then the manually reviewed content shall remain unchanged.

## Assets and Review

- [ ] **WRIT-MIGRATE-020**: When an owned legacy asset is available and required to understand a post, the migration shall preserve it locally with that post where practical.
- [ ] **WRIT-MIGRATE-021**: If a required legacy asset is unavailable, then the migration inventory shall record the missing asset and its chosen handling.
- [ ] **WRIT-MIGRATE-022**: When a third-party asset cannot be copied permissibly, the migrated post shall link to its authoritative source rather than store a local copy.
- [ ] **WRIT-MIGRATE-023**: Before a legacy post is marked migrated, it shall pass rendered comparison, internal-link, media, code, and math checks applicable to that post.
- [ ] **WRIT-MIGRATE-024**: If a generated technical page has no verified publication date, then its replacement shall remain a draft until the site owner approves a date policy.

## Related Documents

- [Writing Migration LLD](./LLD.md)
