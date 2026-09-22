# Dynamic VAD Survey

Static companion website for **“Language Models in Video Anomaly Detection: A Dynamic Survey.”** It provides a web-native survey, searchable method records, dataset and benchmark views, version history, frozen releases, citation guidance, and a transparent maintenance policy.

The current public release is **v1.0**. Version **v1.1** is listed only as a planned release and does not yet have an archive or comparison data.

## How the site works

The site is generated entirely from files in this repository. It requires no application server or database after deployment. Browser-side JavaScript provides search, filtering, version selection, dynamic citation access dates, and other interactions over the generated static pages.

- `/survey/` always represents the latest maintained survey in `content/`.
- `/versions/v1.0/survey/` is the immutable archive generated from `versions/v1.0/`.
- `/updates/compare/` becomes useful after at least two complete frozen releases exist.
- `dist/` is disposable generated output and must not be edited manually.

Although the latest survey and the v1.0 archive currently contain the same release, they come from separate source locations. Future edits belong in the top-level maintained files; a published archive must remain unchanged.

## Repository structure

| Path | Purpose |
| --- | --- |
| `content/` | Latest survey prose in Markdown, including method-family sections |
| `data/` | Current methods, datasets, benchmarks, references, statistics, and version metadata |
| `src/` | Shared CSS, browser-side JavaScript, and survey figures |
| `versions/vX.Y/` | Complete immutable source archive for each published release |
| `scripts/build.mjs` | Generates the full static website in `dist/` |
| `scripts/generate-diffs.mjs` | Generates comparisons between complete frozen releases |
| `scripts/validate-data.mjs` | Validates structured records and release consistency |
| `scripts/serve.mjs` | Serves the generated files locally for previewing |
| `tests/` | Automated checks against generated output |
| `.github/workflows/deploy.yml` | Builds, checks, and deploys the site with GitHub Pages |
| `WEBSITE_OPERATIONS_GUIDE.md` | Detailed content, release, versioning, and deployment procedures |

The operations guide is also rendered during the build at `/website-operations-guide/`. It is intentionally absent from the public navigation but can be opened directly by maintainers.

## Current data coverage

The current top-level data includes:

- **182** papers/references in the reviewed corpus and homepage statistic;
- **62** detailed method records in `data/papers.json`;
- **28** datasets in `data/datasets.json`;
- **107** benchmark rows in `data/benchmarks.json`;
- **5** supported method paradigms;
- **1** complete frozen release: v1.0.

The structured values were transcribed from the survey and should be verified against original sources before they are treated as final scholarly metadata. See `DATA_STATUS.md` for the remaining verification work.

## Local development

Node.js 18 or newer is required. Install the locked dependencies once:

```bash
npm ci
```

Build the site and start the local static preview server:

```bash
npm run dev
```

Open <http://127.0.0.1:4173/>. The localhost process is only a convenient static-file server; it is not part of the deployed website. The development command builds once when it starts, so rerun it after source changes if another process has not already rebuilt `dist/`.

Useful commands:

```bash
npm run build   # regenerate dist/
npm run test    # test the existing generated output
npm run check   # generate diffs, validate data, build, and test
```

Use `npm run check` before publishing or committing a release-related change.

## Generated output

`npm run build` creates `dist/`, including all HTML routes, shared assets, JSON exposed to the browser, archived release pages, the rendered website operations guide, sitemap, robots file, and `.nojekyll`.

`dist/` is excluded by `.gitignore` because GitHub Actions regenerates it during deployment. Do not maintain or commit changes directly inside `dist/`; they will be deleted by the next build.

## GitHub Pages deployment

1. Push the repository to GitHub with `main` as the default branch.
2. In **Settings → Pages**, set **Source** to **GitHub Actions**.
3. Push to `main`, or manually run **Deploy static site to GitHub Pages** from the Actions tab.

The deployment workflow runs `npm ci` and `npm run check`, uploads `dist/` as the Pages artifact, and deploys that artifact. The repository does not need to store generated files or run a persistent server.

For the organization site, the repository name should remain `dynamicvadsurvey.github.io`, producing the canonical URL <https://dynamicvadsurvey.github.io/>. The build also rewrites root-relative links at runtime when hosted under a GitHub Pages project subpath.

## Updating current content

- Edit survey prose in `content/`.
- Edit current structured records in `data/*.json`.
- Edit shared presentation and interactions in `src/site.css` and `src/site.js`.
- Edit page generation, global layout, or shared metadata in `scripts/build.mjs`.
- Add or replace survey figures in `src/figures/`.
- Update `data/statistics.json` and `data/versions.json` when release metadata changes.

Then run:

```bash
npm run check
```

For exact schemas, route ownership, validation rules, and a file-by-file maintenance map, consult `WEBSITE_OPERATIONS_GUIDE.md`.

## Publishing a new version

Do not create a release by copying only one JSON snapshot. Each published version needs a complete immutable archive:

```text
versions/vX.Y/
├── content/
├── data/
├── figures/
└── release.json
```

At a high level:

1. Finish and review the latest top-level `content/`, `data/`, and figures.
2. Update the current version and dates in `data/statistics.json`.
3. Replace the matching planned entry in `data/versions.json` with its released metadata; do not add a duplicate version entry.
4. Copy the complete reviewed sources into a new `versions/vX.Y/` directory.
5. Add immutable `release.json` metadata to that archive.
6. Run `npm run check` to generate archive routes and chronological comparisons.
7. Manually compare `/survey/` with `/versions/vX.Y/survey/` before publishing.
8. Never edit the frozen archive after release; corrections belong in a subsequent version.

The full release checklist and required metadata examples are in `WEBSITE_OPERATIONS_GUIDE.md`.

## Publication policy

Agentic tools may assist with discovery, extraction, routing, summaries, and localized drafts. Taxonomy changes, evaluative claims, removals, benchmark interpretations, and public releases require human review and approval. Automation should prepare reviewable repository changes; it must not publish a scholarly release autonomously.
