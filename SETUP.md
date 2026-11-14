# Hybrid futuristic GitHub profile — setup

The package contains `README.md` and four **static, local SVG** files in `assets/`. It requires **no Actions workflows, analytics jobs, API tokens, or external image generators**. The diagrams are visual summaries; the real content remains readable/selectable Markdown.

## Install

1. Back up the current profile repository `m-arslan009/m-arslan009`.
2. Replace its root `README.md` with the one in this kit.
3. Copy the entire `assets/` folder, including `hero.svg`, `engineering-map.svg`, `campusgo-blueprint.svg` and `career-timeline.svg`.
4. Remove files from the OLD kit if present: `assets/dashboard.svg`, `assets/languages.svg`, `assets/activity.svg`, `scripts/generate_profile.py`, `.github/workflows/update-profile-dashboard.yml`. Also remove any outdated README embeds for those files. **Delete these from the GitHub repository**, not only from a download folder.
5. Commit to your profile repository's default branch, then preview at `https://github.com/m-arslan009`.

## Privacy and accuracy

Removing the old feed and generator prevents *this profile README* from publishing them, but doesn't change GitHub's own contribution chart, public repositories, or profile activity. Use GitHub repository visibility/settings for those separately.

This README includes the user's LinkedIn and email from the supplied résumé. Remove them if you prefer not to publish contact details. It describes projects and experience from that résumé, not live GitHub repository discovery. The CampusGo architecture diagram is conceptual, not a fully verified deployment map.

## Customizing the design

Edit text directly in `README.md`; edit titles, colors and shapes in the `assets/*.svg` files. All SVGs use fixed white/light fills so the look remains light even when GitHub is set to dark mode. Keep SVG text as secondary to actual README content for accessibility and search.
