# Build Validation - EARS

**Parent LLD**: [Publishing and Deployment LLD](./LLD.md)

## Reproducible Build

- [ ] **PUB-VALIDATE-001**: The repository shall pin one Zola version for local and continuous-integration builds.
- [ ] **PUB-VALIDATE-002**: When a production build runs from a clean checkout, the system shall generate the complete site without reading files outside the repository.
- [ ] **PUB-VALIDATE-003**: The production build shall use `https://sauravrt.github.io` as the base URL.
- [ ] **PUB-VALIDATE-004**: The production build shall exclude draft content.
- [ ] **PUB-VALIDATE-005**: The production build shall generate the home page, About page, Posts section, Technical section, feed, sitemap, 404 page, aliases, and static notebook artifacts.
- [ ] **PUB-VALIDATE-006**: The repository shall exclude the generated `public/` directory from version control.

## Continuous Validation

- [ ] **PUB-VALIDATE-010**: When a pull request changes the repository, GitHub Actions shall run Zola's built-in build/check commands without deploying.
- [ ] **PUB-VALIDATE-011**: If Zola's built-in checks fail, then the workflow shall report the failure.
- [ ] **PUB-VALIDATE-012**: Before publication, new content shall undergo manual review of metadata, links, and assets.
- [ ] **PUB-VALIDATE-015**: When Zola reports an external-link failure, the publication review shall inspect whether the failure is permanent or transient.

## Local Workflow

- [ ] **PUB-VALIDATE-020**: The repository documentation shall provide commands for local preview and production validation.
- [ ] **PUB-VALIDATE-021**: The documented local validation commands shall use the same Zola build/check modes as continuous integration.

## Related Documents

- [Publishing and Deployment LLD](./LLD.md)
