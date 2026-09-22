# Data Status

Snapshot of what has been populated into `data/` from the survey PDF
(*Language Models in Video Anomaly Detection: A Dynamic Survey*, Mumcu et al.),
and what still needs human verification before public release.

## Populated from the PDF

| File | Records | Source in PDF |
|------|---------|---------------|
| `data/datasets.json` | 28 datasets | Table 3 (all rows, in order) |
| `data/benchmarks.json` | 107 rows | Tables 4 (semi-supervised), 5 (weakly supervised), 6 (training-free/open-world) |
| `data/papers.json` | 62 methods | All benchmark-table methods + key methods from §V prose |
| `data/references.json` | 167 references | Full bibliography [1]–[167] |
| `data/statistics.json` | — | `datasets` set to 28; `papers` kept at 161 (target corpus) |

### Method coverage by paradigm (`papers.json`)
- Unsupervised & Semi-Supervised: 9 (incl. 2 non-LM baselines)
- Weakly Supervised: 27 (incl. 4 non-LM baselines)
- Training-Free: 14
- Instruction-Tuned: 7
- Open-World / Open-Vocabulary: 5

## Fixes applied (from the earlier consistency check)

1. **Citation title** — the BibTeX in `scripts/build.mjs` now reads
   "…: A Dynamic Survey" (was "A Sustainable Dynamic Survey"), matching the paper.
2. **Dataset count** — `statistics.json` now says 28 (was 26), matching Table 3.
3. **Holmes-VAD venue** — the current structured record uses `arXiv` rather than the earlier illustrative `CVPR` value.

## Still to verify before release

- **Benchmark numbers** — transcribed from the paper's tables; spot-check against the
  original method papers, especially cells that were blank vs. a real value.
- **Author lists** — each method record has a placeholder `authors` field pointing to its
  reference; fill in real author lists if you want them shown on method pages.
- **URLs** — `paperUrl` points to the in-page reference anchor and `code` is `false` for all
  methods. Add verified paper/code/project links; set `code: true` where a repo exists.
- **Dataset access** — `access` is set to "See original paper"; add real links if desired.
- **Reference details** — a few venues use short forms and long author lists were compacted
  with "et al."; expand/verify against the PDF as needed.
- **Version snapshots** — `versions/v1.0/` is the complete frozen release, with its own survey content, structured data, figures, and release metadata.
  Version v1.1 is a roadmap placeholder and will receive a snapshot only when that release
  has been human-reviewed. Comparisons activate when two published snapshots exist.

## Automated arXiv updates

`.github/workflows/update-survey.yml` runs weekly (Mondays, also triggerable via
"Run workflow"): `scripts/fetch-arxiv.mjs` queries the arXiv API for new papers
matching the survey's topic, `scripts/select-papers.mjs` sends the candidates to
Gemini (requires a `GEMINI_API_KEY` repo secret) to decide which are genuinely
in-scope and draft `data/papers.json` / `data/references.json` entries in the
existing schema. Nothing is auto-merged — the workflow opens a pull request
(labelled `automated`, `needs-verification`) that must pass `npm run check` and be
reviewed by a human before merging, matching the maintenance policy above. Every
auto-drafted paper entry is marked
`"status": "Proposed by automated arXiv update — needs human verification"`
until someone clears it.

## Regenerating

The three `build_*.py` helper scripts used to produce the JSON are kept at the repo root
(`build_data.py`, `build_refs.py`, `build_papers.py`) so you can edit the source lists and
re-emit the JSON. After any data change:

```bash
npm run check   # generate diffs, validate, build, run tests
npm run dev     # build once and serve at http://127.0.0.1:4173/
```
