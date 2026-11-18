---
name: journal-style-corpus
description: Build a reusable writing-style corpus and evidence-based style guide from journal article PDFs. Use when selecting, auditing, sectioning, coding, comparing, or validating articles to learn a journal or field's rhetorical writing patterns without model fine-tuning. Supports quantitative and qualitative articles across disciplines; do not use for ordinary one-paper summarization or literature reviews whose primary goal is substantive findings.
---

# Journal Style Corpus

Turn a set of journal PDFs into a reproducible style-analysis corpus, a move-code dataset, a formal writing guide, and a clean holdout validation. Treat this as corpus analysis, not model training.

## Start by fixing the study design

Before modifying files, establish or infer:

- target journal/field and article type;
- corpus root and available metadata;
- modules relevant to that field (do not assume IMRaD);
- intended development/holdout split;
- design strata worth balancing (method, epistemology, article format, period);
- final use: analysis, drafting, revision, or all three.

If the user has already chosen these, preserve them. Do not move holdout papers into development to increase sample size.

For a new corpus, run `scripts/init_journal_corpus.py --root <corpus-root>` and adapt the generated configuration. Read [references/workflow.md](references/workflow.md) before executing the full workflow. Read [references/schemas.md](references/schemas.md) when creating registries or coding tables.

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

## Workflow

### 1. Audit and register

Inventory PDFs, metadata, duplicates, missing items, article types, years, and method/design families. Create a registry using the schema in [references/schemas.md](references/schemas.md). Do not delete duplicates without explicit authorization; when authorized, log what was removed.

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
- rerunnable scripts/configuration.

## Completion criteria

Do not call the workflow complete merely because files were generated. Confirm:

- every intended development article has all required modules or an explicit exception;
- holdout leakage is zero;
- extraction noise is removed or flagged;
- coverage denominators match the registered development set;
- method/design subgroups are named and their sizes reported;
- style rules cite development evidence and distinguish observation from recommendation;
- scripts compile/run and generated artifacts are non-empty.
