#!/usr/bin/env python3
"""Initialize a reusable journal-style corpus workspace."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


REGISTRY_FIELDS = [
    "citation_key", "title", "journal", "year", "pdf_file", "article_type",
    "method_family", "method_group", "dataset_split", "status", "notes",
    "incremental_phase", "batch_id", "batch_order", "codebook_version",
    "coding_status",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--journal", default="")
    parser.add_argument("--modules", nargs="+", default=["introduction", "theory", "method", "results"])
    args = parser.parse_args()

    root = args.root.expanduser().resolve()
    directories = [
        root / "00_pdfs",
        root / "01_registry",
        root / "02_extracted" / "full_text",
        root / "04_style_analysis",
        root / "04_style_analysis" / "batches",
        root / "04_style_analysis" / "cumulative",
        root / "04_style_analysis" / "guide_versions",
        root / "05_manuscript_revision",
        root / "scripts",
        root / "tmp" / "pdfs",
        *[root / "03_sections" / module for module in args.modules],
    ]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

    registry = root / "01_registry" / "corpus_registry.csv"
    if not registry.exists():
        with registry.open("w", encoding="utf-8", newline="") as handle:
            csv.DictWriter(handle, fieldnames=REGISTRY_FIELDS).writeheader()

    config = root / "corpus_config.json"
    if not config.exists():
        config.write_text(
            json.dumps(
                {
                    "journal": args.journal,
                    "modules": args.modules,
                    "development_label": "development",
                    "holdout_label": "holdout",
                    "style_analysis_goal": "rhetorical moves and writing style",
                },
                indent=2,
                ensure_ascii=False,
            ) + "\n",
            encoding="utf-8",
        )

    print(f"Initialized corpus at {root}")
    print(f"Registry: {registry}")
    print(f"Configuration: {config}")


if __name__ == "__main__":
    main()
