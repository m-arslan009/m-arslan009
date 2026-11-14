# Light-mode GitHub profile README — installation

## What this version does

This package is a **static public portfolio**. It does not call GitHub's API, collect events, display GitHub statistics, fetch repository lists, or run a scheduled workflow. All local SVG assets are static.

The README shows intentionally written **project summaries**, not public repository names, repository links, live counts, activity history, or analytics. It contains a LinkedIn link and an email address drawn from the supplied résumé; remove either if you do not wish to publish it.

## Install

1. Open the **profile repository** named `m-arslan009/m-arslan009` on GitHub (the repository name must match the username).
2. Back up your existing `README.md`.
3. Replace the root `README.md` with this package's version.
4. Upload the complete `assets/` directory alongside `README.md`, preserving names and capitalization.
5. **Remove legacy files** from the profile repository if present:
   - `assets/dashboard.svg`
   - `assets/languages.svg`
   - `assets/activity.svg`
   - `scripts/generate_profile.py`
   - `.github/workflows/update-profile-dashboard.yml`
6. Commit and push your changes to the default branch. Inspect the public profile page while signed out.

**Note:** If the old generator/workflow is not removed, it may continue to update or recreate analytic SVG files even when they are no longer referenced by the README. Delete the files from the *remote repository*, not just from your local copy. You can delete the empty `scripts/` or `.github/workflows/` directories too, if they contain no other files.

## Privacy boundaries

- This only controls what the **README** chooses to show. GitHub controls the built-in contribution graph, profile activity, repository visibility, and public profile metadata.
- To hide repositories themselves, change their visibility in GitHub settings where applicable. Making a repository private can affect access, forks, Pages, and collaborators.
- To adjust contribution-related settings, review your GitHub profile settings. The README cannot switch off GitHub's built-in contribution graph.
- The LinkedIn/email badges load icons from `shields.io`. The two portfolio illustrations are local, static SVG files and do not make network requests.
- No GitHub Actions permissions or personal access tokens are required.

## Customization

Edit the text in `README.md` and the static SVGs in `assets/` as desired. The layout is white/light by design, and visuals do not rely on OS-level dark-mode adaptation.
