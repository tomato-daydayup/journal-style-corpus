# Reusable journal-corpus workflow

## Contents

1. Project layout
2. Corpus design
3. PDF extraction and cleaning
4. Quality assurance
5. Move induction and coding
6. Stability analysis
7. Style-guide construction
8. Holdout validation

## 1. Project layout

Recommended layout:

```text
corpus-root/
|-- 00_pdfs/                 Canonical source PDFs; do not edit
|-- 01_registry/             Registry, audit, split records
|-- 02_extracted/
|   |-- full_text/           Provenance-oriented extraction
|   `-- extraction_report.csv
|-- 03_sections/             One folder per target module
|-- 04_style_analysis/       Codebook, coding CSVs, statistics, guide
|-- scripts/                 Corpus-specific reproducible scripts
`-- tmp/pdfs/                Disposable extraction/render intermediates
```

Use the target field's own section names. Examples include Introduction/Theory/Method/Results, Background/Materials/Analysis/Discussion, or discipline-specific structures.

## 2. Corpus design

### Inclusion criteria

Define journal, time window, article type, empirical/theoretical status, language, and accessibility. Exclude documents whose genre would distort the target unless the user wants a mixed-genre guide.

### Strata

Potential balancing variables:

- quantitative, qualitative, mixed methods;
- experiment, survey, archival, ethnography, simulation, case study;
- full article, research note, review;
- older/newer editorial eras;
- single-country/multicountry;
- theory-building/theory-testing.

Choose only dimensions likely to influence rhetoric. Report counts; do not pretend tiny strata support precise differences.

### Split

Make the split before inducing rules. A common small-corpus design is:

- pilot: 3–5 development articles spanning major formats;
- remaining development: used to estimate stability;
- holdout: 20–30%, balanced where possible.

The holdout is evaluation data, not extra evidence for the style guide.

## 3. PDF extraction and cleaning

### Reading order

For born-digital PDFs, compare Poppler default extraction and `-bbox-layout`. Default extraction often preserves reading order; bbox output helps identify layout blocks and paragraph indentation. Scanned PDFs require OCR and additional QA.

### Boundary detection

Use article-specific headings when formats vary. Record start/end pages and confidence. When one logical module spans several headings, define the boundary at the first relevant heading and retain meaningful subheadings.

### Paragraph recovery

Join wrapped lines only when they belong to the same layout paragraph. Useful signals include line indentation, block coordinates, incomplete sentence endings, and page/column transitions. Never turn an entire section into one paragraph.

### Noise removal

Handle these separately:

- recurring headers, footers, page numbers;
- editorial history (`Accepted by...`, revisions);
- author emails, affiliations, addresses;
- numbered notes at page bottoms and their superscript markers;
- publisher artifacts;
- table titles, headers, cells, notes, and significance legends;
- figure captions if visual rhetoric is out of scope;
- formula fragments.

Retain prose that interprets a table/figure. For example, keep “Table 2 shows a negative association...” while removing the table matrix.

### Tables and footnotes

PDF reading order may insert a table or footnote between two halves of a sentence. Remove the non-prose block, then rejoin only if the surrounding text is syntactically incomplete. Validate against the rendered page when uncertain.

## 4. Quality assurance

Automated checks:

- expected article/module counts;
- empty or unusually short sections;
- page-marker residue;
- emails/editorial notes/affiliations;
- table titles and high numeric density;
- publisher headers;
- references/discussion leaking into earlier modules;
- holdout citation keys in development artifacts.

Visual checks:

- render every pilot boundary page;
- render representative old/new and one-/two-column layouts;
- inspect pages containing tables, equations, and footnotes;
- confirm the latest extraction after every meaningful rule change.

Keep a manual review checklist with article-specific risks.

## 5. Move induction and coding

Induce moves from pilot prose by asking: “What communicative job does this paragraph perform for a reader?” Do not create separate codes for every topic.

A useful codebook entry contains:

- code and label;
- functional definition;
- inclusion cues;
- exclusion cues;
- common neighboring moves;
- multi-move example;
- representative development excerpt;
- confidence/notes.

Use one primary move plus optional secondary moves. Preserve raw paragraph order and article/module identity.

## 6. Stability analysis

### Article coverage

For move `m`:

```text
coverage(m) = number of development articles containing m
              / total development articles eligible for that module
```

Article coverage is more useful for a style rule than paragraph frequency, which can be dominated by long papers.

### Order

For each article/module:

1. order paragraphs;
2. take primary moves;
3. collapse adjacent duplicates;
4. count adjacent transitions;
5. calculate normalized first position for each move.

Use these statistics to describe typical architecture. Do not infer that the median order is the only acceptable order.

### Groups

Compare coverage by method/design only when groups have defensible definitions. Always show group N. Treat N<3 as illustrative.

### Rule tiers

A useful default:

- core: >=75% article coverage;
- common: 50–74.9%;
- optional: 25–49.9%;
- rare: <25%.

Adjust thresholds when corpus size or genre warrants it, and report the chosen thresholds.

## 7. Style-guide construction

For each module, translate descriptive findings into a reader-centered guide:

1. reader question;
2. evidence table;
3. recommended architecture;
4. move-by-move instructions;
5. paragraph templates with semantic slots;
6. tense, voice, transitions, citation roles;
7. method/article-type variants;
8. checklist and anti-patterns.

Do not claim the corpus establishes grammatical rules it did not measure. Keep direct excerpts short and use them as evidence, not templates to copy.

## 8. Holdout validation

Freeze and version the guide. Extract/code holdout using the existing codebook. Compare:

- move presence/absence;
- order and transitions;
- module length and paragraph structure;
- tense/voice/citation behavior;
- method-specific templates;
- drafting/revision performance if Codex-generated text is tested.

Classify failures as extraction error, coding error, style-rule error, method/genre variant, or insufficient factual input. Preserve the original guide before any post-holdout revision.
