# Large-corpus incremental mode

Use this mode when the corpus is large enough that repeatedly reading historical prose would waste context, or when papers arrive over time. The durable evidence is the registry, codebook, paragraph coding, QA decisions, cumulative statistics, and versioned guide.

## Operating model

Keep four cohorts distinct:

- **pilot:** diverse development papers used to induce moves;
- **calibration:** development papers used to refine definitions and test coding consistency;
- **scale:** development batches coded with a locked codebook;
- **holdout:** unopened evaluation papers.

For 200 papers, a defensible starting plan is 12 pilot, 28 calibration, 120 scale, and 40 holdout. Adapt counts to the actual design strata; the numbers are defaults, not universal requirements.

## Plan batches

First set `dataset_split` in the registry. The planner never converts holdout into development.

```bash
python scripts/manage_incremental_corpus.py plan \
  --registry 01_registry/corpus_registry.csv \
  --output 01_registry/incremental_batch_plan.csv \
  --pilot 12 --calibration 28 --batch-size 20 \
  --strata method_group article_type
```

The planner uses deterministic stratum interleaving. Review the plan manually because deterministic balancing cannot repair missing or inaccurate metadata.

For a 191-paper single-genre corpus, a reasonable project-specific configuration is 12 pilot, 28 calibration, 113 scale, and 38 holdout. Divide scale into bounded batches such as 20, 20, 20, 20, 20, and 13. Balance assignment across period and method/design strata; do not treat file order as randomization.

## Staged execution gates

When the user asks to approve each step, use explicit gates and stop after every gate:

1. confirm the genre pool and update the reusable workflow;
2. create the directory layout and project control file;
3. build and audit the article registry;
4. enrich method/design metadata and flag uncertain cases;
5. assign pilot, calibration, scale, and holdout cohorts;
6. test extraction on the pilot and resolve material defects;
7. extract development sections only;
8. induce moves on pilot;
9. calibrate and lock the codebook;
10. code and merge each scale batch as its own gate;
11. update the full guide only at declared checkpoints;
12. freeze the development guide;
13. open and evaluate holdout;
14. create a separately versioned post-validation guide if authorized.

At the end of each gate, report exactly:

- `已执行第 N 步：` completed work and generated artifacts;
- `验证结果：` counts, checks, and unresolved exceptions;
- `下一步：` the next bounded action;
- `需要手动的工作：` `无` or a concrete review/decision;
- `是否进行下一步？`

Do not start the next gate in the same turn unless the user explicitly requests continuous execution.

## Codex App batch pattern

Treat files as durable memory. Do not rely on a long-running chat to remember prior coding decisions. For an ordinary scale batch, load only:

- the batch rows from the approved plan;
- the corresponding cleaned section files;
- the locked codebook and its version;
- the cumulative ledger needed for duplicate and leakage checks;
- the current QA rubric.

Save the batch coding and QA summary before merging. After merge, create a guide delta rather than reopening old prose or rewriting the complete guide.

A suitable bounded batch instruction is:

```text
Use journal-style-corpus and process only <batch_id> from the approved plan.
Use <codebook_version>; do not change code definitions or read holdout.
Save paragraph coding and QA flags, merge deterministically, recompute
cumulative statistics, and produce a guide delta. Stop after reporting this gate.
```

At a formal guide checkpoint, do not load article prose. Load the frozen codebook, current guide, previous and current cumulative statistics, batch QA summaries, and guide deltas. Update the guide with a versioned change log.

## Codebook lifecycle

Induce on pilot, refine on calibration, and assign a named version before scale coding. After lock:

- existing codes may be clarified without changing their boundary only if the clarification is logged;
- a changed boundary requires a new codebook version;
- a candidate new move stays provisional until old coding is searched for affected paragraphs;
- incompatible versions are not merged silently;
- a migration records which old articles/paragraphs were recoded.

## Batch execution

Each batch should produce one CSV in `04_style_analysis/batches/`. Process only new section files. Use the current locked codebook and record low-confidence/multi-move/noisy cases for QA.

Do not re-read old article prose for ordinary updates. Old prose may be reopened for:

- targeted codebook migration;
- resolving a QA flag;
- checking an apparent statistical anomaly;
- selecting a short, licensed representative excerpt.

## Merge and analyze

```bash
python scripts/manage_incremental_corpus.py merge \
  --root . \
  --batch-coding 04_style_analysis/batches/scale_01.csv \
  --batch-id scale_01 \
  --codebook-version v1
```

The merge command:

1. checks required coding fields;
2. rejects unplanned, holdout, and duplicate paragraph rows;
3. rejects incompatible codebook versions;
4. rewrites cumulative coding deterministically;
5. runs coverage and transition analysis;
6. writes a guide-delta packet.

The command is idempotent for the same batch: identical rows do not multiply. Conflicting rows stop the run.

## Guide update policy

Between formal checkpoints, create a delta rather than rewriting the full guide. Load only:

- frozen codebook;
- current guide;
- current and previous cumulative statistics;
- new-batch QA summary;
- guide-delta packet.

Update a rule when evidence crosses a declared tier, order/transition evidence changes materially, a method-specific variant stabilizes, or a prior recommendation is contradicted. Otherwise update denominators or record “no material change.”

Useful checkpoints for a 160-paper development set are N=12, 40, 80, 120, and 160. Freeze the development guide at N=160 before opening the 40-paper holdout.

For a 153-paper development set, use N=12, 40, 80, 120, and 153, then freeze before opening holdout.

## Token discipline

- classify method/design through a metadata-first funnel: bibliographic abstract, then targeted PDF snippets, then model adjudication;
- match bibliographic records by normalized DOI and report coverage before trusting metadata;
- cache the compact classification evidence and its source; do not repeatedly parse PDFs after a decision is persisted;
- send one article/module or a bounded batch to the model, not the corpus;
- cache coding and never ask the model to recreate it from prose;
- use scripts for counts, joins, transitions, and tier changes;
- keep excerpts short and only for adjudication or examples;
- retain a compact guide-change log;
- report input article/paragraph counts for every batch.

Token savings come from avoiding repeated historical prose, not from reducing evidence quality.
