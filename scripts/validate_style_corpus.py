#!/usr/bin/env python3
"""Validate corpus structure, module coverage, noise, and holdout isolation."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path


NOISE_PATTERNS = {
    "page_marker": re.compile(r"<!--\s*page:", re.I),
    "email": re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}"),
    "editorial_note": re.compile(r"Accepted by|has been with the authors for .* revisions", re.I),
    "publisher_artifact": re.compile(r"Vol\.:?\s*\(0123456789\)|© The Author", re.I),
    "table_title": re.compile(r"(?m)^Table\s+[A-Z]?\d+\b(?!\s+(?:shows?|reports?|presents?|provides?|indicates?|investigates?)\b)", re.I),
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--coding", type=Path, help="Optional paragraph coding CSV to check for holdout leakage")
    args = parser.parse_args()
    root = args.root.expanduser().resolve()

    config_path = root / "corpus_config.json"
    config = json.loads(config_path.read_text(encoding="utf-8")) if config_path.exists() else {}
    modules = config.get("modules") or [p.name for p in (root / "03_sections").iterdir() if p.is_dir()]
    registry_path = root / "01_registry" / "corpus_registry.csv"
    if not registry_path.exists():
        raise SystemExit(f"Missing registry: {registry_path}")
    registry = read_csv(registry_path)
    keys = [row.get("citation_key", "") for row in registry]
    duplicates = sorted(key for key, count in Counter(keys).items() if key and count > 1)
    development = {row["citation_key"] for row in registry if row.get("dataset_split") == "development"}
    holdout = {row["citation_key"] for row in registry if row.get("dataset_split") == "holdout"}

    issues: list[str] = []
    if duplicates:
        issues.append(f"Duplicate citation keys: {', '.join(duplicates)}")
    overlap = development & holdout
    if overlap:
        issues.append(f"Development/holdout overlap: {', '.join(sorted(overlap))}")

    module_counts: dict[str, int] = {}
    noise_counts = Counter()
    missing_modules: list[str] = []
    for module in modules:
        folder = root / "03_sections" / module
        files = list(folder.glob("*.md")) if folder.exists() else []
        module_counts[module] = len(files)
        stems = {path.stem for path in files}
        for key in sorted(development - stems):
            missing_modules.append(f"{key}:{module}")
        for path in files:
            text = path.read_text(encoding="utf-8", errors="replace")
            body = text.split("---", 2)[-1].strip()
            if not body:
                issues.append(f"Empty section: {path}")
            for label, pattern in NOISE_PATTERNS.items():
                if pattern.search(body):
                    noise_counts[label] += 1

    if missing_modules:
        issues.append(f"Missing development modules ({len(missing_modules)}): " + ", ".join(missing_modules[:20]))

    warnings = [f"{label} detected in {count} section file(s)" for label, count in sorted(noise_counts.items()) if count]

    leakage: list[str] = []
    if args.coding:
        coding = read_csv(args.coding)
        leakage = sorted({row.get("citation_key", "") for row in coding} & holdout)
        if leakage:
            issues.append(f"Holdout leakage in coding: {', '.join(leakage)}")

    print(json.dumps({
        "registry_articles": len(registry),
        "development_articles": len(development),
        "holdout_articles": len(holdout),
        "module_file_counts": module_counts,
        "noise_file_counts": dict(noise_counts),
        "holdout_leakage": leakage,
        "warnings": warnings,
        "issues": issues,
        "status": "review_required" if issues else ("pass_with_warnings" if warnings else "pass"),
    }, indent=2, ensure_ascii=False))
    raise SystemExit(0 if not issues else 1)


if __name__ == "__main__":
    main()
