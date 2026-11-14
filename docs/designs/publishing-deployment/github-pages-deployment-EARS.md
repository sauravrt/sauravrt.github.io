# GitHub Pages Deployment - EARS

**Parent LLD**: [Publishing and Deployment LLD](./LLD.md)

## Deployment Trigger and Artifact

- [ ] **PUB-DEPLOY-001**: When a commit reaches `main`, GitHub Actions shall validate and build the production site.
- [ ] **PUB-DEPLOY-002**: Where a maintainer manually dispatches the deployment workflow, GitHub Actions shall validate and build the selected `main` revision.
- [ ] **PUB-DEPLOY-003**: If production validation succeeds, then the deployment workflow shall upload only the generated `public/` directory as the GitHub Pages artifact.
- [ ] **PUB-DEPLOY-004**: If production validation fails, then the deployment workflow shall not upload or deploy a new Pages artifact.
- [ ] **PUB-DEPLOY-005**: While a Pages deployment is active, the workflow shall prevent another deployment from running concurrently without canceling the active deployment.

## Permissions and Environment

- [ ] **PUB-DEPLOY-010**: The deployment workflow shall request only `contents: read`, `pages: write`, and `id-token: write` permissions.
- [ ] **PUB-DEPLOY-011**: The deployment workflow shall deploy through GitHub's `github-pages` environment.
- [ ] **PUB-DEPLOY-012**: The deployment workflow shall use GitHub's official Pages artifact and deployment actions.
- [ ] **PUB-DEPLOY-013**: The deployment workflow shall not require a personal access token, deploy key, Flickr credential, or notebook secret.

## Failure and Recovery

- [ ] **PUB-DEPLOY-020**: If a production build, artifact upload, or Pages deployment fails, then the workflow shall report a failed run without modifying generated output in the source branch.
- [ ] **PUB-DEPLOY-021**: The repository shall retain source history as the rollback mechanism and shall not commit generated production output to a deployment branch.
- [ ] **PUB-DEPLOY-022**: The repository documentation shall identify the GitHub Actions run as the location for deployment status and failure logs.

## Related Documents

- [Publishing and Deployment LLD](./LLD.md)
