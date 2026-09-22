# Dynamic VAD Survey Website Operations Guide

This document explains how to maintain the website, update its scholarly content, create immutable releases, validate changes, and deploy the resulting static site. It is an internal maintainer document and is intentionally not linked from the public navigation.

## 1. Core publishing model

The repository has two distinct content layers:

- **Latest working survey:** `content/`, `data/`, and `src/figures/` are editable. They generate the current pages under `/survey/`, `/explore/`, `/datasets/`, and `/benchmarks/`.
- **Frozen releases:** `versions/vX.Y/` contains a complete copy of a published release. It generates archival pages under `/versions/vX.Y/` and must never be edited after publication.

For example:

| Public URL | Source | Maintenance rule |
| --- | --- | --- |
| `/survey/` | `content/`, `data/references.json`, `src/figures/` | Always the latest reviewed working state |
| `/versions/v1.0/survey/` | `versions/v1.0/content/`, `versions/v1.0/data/`, `versions/v1.0/figures/` | Frozen and never edited |

Immediately after a release, the latest and frozen pages can look identical. They are nevertheless generated from different files. Later edits to the top-level source change `/survey/` without changing an earlier archive.

The survey selector therefore distinguishes **Latest survey (vX.Y)** from **vX.Y — Frozen archive**, even when both currently carry the same release number. If a section was introduced after an older release and has no archived counterpart, selecting that archive opens its full survey instead of a nonexistent section URL.

`dist/` is generated output. Do not maintain content by editing files inside it; the next build deletes and recreates the directory.

## 2. Repository map and website ownership

| Website area | Primary source files | Notes |
| --- | --- | --- |
| Home | `data/statistics.json`, `data/versions.json`, and copy in `scripts/build.mjs` | Counts, current version, release text, citation example |
| Survey | `content/**/*.md`, `data/references.json`, `src/figures/` | Full-document and section routes are generated together |
| Explore | `data/papers.json` | Search, filters, cards, table rows, and paper detail pages |
| Datasets | `data/datasets.json` | Dataset filters and metadata table |
| Benchmarks | `data/benchmarks.json` | Grouped protocol-aware benchmark tables |
| Updates | `data/versions.json`, `data/diffs/*.json` | Diff files are generated; do not hand-edit them |
| Version archive | `versions/vX.Y/` | Complete immutable release source |
| Maintenance | `content/maintenance.md` and page copy in `scripts/build.mjs` | Public methodology and responsibility description |
| About and citation | Citation and author copy in `scripts/build.mjs`, version/date in `data/statistics.json` | Update when archival paper metadata changes |
| Styling | `src/site.css` | Shared across current and archived pages |
| Browser interactions | `src/site.js` | Search, filters, dialogs, comparisons, dropdowns, copy buttons |
| Build behavior | `scripts/build.mjs` | Route generation and static asset copying |
| Validation | `scripts/validate-data.mjs`, `tests/site.test.mjs` | Schema checks and generated-page checks |
| Deployment | `.github/workflows/deploy.yml` | Builds and publishes `dist/` through GitHub Pages |

## 3. Survey content format

Survey prose is stored as Markdown in `content/`. The route list and display order are defined by the `sections` array in `scripts/build.mjs`.

Current section files:

```text
content/
├── introduction.md
├── problem-settings.md
├── datasets.md
├── evaluation.md
├── methods/
│   ├── semi-supervised.md
│   ├── weakly-supervised.md
│   ├── training-free.md
│   ├── instruction-tuned.md
│   └── open-world.md
├── maintenance.md
├── challenges.md
├── survey-scope.md
├── conclusion.md
└── reproducibility-appendix.md
```

Supported conventions include:

- `#`, `##`, and `###` headings. Heading text becomes the anchor ID.
- Paragraphs separated by blank lines.
- Markdown tables using pipe syntax.
- Inline math enclosed in single dollar signs.
- Display equations enclosed in double dollar signs on one line.
- Figures written as `![Caption](filename.png)`. The filename must exist in `src/figures/`.
- Numeric citations written as `[18]`. They link to reference `18` in the full survey.
- Bold text written as `**text**`.

The generator intentionally supports a controlled Markdown subset. Confirm generated output whenever introducing unfamiliar Markdown syntax.

When adding, removing, renaming, or reordering a section, update both the filesystem and the `sections` array in `scripts/build.mjs`. A filename alone does not create a route.

## 4. Structured data formats

All JSON files must contain valid JSON, use double quotes, and avoid trailing commas. Preserve existing field names because the build reads them directly.

### 4.1 Papers and methods: `data/papers.json`

Each paper record uses this shape:

```json
{
  "slug": "unique-url-slug",
  "method": "Method name",
  "title": "Full paper or display title",
  "authors": ["Author One", "Author Two"],
  "venue": "Venue",
  "year": 2026,
  "paradigm": "Training-Free",
  "modelTypes": ["MLLM"],
  "training": "Training description",
  "tasks": ["Detection", "Explanation"],
  "datasets": ["Dataset name"],
  "summary": "Concise, evidence-grounded summary.",
  "taxonomy": "Paradigm / Subfamily",
  "badges": ["Open vocabulary"],
  "code": true,
  "paperUrl": "https://example.org/paper",
  "codeUrl": "https://github.com/example/repository",
  "added": "v1.1",
  "updated": "v1.1",
  "verified": "Human verified on YYYY-MM-DD",
  "status": "Verified",
  "isLM": true
}
```

Rules:

- `slug` must be unique and should not change after publication.
- `paradigm` should use one of the five active taxonomy labels already present in the data.
- `codeUrl` is optional when no verified implementation exists.
- Do not invent a URL. Record an honest verification status when a link is unavailable.
- Update `added`, `updated`, and `verified` deliberately; these fields support release history and review.

### 4.2 Datasets: `data/datasets.json`

```json
{
  "slug": "unique-dataset-slug",
  "name": "Dataset name",
  "year": 2026,
  "group": "Detection-Oriented",
  "domain": "Domain description",
  "scale": "Human-readable scale",
  "categories": 10,
  "temporal": "Frame",
  "spatial": "Bounding box",
  "semantic": "Category label",
  "tasks": ["Detection", "Localization"],
  "access": "Verified dataset URL or access note",
  "verified": "Human verified on YYYY-MM-DD"
}
```

`slug` must be unique. Keep annotation terminology consistent so the table remains comparable and filterable.

### 4.3 Benchmarks: `data/benchmarks.json`

```json
{
  "group": "Training-free VAD",
  "dataset": "Dataset name",
  "method": "Method name",
  "metric": "AUC",
  "value": "95.4",
  "protocol": "Exact evaluation protocol",
  "source": "Paper, table, or verified URL",
  "reliability": "Author Reported",
  "comparable": true
}
```

Benchmark identity is derived from `group`, `method`, `dataset`, `metric`, and `protocol`. Changing one of these fields can appear as a removed row plus an added row during version comparison. Only set `comparable` to `true` when protocols genuinely match. Never imply a universal ranking across incompatible protocols.

### 4.4 References: `data/references.json`

```json
{
  "id": 18,
  "key": "ref18",
  "title": "Paper title",
  "authors": "Author list",
  "venue": "Publication metadata",
  "url": "https://doi.org/..."
}
```

Citation syntax such as `[18]` depends on the numeric `id`. Keep IDs unique and stable. Renumbering references requires updating every citation in `content/`.

### 4.5 Site statistics: `data/statistics.json`

This file controls homepage counts and the version/date displayed across the current website:

```json
{
  "papers": 161,
  "datasets": 28,
  "paradigms": 5,
  "version": "v1.0",
  "lastUpdated": "July 2026",
  "lastUpdatedFull": "July 9, 2026",
  "sampleNotice": "Data-quality notice"
}
```

Keep this metadata aligned with the maintained corpus and release notes. The homepage's visible collection totals are independently derived from the structured JSON files, so stale manual totals cannot silently change those displayed counts.

The homepage paper total comes from `statistics.json` because it represents the full reviewed survey corpus, while `papers.json` contains only the structured records currently available in the explorer. Dataset and paradigm totals are derived from the structured JSON during the build. The `lastUpdated` fields remain explicit editorial metadata and should be changed when the editable survey is materially updated. The BibTeX **access date** is different: browser JavaScript fills it with each visitor's local calendar date when the page opens and also updates the copied BibTeX text.

### 4.6 Version history: `data/versions.json`

Published entries require `version`, `date`, `title`, `status`, `tag`, `summary`, and `counts`. A planned entry may use `"date": "Planned"` and `null` for its tag.

Exactly one entry should have status `Current`, and it must be the first entry. Planned versions are displayed as roadmap placeholders but do not receive archive pages or dropdown options until their frozen directories exist.

The changing lifecycle status belongs here, not inside an immutable release archive. For example, when v1.1 is released, change v1.0 from `Current` to a historical status in this file and replace the existing planned v1.1 entry with the released v1.1 entry. Do not add a second v1.1 record.

## 5. Routine update workflow

1. Create or switch to an appropriate working branch.
2. Update the editable top-level source only: `content/`, `data/`, and `src/figures/`.
3. Update cross-references, statistics, version fields, and verification notes affected by the change.
4. Run `npm run check`.
5. Start `npm run dev` and inspect the relevant pages at `http://127.0.0.1:4173/`.
6. Confirm mobile-width behavior, navigation, citations, figures, filters, dialogs, and links relevant to the change.
7. Have scholarly changes reviewed by a human before publication.

Do not modify an existing `versions/vX.Y/` directory during routine maintenance.

## 6. Creating and freezing a release

Create the archive only after the top-level working state has passed human review.

The required release structure is:

```text
versions/vX.Y/
├── release.json
├── content/
├── data/
│   ├── papers.json
│   ├── datasets.json
│   ├── benchmarks.json
│   ├── references.json
│   └── statistics.json
└── figures/
```

Recommended procedure:

For a concrete v1.1 release:

1. Finish and human-review the editable top-level `content/`, `data/`, and `src/figures/` state.
2. Update `data/statistics.json` so `version`, release dates, and counts describe v1.1.
3. In `data/versions.json`, replace the existing planned v1.1 entry with the released v1.1 entry, place it first with status `Current`, and change v1.0 from `Current` to a historical status. Optionally add one new planned v1.2 placeholder.
4. Create `versions/v1.1/` and copy the complete reviewed `content/` tree into `versions/v1.1/content/`.
5. Copy `papers.json`, `datasets.json`, `benchmarks.json`, `references.json`, and the updated `statistics.json` into `versions/v1.1/data/`.
6. Copy the complete `src/figures/` tree into `versions/v1.1/figures/`.
7. Add `versions/v1.1/release.json` using immutable release metadata. Use the permanent status `Released`, not `Current`; the current version is tracked by `data/versions.json`.
8. Confirm that top-level `data/statistics.json`, the current entry in `data/versions.json`, and `versions/v1.1/data/statistics.json` all identify v1.1 and use the intended release date.
9. Run `npm run check`. The build creates the v1.1 archive routes and generates the v1.0-to-v1.1 comparison.
10. Compare `/survey/` with `/versions/v1.1/survey/`; at release time they should contain the same reviewed survey.
11. Confirm that `/versions/v1.0/` is unchanged, commit the new archive, and create the matching Git tag only after final approval.

Example immutable `release.json`:

```json
{
  "version": "v1.1",
  "date": "Month D, YYYY",
  "tag": "survey-v1.1",
  "status": "Released",
  "title": "Second public release",
  "summary": "Human-reviewed summary of this release."
}
```

After publication, treat the entire directory as immutable. If a published release contains an error, correct it in a new release and document the correction instead of silently changing the old archive.

## 7. How version comparison works

`scripts/generate-diffs.mjs` discovers version folders that contain `release.json`. For every chronological pair, it compares:

- papers by `slug`;
- datasets by `slug`;
- benchmarks by their derived composite identity;
- survey sections by relative Markdown filepath and complete file content.

It writes generated JSON into `data/diffs/`. The comparison page reads these files and reports added, removed, and modified records plus revised survey sections.

The comparison describes differences between stored release files. It does not infer scientific importance, judge method quality, or perform a semantic peer review. A planned entry in `data/versions.json` is not enough: comparisons activate only after both complete frozen directories, including their `release.json` files, exist. With only one frozen release, the website correctly reports that no comparison is available.

## 8. Validation checklist

Before publishing, verify all applicable items:

- [ ] `npm ci` completes from `package-lock.json` on a clean environment.
- [ ] `npm run check` passes.
- [ ] `dist/` is regenerated successfully.
- [ ] Homepage counts and current version are correct.
- [ ] Every survey section opens and the previous/next controls are correct.
- [ ] Full-survey citations reach the intended reference.
- [ ] Every referenced figure exists and renders with the correct caption.
- [ ] Method search and filters return expected results.
- [ ] Paper detail pages use verified metadata and links.
- [ ] Dataset rows and annotations are accurate.
- [ ] Benchmark values include their source and protocol.
- [ ] Version history matches the available frozen release directories.
- [ ] The version dropdown opens the same section when that section exists in the selected release; otherwise it opens that release's full archived survey.
- [ ] Earlier frozen releases remain unchanged.
- [ ] Version comparison summaries match the actual reviewed changes.
- [ ] `data/statistics.json`, the current `data/versions.json` entry, and the new frozen `statistics.json` agree on the released version.
- [ ] Planned versions do not have frozen directories and do not generate archive pages.
- [ ] The site works from both the root domain and the intended GitHub Pages path.

## 9. Local development and generated files

Install dependencies once:

```bash
npm ci
```

Build, validate, and test:

```bash
npm run check
```

Run the local static preview:

```bash
npm run dev
```

Open `http://127.0.0.1:4173/`. The local server is only a convenient way to view static files; it is not an application server and is not required after deployment.

The deployable output is `dist/`. It can be deleted and regenerated at any time from the maintained source files.

## 10. GitHub Pages deployment

The workflow in `.github/workflows/deploy.yml` runs when changes reach `main` or when manually dispatched. It:

1. checks out the repository;
2. installs dependencies with `npm ci`;
3. runs `npm run check`;
4. uploads `dist/` as the Pages artifact;
5. deploys that artifact to GitHub Pages.

In GitHub, set **Settings → Pages → Source** to **GitHub Actions**. The public website remains completely static and requires no database or server process.

## 11. Common mistakes

- Editing `dist/` instead of source files. Those changes disappear on rebuild.
- Editing a published `versions/vX.Y/` directory. This destroys archival integrity.
- Updating survey prose without updating citations or references.
- Adding a figure to Markdown without adding the file to `src/figures/`.
- Changing a JSON field name without updating the generator and validation.
- Using duplicate paper or dataset slugs.
- Publishing unverified paper, code, dataset, or benchmark URLs.
- Comparing benchmark values that use different protocols.
- Adding a published version to `data/versions.json` without creating its complete frozen directory.
- Creating a version directory without adding `release.json`; the comparison generator will not recognize it.
- Forgetting to update `data/statistics.json` and the release date.

## 12. Documentation URL

The build publishes a browser-readable, unlinked view at:

```text
http://127.0.0.1:4173/website-operations-guide/
https://dynamicvadsurvey.github.io/website-operations-guide/
```

The source file is also copied to `/WEBSITE_OPERATIONS_GUIDE.md`, although some browsers or static servers download `.md` files instead of displaying them. Because the HTML view is not linked from the website, visitors will normally encounter it only if they know the URL. It is public, not private: an unlinked URL can still be opened, shared, indexed, or discovered in the repository.
