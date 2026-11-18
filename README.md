# Journal Style Corpus

A reusable Codex skill for turning journal article PDFs into an audited writing-style corpus, rhetorical-move dataset, evidence-based style guide, and holdout validation.

It is journal- and discipline-agnostic: modules and move codes are induced from each target corpus rather than copied from a fixed IMRaD or JIBS template.

## Install

Copy this repository into your Codex skills directory:

```bash
git clone https://github.com/tomato-daydayup/journal-style-corpus.git ~/.codex/skills/journal-style-corpus
```

## Use

Invoke it in Codex with:

```text
Use $journal-style-corpus to turn my journal PDFs into a validated writing-style corpus and guide.
```

See [SKILL.md](SKILL.md) for the workflow and constraints.

## Included tools

- `init_journal_corpus.py`: initialize a corpus workspace.
- `validate_style_corpus.py`: validate modules, extraction noise, and holdout isolation.
- `analyze_move_coding.py`: calculate article-level move coverage and sequence transitions.

The repository does not contain source articles, extracted journal text, or project-specific style guides.
