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
representative_excerpt,extraction_quality,quality_note,review_status
```

Rules:

- `paragraph_position` preserves raw order, e.g. `3/12`;
- `secondary_moves` is semicolon-separated;
- `research_link` may reference hypotheses, propositions, research questions, models, tables, or figures;
- `extraction_quality`: `clean` or `review`;
- do not put excluded tables/formulas in the coding file.

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
