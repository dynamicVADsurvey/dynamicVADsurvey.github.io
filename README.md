# Dynamic VAD Survey

First working static version of the companion website for **“Language Models in Video Anomaly Detection: A Sustainable Dynamic Survey.”** It combines a web-native reading experience, a structured literature explorer, dataset and benchmark views, version history, a unified diff, and a transparent maintenance page.

> This repository currently contains a clearly marked representative sample corpus. Aggregate counts mirror the website concept, while detailed paper, dataset, benchmark, author, citation, and link metadata must be replaced with the reviewed project corpus before scholarly release.

## Architecture

- `content/` — controlled survey prose in Markdown, one file per section.
- `data/` — structured JSON records and precomputed release diffs.
- `versions/v*/snapshot.json` — immutable, complete version inputs used for archival pages and comparisons.
- `src/` — shared accessible CSS and browser-side interactions.
- `scripts/build.mjs` — dependency-free static generator; emits clean routes to `dist/`.
- `scripts/validate-data.mjs` — checks required data fields and unique slugs.
- `tests/` — build-output checks.
- `.github/workflows/deploy.yml` — GitHub Pages deployment.

All public functionality is static. Search and filtering execute locally in the browser; every version snapshot gets a permanent `/versions/vX.Y/` page, and all chronological comparison pairs are precomputed during the build. No server or database is required.

## Local development

Node.js 18 or newer is required. There are no third-party runtime dependencies.

```bash
npm run dev
```

Open `http://127.0.0.1:4173/`. The development command rebuilds once and starts a local static server. After content or code changes, stop it, rerun the command, and refresh.

Build and validate separately:

```bash
npm run build
npm run check
```

The deployable site is written to `dist/`.

## GitHub Pages deployment

1. Push the repository to GitHub with `main` as the default branch.
2. In **Settings → Pages**, set **Source** to **GitHub Actions**.
3. Push to `main`, or run the “Deploy static site to GitHub Pages” workflow manually.

The workflow validates data, runs tests, builds the site, and deploys `dist/`. A `.nojekyll` file is included. Root-relative links are automatically rewritten in the browser when the site is hosted at a repository subpath, so both `https://dynamicvadsurvey.github.io/` and project Pages URLs are supported.

For the intended organization/user site, name the repository `dynamicvadsurvey.github.io` so the canonical URL is `https://dynamicvadsurvey.github.io/`.

## Replacing sample content

1. Replace section prose in `content/` with the reviewed manuscript text.
2. Replace representative entries in `data/*.json` and update `data/statistics.json`.
3. Add verified paper, code, project, repository, contact, archival PDF, and citation URLs.
4. Copy the current reviewed state into a new `versions/vX.Y/snapshot.json`. The build automatically regenerates every chronological pair under `data/diffs/` and publishes the new snapshot route.
5. Run `npm run check` and manually review generated pages before tagging a release.

The maintenance policy intentionally prevents automatic publication of uncertain metadata, taxonomy changes, benchmark superiority claims, removals, or major prose rewrites.
