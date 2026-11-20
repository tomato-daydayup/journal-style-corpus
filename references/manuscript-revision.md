# Manuscript diagnosis and revision

Use this reference only when the task includes applying a frozen corpus guide to a draft. The goal is journal-aware rhetorical revision with a complete preservation and provenance trail.

## Contents

1. Entry gate and inputs
2. Rule priority
3. Manuscript-specific profile
4. Section diagnosis
5. Section revision
6. Revision log
7. Whole-manuscript audit
8. Output layout

## 1. Entry gate and inputs

Prefer a frozen development guide that has passed holdout validation. If validation is incomplete, label the guide `development-only` and tell the user that its rules are provisional. Never imply journal acceptance or stylistic certainty.

Required inputs:

- manuscript source or readable export;
- writing destination and article type;
- frozen guide path and version;
- sections in scope;
- method/design family;
- author constraints and desired edit intensity.

Record the source hash or modification time when practical. Work on copies or Markdown intermediates; do not overwrite the original by default. If the manuscript is PDF, extract it for diagnosis but request an editable source before claiming a production-ready revision.

## 2. Rule priority

Apply the following hierarchy:

| Priority | Rule class | Treatment |
|---|---|---|
| P1 | Hard preserve | Do not alter without explicit authorization |
| P2 | Validated target-style rules | Apply when relevant to this genre/method |
| P3 | Manuscript coherence | Preserve established logic and terminology |
| P4 | Optional preferences | Apply only when they improve clarity and do not conflict |
| P5 | Cleanup | Remove avoidable noise without changing substance |

P1 includes facts, samples, constructs, measures, citations, equations, numerical results, signs/significance, hypothesis and model labels, table/figure references, causal strength, limitations, and explicit uncertainty.

P2 rules must come from the named guide version. Prefer core/common rules; use design-specific variants for the matching method. Do not turn optional or rare patterns into requirements.

P3 prevents local stylistic improvements from breaking the manuscript's research question, theory-to-hypothesis chain, method-result mapping, terminology, or cross-section promises.

P4 may include user/lab preferences and general academic-writing defaults. Label these sources; they cannot override P1–P3.

P5 includes redundant meta-discourse, repeated claims, empty intensifiers, vague references, and extraction residue. Cleanup is not permission to strengthen claims.

When rules conflict, follow the higher priority and record the conflict if it affects meaning, organization, or an explicit user preference.

## 3. Manuscript-specific profile

Create `revision_profile.md` before revision. It should contain:

- manuscript metadata and source;
- writing destination, guide version/status, and applicable method variant;
- sections and edit intensity in scope;
- P1 hard-preserve inventory;
- selected P2 rules with IDs, evidence tiers, coverage denominators, and applicability notes;
- P3 terminology and cross-section commitments;
- P4 preferences and their sources;
- known exclusions and unresolved questions.

Translate the guide into actionable rules; do not paste the entire guide. A selected rule should state the reader need, action, evidence tier, eligible sections, and exceptions.

Present the profile for review before revision. If the user explicitly requested an end-to-end unattended pass, proceed but mark assumptions in the output.

## 4. Section diagnosis

Diagnose before rewriting. For each section:

1. identify its reader question and expected communicative purpose;
2. segment the source into stable paragraph IDs;
3. assign each paragraph a current rhetorical function;
4. compare observed moves and order with applicable P2 rules;
5. flag missing, duplicated, misordered, or weakly realized moves;
6. assess paragraph focus, transitions, citation function, tense/voice, and links to hypotheses/models/tables;
7. separate rhetorical defects from absent evidence or reasoning.

For every recommendation, include a rule ID and evidence tier. Recommendations without corpus support must be labeled `editorial judgment`.

Use an author query when:

- a claimed contribution lacks a defensible basis in the source;
- a required method detail is absent;
- results and prose appear inconsistent;
- a transition requires a substantive premise not supplied;
- a citation, number, label, or cross-reference is ambiguous.

Do not solve these gaps by invention. Save the result as `[section]_diagnosis.md`.

## 5. Section revision

Revise one complete section at a time in the agreed order. Before editing, preserve an immutable copy of the section.

For each paragraph:

- keep or deliberately change its rhetorical function;
- apply only relevant selected rules;
- preserve citation-to-claim proximity and scope;
- preserve all numbers, signs, significance statements, labels, and notation;
- retain calibrated verbs such as `suggest`, `associate`, or `cause` unless the evidence in the manuscript authorizes a change;
- use slot-based patterns, never phrases copied from corpus papers;
- maintain the author's technical terminology unless the profile records an approved normalization.

Reordering is allowed when it improves the move sequence, but the log must map old paragraph IDs to new positions. Splitting or merging paragraphs must preserve sentence provenance. If a target move needs new substance, insert `[AUTHOR QUERY: ...]` or keep it in the query list rather than drafting unsupported content.

After revising a section, check:

- all original factual propositions remain represented;
- citations still support the same claims;
- equations, results, hypotheses, tables, and figures are referenced consistently;
- the intended move sequence is visible without mechanical signposting;
- no optional corpus pattern has been presented as mandatory;
- prose is original and not derived from corpus wording.

## 6. Revision log

Save `[section]_revision_log.md`. Include:

- source and revised file names;
- rule IDs applied and their priority/evidence tier;
- paragraph mapping for moves, splits, and merges;
- material deletions, additions, and reordering;
- P1 elements checked and preserved;
- priority conflicts and their resolution;
- editorial judgments not directly supported by corpus evidence;
- unresolved author queries.

Do not use an unexplained journal-fit score. If a score is requested, define a rubric first and report dimension-level evidence rather than a false acceptance probability.

## 7. Whole-manuscript audit

After all requested sections are revised, verify:

- stable terminology and construct definitions;
- consistent research questions, hypotheses, proposition and model labels;
- introduction promises match theory, method, results, and discussion;
- method descriptions match reported analyses;
- results claims match numbers, direction, and uncertainty;
- contribution claims do not exceed the demonstrated findings;
- citations, equations, tables, figures, appendices, and section references resolve;
- tense and voice vary appropriately by rhetorical function;
- all author queries are collected and none are silently resolved.

Produce `revision_summary.md` and `preservation_audit.md`. The summary distinguishes corpus-grounded changes, manuscript-coherence changes, optional preferences, and cleanup.

## 8. Output layout

```text
05_manuscript_revision/
|-- revision_profile.md
|-- author_queries.md
|-- original_sections/
|   `-- [section].md
|-- diagnoses/
|   `-- [section]_diagnosis.md
|-- revised_sections/
|   `-- [section]_revised.md
|-- logs/
|   `-- [section]_revision_log.md
|-- revision_summary.md
`-- preservation_audit.md
```

Keep machine-readable CSV versions of diagnoses and logs when the project needs aggregation. Preserve the frozen guide and its version record outside this directory; do not silently edit it during manuscript revision.
