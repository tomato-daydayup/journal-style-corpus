---
name: journal-style-corpus
description: Start from a user-specified folder of already prepared journal article PDFs, plan and run a staged corpus workflow, build a reusable evidence-based writing guide, and optionally diagnose and revise a manuscript against the frozen guide. Use when auditing, sectioning, coding, comparing, validating, drafting, or revising articles to learn a journal or field's rhetorical writing patterns without model fine-tuning. PDF acquisition and publisher scraping are out of scope. Supports quantitative and qualitative articles across disciplines; do not use for ordinary one-paper summarization or literature reviews whose primary goal is substantive findings.
---

# Journal Style Corpus

Turn journal PDFs into a reproducible style-analysis corpus, a move-code dataset, a validated writing guide, and—when requested—a traceable manuscript revision. Treat this as corpus analysis plus rule-governed revision, not model training.

## PDF-folder-first launch

For a new guide project, require only one initial input: **the folder containing the already downloaded source PDFs**. If the user has not supplied it, ask for that folder path as the next and only blocking question. Once supplied:

1. inspect the folder read-only and report PDF count, nested folders, obvious duplicates, naming patterns, and nearby `.bib`, `.ris`, `.csv`, or exported metadata;
2. infer what is safe from the files and metadata, then ask only for decisions that materially change the study—normally target journal/field, included article genre(s), and intended use if these remain ambiguous;
3. propose a numbered, corpus-size-appropriate plan with development/holdout separation, estimated manual decisions, and expected artifacts;
4. create or identify a project root separate from the source PDFs; never reorganize or rename the source folder without explicit authorization;
5. start with the first approved gate, report it in the staged format below, and wait for confirmation before each subsequent gate.

Do not make the user design the corpus workflow before inspecting the folder. Do not ask for information already recoverable from filenames, PDF metadata, publisher metadata, or an adjacent bibliography export. Read [references/onboarding.md](references/onboarding.md) for the required intake, planning logic, corpus-size modes, and first-gate behavior.

## Acquisition boundary

PDF acquisition is a prerequisite, not part of this skill. Do not design, write, run, repair, or recommend journal scrapers; do not browse publisher issue pages to assemble the corpus; and do not add download/acquisition gates to the project plan. If the supplied folder is missing, inaccessible, or contains no usable PDFs, state that the user must prepare the PDF corpus first and stop the guide-generation workflow. Resume when the user provides a usable folder.

Use bibliographic exports or manifests only when they already exist in or alongside the supplied folder. The workflow begins with local corpus audit and ends with guide/manuscript artifacts; it does not cover how the user obtained the PDFs.

## Fix the study design after folder inspection

After inspecting the supplied PDF folder and before modifying files, establish or infer:

- target journal/field and article type;
- corpus root and available metadata;
- modules relevant to that field (do not assume IMRaD);
- intended development/holdout split;
- design strata worth balancing (method, epistemology, article format, period);
- final use: analysis, drafting, revision, or all three.

If the user has already chosen these, preserve them. If a choice remains unknown but does not affect the first read-only audit, proceed with the audit and flag the assumption. Do not move holdout papers into development to increase sample size.

For a new corpus, run `scripts/init_journal_corpus.py --root <corpus-root>` and adapt the generated configuration. Read [references/workflow.md](references/workflow.md) before executing the full workflow. Read [references/schemas.md](references/schemas.md) when creating registries or coding tables.

For roughly 50 or more papers, or whenever papers will arrive over time, use large-corpus incremental mode. Read [references/large-corpus.md](references/large-corpus.md) and use `scripts/manage_incremental_corpus.py`. Do not repeatedly load old article prose merely to update the guide.

New PDF-folder projects use staged execution by default. Define numbered gates before mutating project files. Execute only the current gate, report its outputs and QA result, identify any manual work, name the next gate, and wait for explicit confirmation. A request to begin authorizes the read-only folder audit and planning; project initialization or later mutations start only after the plan/project location is approved unless the user explicitly authorizes continuous execution.

## Preserve these invariants

1. Keep original PDFs unchanged; generated text belongs in separate folders.
2. Maintain one canonical citation key per article and record every rename/missing file.
3. Split development and holdout before inducing writing rules.
4. Use holdout only for evaluation. Never add a rule because it appears in holdout.
5. Derive modules and move codes from the target corpus; JIBS/IMRaD codes are examples, not defaults.
6. Keep tables, equations, figures, footnotes, affiliations, headers, and publisher notes out of prose style analysis unless the user's target explicitly includes them.
7. Preserve narrative references to evidence (for example, “Table 3 shows...”) while removing the table body.
8. Mark uncertain boundaries and extraction noise. Never silently treat corrupted text as style evidence.
9. Separate observed regularities from recommended writing rules and report denominators.
10. Keep all steps rerunnable with scripts/configuration rather than relying on undocumented manual edits.
11. During manuscript revision, preserve the author's claims, evidence, citations, equations, numerical results, labels, and calibrated certainty unless the user explicitly authorizes substantive changes.
12. Never copy, closely paraphrase, or import findings from corpus papers. Corpus evidence governs rhetorical choices, not manuscript content.
13. Do not use holdout observations to revise a manuscript-specific rule unless a post-validation guide version has been explicitly created.
14. In incremental mode, treat paragraph coding as the durable representation of previously read papers. Reopen old prose only for targeted recoding, QA, or a documented codebook migration.
15. Lock a codebook version for each batch. Never silently merge incompatible codebook versions.

## Workflow

### 1. Audit and register

Inventory PDFs, metadata, duplicates, missing items, article types, years, and method/design families. Create a registry using the schema in [references/schemas.md](references/schemas.md). Do not delete duplicates without explicit authorization; when authorized, log what was removed.

Normalize publisher metadata before using article type as a sampling stratum. Treat access badges and publication dates as metadata, not genres. When a publisher page supplies no more specific genre and its apparent type is only `Open access`, `Published: <date>`, or blank, classify the item as the publisher's default `Article`; preserve open-access status and publication date in their own fields. An explicit genre such as `Research Note`, `Review Article`, `Editorial`, or `Commentary` always takes precedence. Record journal-specific overrides when the publisher uses a different default label.

For method/design stratification, use an evidence funnel. Prefer structured bibliographic metadata with abstracts, matched by normalized DOI. Apply deterministic cues to the abstract first. Read PDF Abstract/Method/Data snippets only when metadata is missing, the abstract is insufficient, or cues conflict. Send only the remaining compact evidence packets to the model for adjudication. Cache abstracts, snippets, evidence sources, confidence, and final decisions so later planning never reopens PDFs merely to recreate method labels.

### 2. Split the corpus

Create a small pilot subset inside development, the remaining development set, and a holdout set. Balance by the dimensions that could alter writing structure. Keep the holdout large enough to contain meaningful variation; for small corpora, 20–30% is a useful default, not a hard rule.

### 3. Pilot extraction

Use the PDF skill/workflow when PDF layout matters. Inspect representative pages visually. Extract full text for provenance and section files for analysis. Define article-specific section boundaries when headings vary.

Normalize prose conservatively:

- remove page separators in analysis sections;
- merge only soft line wraps inside a paragraph;
- preserve paragraph boundaries and headings;
- remove author/editor notes and numbered footnotes, including orphan markers;
- remove table bodies from empirical sections while retaining narrative interpretation;
- flag formulas and complex layouts instead of guessing.

Iterate on pilot extraction until section text is readable. Do not scale a known extraction defect to the full corpus.

### 4. Scale extraction

Apply the verified rules to development only. Produce article/module metadata containing source PDF, page range, confidence, split, and extraction engine. Run `scripts/validate_style_corpus.py --root <corpus-root>` and resolve material errors.

### 5. Induce a target-specific move codebook

Read the pilot modules and identify what paragraphs do rhetorically. Start with functions, not topics. Allow one primary move and optional secondary moves. Define inclusion/exclusion cues and multi-move examples.

Use [references/move-analysis.md](references/move-analysis.md) for coding and stability analysis. Do not force the same code inventory across disciplines or article types.

### 6. Code development paragraphs

Code pilot paragraphs, refine the codebook, then code the remaining development articles using the same definitions. Record transition markers, citation role, tense/voice, links to hypotheses/models/research questions, representative excerpts, extraction quality, and review status.

Rule-based or LLM-assisted coding is a first pass. Review low-confidence, multi-move, and noisy paragraphs before using them as exemplars. Keep excluded non-prose units in a separate audit file.

### 7. Analyze stability

Calculate:

- article coverage for each move (not only paragraph frequency);
- typical first position and adjacent transitions;
- recurring module-level sequences;
- differences by method/design/article type;
- uncertainty from small subgroups.

Run `scripts/analyze_move_coding.py` for generic coverage and transition tables. Treat its results as descriptive evidence, not a normative order. A frequent move can occur in different positions for legitimate reasons.

### 8. Write the style guide

Convert evidence into three or four rule tiers, such as core/common/optional/rare. For each module include:

- reader question and communicative purpose;
- coverage table with denominators;
- evidence-weighted architecture;
- paragraph microstructure;
- transitions, tense, voice, and citation functions;
- design-specific variants;
- templates that contain slots, not copied sentences;
- anti-patterns and a review checklist;
- a Codex drafting/revision protocol.

Explicitly state what the guide cannot infer from the corpus.

### 9. Freeze and validate on holdout

Version the development guide before opening holdout. Apply the frozen guide to holdout and compare predicted versus observed move coverage, order, and language choices. Report misses without immediately changing the guide. If the user later authorizes revision, preserve the pre-holdout version and document every change to avoid hidden overfitting.

### Large-corpus incremental mode

The ordinary workflow remains valid, but execute it in persisted batches:

1. split development and holdout before analysis;
2. create a balanced pilot and calibration cohort inside development;
3. induce the codebook on pilot, stabilize it on calibration, then lock a version;
4. process each scale batch once and save article-level coding;
5. merge only the new batch into cumulative coding;
6. recompute cumulative statistics deterministically;
7. generate a guide-delta packet and update only rules whose evidence changed materially;
8. freeze the development guide before opening holdout.

Do not regenerate the whole guide after every batch. Prefer formal guide checkpoints and lightweight delta reports between them. A candidate new move after codebook lock requires targeted retrospective search/recode or a versioned migration; it is not automatically appended.

For Codex App execution, use project files—not chat history—as the source of truth. Keep the registry, batch plan, ledger, locked codebook, cumulative coding, cumulative statistics, QA decisions, guide deltas, and versioned guides on disk. A new chat may process one bounded batch by loading only that batch plus the durable control files. See [references/large-corpus.md](references/large-corpus.md) for batch and checkpoint prompts.

### 10. Build a manuscript-specific revision profile

Use only a frozen, named guide version plus the manuscript; do not re-read corpus papers during revision. Read [references/manuscript-revision.md](references/manuscript-revision.md) before diagnosing or rewriting a manuscript.

Record the writing destination, manuscript genre/method, guide version, sections in scope, author constraints, and factual elements that must remain unchanged. Convert the frozen guide into an actionable manuscript profile only where its evidence applies. Keep journal-level defaults separate from method- or genre-specific variants.

Apply this priority order:

1. **P1 hard preserve:** facts, data, results, citations, equations, labels, terminology, causal strength, limitations, and author-specified constraints;
2. **P2 validated target-style rules:** core/common rules supported by the frozen development guide and its validated variants;
3. **P3 manuscript-specific coherence:** the paper's research question, theory, method, results, cross-references, and established author terminology;
4. **P4 optional style preferences:** optional/rare corpus patterns, user/lab preferences, and general academic-writing defaults;
5. **P5 cleanup:** remove unsupported meta-claims, repetition, vague signposting, and extraction artifacts without changing substance.

Higher priorities win. Log consequential conflicts instead of silently resolving them.

### 11. Diagnose before rewriting

Diagnose one section at a time against the frozen guide. Map each paragraph to its current function, identify missing/duplicated/misordered moves, assess paragraph focus and transitions, and distinguish style problems from missing substantive content.

Do not rewrite during diagnosis. Do not fill a substantive gap with invented material; mark it as an author query. Produce a diagnosis table whose recommendations cite guide rules or identify themselves as optional editorial judgment.

### 12. Revise section by section

Wait for the user's approval of the diagnosis and manuscript-specific profile before substantive rewriting unless the user already explicitly asked for diagnosis and revision in one pass. Revise complete sections in the user's requested order. Preserve citation-to-claim relationships and all P1 content; use semantic-slot templates only, never corpus sentences.

After each section, run factual-preservation, cross-reference, rhetorical-sequence, and language checks. If a requested style move needs information absent from the manuscript, leave a clear placeholder or author query rather than inventing it.

### 13. Log and validate the revision

Save the original section, diagnosis, revised section, and revision log as separate artifacts. The log must identify material changes, applied rule IDs and evidence tiers, preserved content, unresolved author queries, and any priority conflicts. Do not assign numerical “journal fit” scores unless a defined rubric and evidence support them.

After all sections, run a whole-manuscript consistency pass for terminology, contribution claims, hypotheses/research questions, method-result alignment, table/figure references, citation integrity, tense/voice, and cross-section promises. Produce a revision summary and preservation audit; do not overwrite the author's source file by default.

## Expected deliverables

Use names suited to the project, but normally produce:

- corpus registry and audit report;
- development/holdout split record;
- clean module files plus extraction QA;
- move codebook;
- paragraph-level coding CSV;
- excluded-noise log;
- coverage, transition, and method-group tables;
- stability report;
- formal style guide with version;
- holdout validation report when requested;
- manuscript-specific revision profile and section diagnoses when revision is requested;
- revised sections, rule-linked revision logs, author queries, and final preservation audit;
- rerunnable scripts/configuration.
- incremental batch plan, batch ledger, cumulative coding, and guide-delta packets for large corpora;

## Completion criteria

Do not call the workflow complete merely because files were generated. Confirm:

- every intended development article has all required modules or an explicit exception;
- holdout leakage is zero;
- extraction noise is removed or flagged;
- coverage denominators match the registered development set;
- method/design subgroups are named and their sizes reported;
- style rules cite development evidence and distinguish observation from recommendation;
- scripts compile/run and generated artifacts are non-empty.
- every manuscript edit is traceable to a rule or explicit editorial rationale;
- P1 content is preserved or every authorized substantive change is explicitly documented;
- unresolved substantive gaps remain author queries rather than invented prose.
