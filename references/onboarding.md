# PDF-folder-first onboarding

Use this reference when a user wants to build a new journal or field writing guide from a folder of PDFs they have already prepared.

## Scope boundary

This onboarding begins only after PDFs exist locally. Scraping, publisher crawling, authentication, browser downloading, article discovery, and obtaining paywalled files are outside this skill. Never insert an acquisition stage before Gate 0.

If the folder is missing, inaccessible, or contains no usable PDFs:

1. report the blocking condition;
2. ask the user to prepare or correct the PDF folder;
3. stop without proposing scraper code, publisher-specific download instructions, or an acquisition workflow.

Existing `.bib`, `.ris`, `.csv`, and manifest files may be consumed as local metadata, but this skill does not fetch them.

## Minimum intake

The only required initial value is a folder that already contains PDFs:

```text
pdf_folder: /absolute/path/to/folder
```

If absent, ask for it and stop. If present but has no usable PDFs, explain the prerequisite and stop. If usable PDFs are present, do not begin with a questionnaire. Inspect first, then ask only questions whose answers materially change inclusion, splitting, or outputs.

## Gate 0 — read-only folder preflight

Inspect without renaming, moving, deleting, or editing source files. Report:

- accessible absolute folder path;
- recursive PDF count and total size;
- top-level and nested folder pattern;
- basename collisions and byte-identical duplicates;
- unreadable, encrypted, empty, or non-PDF files with a `.pdf` extension;
- nearby metadata exports (`.bib`, `.ris`, `.enw`, `.csv`, `.tsv`, publisher manifests);
- journal/year/article-type signals recoverable from metadata;
- whether the folder appears single-journal/single-genre or mixed.

Use filenames and PDF metadata only for the preflight. Do not read full article prose merely to plan the workflow.

## Minimal decision pass

After preflight, infer defaults and present them. Ask only unresolved decisions such as:

- mixed journals: one combined field guide or separate journal guides;
- mixed explicit genres: which genres to include or whether to create separate guides;
- project destination when no writable parent is evident;
- final use when it changes outputs: analysis only, drafting, manuscript revision, or all three.

Do not require the user to specify modules, move codes, method strata, split ratios, or batch sizes. Propose these from corpus evidence and size, and let the user approve or adjust them.

## Choose the execution mode

Use these as planning defaults, not rigid laws:

| Usable PDFs | Mode | Suggested design |
|---:|---|---|
| 1–7 | exploratory only | Explain that stable frequency rules and holdout validation are not defensible; offer qualitative pattern notes |
| 8–24 | small corpus | 3–5 pilot, remaining development, optional 20–25% holdout if coverage permits |
| 25–49 | standard corpus | balanced pilot, development, and about 20–25% holdout |
| 50+ | large incremental | pilot + calibration + locked-codebook scale batches + 20–25% holdout |

Stratify by dimensions likely to change rhetoric—method/design, article genre, time/editorial era—only when metadata supports them. Never invent balance from missing labels.

## Plan output

Before project initialization, give the user a compact plan containing:

1. inferred scope and inclusion/exclusion proposal;
2. corpus audit and metadata strategy;
3. development/holdout design and leakage controls;
4. pilot extraction and visual QA;
5. move-code induction and calibration;
6. bounded scale batches and checkpoint policy when applicable;
7. frozen guide contents;
8. Holdout validation;
9. optional manuscript diagnosis/revision stage;
10. expected project directory and artifacts;
11. estimated manual decisions and major cost/token drivers.

End with the staged execution contract:

```text
已规划第 0 步：<folder preflight summary>
下一步：第 1 步，<bounded action>
需要手动的工作：<none or one concrete decision>
是否进行下一步？
```

## Default gates

Adapt names to the corpus, but preserve the dependency order:

0. read-only preflight of the already prepared PDF folder and plan;
1. initialize project layout and immutable source pointer;
2. build/audit registry and match metadata;
3. normalize article types and method/design labels;
4. approve inclusion pool and assign development/holdout before style induction;
5. pilot extraction and visual QA;
6. extract development only;
7. induce pilot move codebook;
8. calibrate and lock the codebook;
9. code development in bounded batches and persist cumulative statistics;
10. generate checkpoint guide(s), then freeze the full development guide;
11. freeze evaluation questions and thresholds;
12. open and evaluate Holdout without changing rules;
13. record validation decision and, only if authorized, create a separate post-validation guide;
14. optionally build a manuscript-specific revision profile and proceed section by section.

For fewer than 50 papers, merge gates where doing so does not weaken QA or Holdout isolation. For 50+ papers, read `large-corpus.md` and keep batch gates explicit.

## Source and project separation

- Treat `pdf_folder` as immutable input by default.
- Store its absolute path and an inventory/hash record in the project registry.
- Prefer a separate project root with generated `00_pdfs` links or a recorded source pointer; do not duplicate a large corpus unless the user requests canonical copies.
- Never rename/delete source PDFs during audit. If canonical renaming is later approved, preserve a rename map and recoverable originals.

## What the assistant should say at first use

If the user invokes the skill without a path, ask:

```text
请提供已经准备好的期刊 PDF 文件夹绝对路径。拿到路径后，我会从本地 PDF 语料审计开始，再给出分阶段指南生成计划；本 skill 不负责抓取或下载论文，在你确认前也不会移动或修改原始 PDF。
```

If the path is already present, begin Gate 0 immediately and do not ask the user to repeat it.
