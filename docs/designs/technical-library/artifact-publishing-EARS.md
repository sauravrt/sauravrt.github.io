# Artifact Publishing - EARS

**Parent LLD**: [Technical Library LLD](./LLD.md)

## Artifact Contract

- [ ] **TECH-ARTIFACT-001**: Every published notebook artifact shall have an entry point at `/labs/<slug>/`.
- [ ] **TECH-ARTIFACT-002**: Every published notebook artifact shall have exactly one corresponding published Technical entry.
- [ ] **TECH-ARTIFACT-003**: Every published Technical entry shall reference an existing notebook artifact.
- [ ] **TECH-ARTIFACT-004**: When a notebook artifact uses local assets, it shall reference those assets through paths that resolve beneath its artifact directory.
- [ ] **TECH-ARTIFACT-005**: When a notebook artifact uses an external dependency, it shall load that dependency over HTTPS.
- [ ] **TECH-ARTIFACT-006**: Each notebook artifact shall display a title or visible identifier without requiring its Technical entry page.

## Publication Safety

- [ ] **TECH-ARTIFACT-010**: Before a notebook artifact is published, it shall be reviewed for credentials, tokens, private URLs, local absolute paths, private outputs, and unintended personal data.
- [ ] **TECH-ARTIFACT-012**: Before publication, each notebook artifact and its catalog entry shall be manually checked for a matching counterpart.
- [ ] **TECH-ARTIFACT-013**: If a notebook artifact depends on internet access for material behavior, then its Technical entry shall disclose that dependency.
- [ ] **TECH-ARTIFACT-014**: Where an artifact is unusually large, its Technical entry shall display a human-readable size before the visitor opens it.

## Verification

- [ ] **TECH-ARTIFACT-020**: Before publication, each artifact shall be opened from its production-relative path in a clean browser session.
- [ ] **TECH-ARTIFACT-021**: Before publication, each artifact's local assets shall be verified in a browser at its production-relative path.
- [ ] **TECH-ARTIFACT-022**: The artifact publication documentation shall identify the exporter and version used for marimo and Jupyter exports.

## Related Documents

- [Technical Library LLD](./LLD.md)
