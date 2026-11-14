# GitHub profile README kit

## Install
1. Back up your existing `README.md`.
2. Copy this kit's `README.md`, `.github/`, `scripts/`, and `assets/` into your profile repository: `m-arslan009/m-arslan009`.
3. Commit and push to the repository's default branch (usually `main`).
4. In GitHub, open **Settings → Actions → General → Workflow permissions** and allow **Read and write permissions**.
5. Open **Actions → Update profile dashboard → Run workflow**.
6. When it succeeds, the workflow commits three SVG cards into `assets/`.

## Token requirements
No personal access token is required. The workflow uses the repository-scoped `GITHUB_TOKEN` automatically provided by GitHub Actions. It only reads public profile/repository/event data and writes the generated SVGs back to this repository.

## Data definitions
- Dashboard: public repository count, followers, stars and forks.
- Language footprint: count of non-fork public repositories whose primary language GitHub reports. This is not a byte-weighted language breakdown.
- Recent activity: event types returned by GitHub's public Events API in the last 30 days. This is not a complete contribution count and may omit activity.

## Notes
- Scheduled refresh: daily at 02:17 UTC.
- Manual refresh: Actions → Update profile dashboard → Run workflow.
- If the workflow cannot push, check that workflow permissions are set to Read and write.
- If your default branch is not `main`, the workflow still runs on the branch where you add it; ensure you commit the files to your actual default branch.
