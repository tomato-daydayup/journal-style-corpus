# Corpus schemas

## Registry

Required columns:

```text
citation_key,title,journal,year,pdf_file,article_type,method_family,method_group,dataset_split,status,notes
```

Recommended values:

- `dataset_split`: `development` or `holdout`;
- `status`: `ready`, `missing_pdf`, `duplicate`, `excluded`, `review_required`;
- `method_family`: specific design, e.g. `difference_in_differences`;
- `method_group`: broader comparison group, e.g. `quasi_experimental`.

Citation keys must be unique. `pdf_file` should be a basename, not an unstable absolute path.

For incremental projects, add:

```text
incremental_phase,batch_id,batch_order,codebook_version,coding_status
```

Keep `dataset_split` authoritative. Pilot, calibration, and scale batches are all development; holdout is never assigned a development batch.

## Section frontmatter

```yaml
---
citation_key: exampleKey2026
title: "Article title"
journal: "Journal name"
year: 2026
source_pdf: 01_exampleKey2026.pdf
module: introduction
page_start: 1
page_end: 3
boundary_confidence: 0.95
split: development
extraction_engine: poppler_bbox_layout_blocks
---
```

Add target-specific fields when useful, but keep these stable for validation.

## Extraction report

One row per article:

```text
citation_key,pdf_file,page_count,modules_detected,references_excluded,boundary_confidence,status,review_note
```

Module page ranges can be separate columns or a JSON field.

## Paragraph move coding

Recommended columns:

```text
citation_key,cohort,module,paragraph_id,paragraph_position,
primary_move,primary_move_label,secondary_moves,transition_marker,
citation_role,tense_voice,sentence_count,research_link,
representative_excerpt,extraction_quality,quality_note,review_status,
codebook_version,batch_id
```

Rules:

- `paragraph_position` preserves raw order, e.g. `3/12`;
- `secondary_moves` is semicolon-separated;
- `research_link` may reference hypotheses, propositions, research questions, models, tables, or figures;
- `extraction_quality`: `clean` or `review`;
- do not put excluded tables/formulas in the coding file.
- `codebook_version` and `batch_id` are required in cumulative large-corpus coding, although the merge tool may add them from command arguments to a new batch file.

## Incremental batch plan

```text
citation_key,dataset_split,incremental_phase,batch_id,batch_order,
stratum,codebook_version,coding_status
```

Recommended `incremental_phase` values: `pilot`, `calibration`, `scale`, and `holdout`. Recommended `coding_status`: `planned`, `in_progress`, `coded`, `qa_complete`, or `excluded`.

## Excluded-noise log

```text
citation_key,module,paragraph_position_raw,exclusion_reason,text
```

Common reasons: `author affiliation`, `editorial note`, `footnote`, `table body`, `figure caption`, `equation fragment`, `publisher header/footer`, `short extraction fragment`.

## Coverage output

```text
module,move,papers_with_move,total_papers,article_coverage_percent,
stability_tier,median_normalized_first_position,papers
```

## Transition output

```text
module,source_move,target_move,transition_count,share_of_module_transitions_percent
```

## Method-group coverage

```text
method_group,group_papers,module,move,papers_with_move,coverage_percent
```

## Version record

Record at least:

```text
guide_version,created_at,development_n,holdout_n,codebook_version,
extraction_version,holdout_opened,notes
```

Once holdout is opened, do not overwrite the frozen development guide.

## Manuscript revision profile

Recommended YAML:

```yaml
manuscript_id: example_manuscript
writing_destination: "Target journal or field"
guide_version: v1.0-validated
guide_status: validated
article_type: empirical_article
method_family: difference_in_differences
sections_in_scope: [introduction, theory, method, results, discussion]
source_file: manuscript.md
author_constraints: []
hard_preserve:
  - claims_and_calibrated_certainty
  - citations_and_claim_links
  - equations_and_notation
  - numerical_results
  - hypotheses_and_labels
  - table_and_figure_references
```

## Section diagnosis

```text
paragraph_id,current_function,target_move,status,issue,
recommended_action,rule_id,evidence_tier,author_query
```

Use `status` values such as `aligned`, `missing`, `duplicated`, `misordered`, `unclear`, or `substantive_gap`. A substantive gap requires an author query, not generated content.

## Revision log

```text
change_id,section,paragraph_id,change_type,summary,rule_id,
priority,evidence_tier,preserved_elements,conflict,author_query
```

Material changes should link to a guide rule. Pure copyediting may use `editorial_cleanup` as the rule ID but must not change claims.

## Preservation audit

```text
check,status,evidence,notes
```

Required checks: numerical results, citations, equations/notation, labels, terminology, causal strength, limitations, cross-references, method-result alignment, and unresolved author queries.
