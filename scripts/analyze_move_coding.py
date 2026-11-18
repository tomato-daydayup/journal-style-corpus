#!/usr/bin/env python3
"""Generate generic article coverage and primary-move transition tables."""

from __future__ import annotations

import argparse
import csv
import statistics
from collections import Counter, defaultdict
from pathlib import Path


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def position(row: dict[str, str]) -> int:
    return int(row["paragraph_position"].split("/", 1)[0])


def codes(row: dict[str, str]) -> list[str]:
    return [row["primary_move"], *[x for x in row.get("secondary_moves", "").split("; ") if x]]


def tier(percent: float) -> str:
    return "core" if percent >= 75 else "common" if percent >= 50 else "optional" if percent >= 25 else "rare"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--coding", required=True, type=Path)
    parser.add_argument("--registry", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    coding = read_csv(args.coding)
    registry = read_csv(args.registry)
    development = {row["citation_key"] for row in registry if row.get("dataset_split") == "development"}
    holdout = {row["citation_key"] for row in registry if row.get("dataset_split") == "holdout"}
    coded_keys = {row["citation_key"] for row in coding}
    leakage = coded_keys & holdout
    if leakage:
        raise SystemExit(f"Holdout leakage: {sorted(leakage)}")
    papers = sorted(coded_keys & development)
    if coded_keys - development:
        raise SystemExit(f"Coding contains unregistered/non-development keys: {sorted(coded_keys - development)}")

    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in coding:
        grouped[(row["citation_key"], row["module"])].append(row)
    for rows in grouped.values():
        rows.sort(key=position)

    modules = sorted({row["module"] for row in coding})
    coverage: list[dict[str, str]] = []
    transitions: list[dict[str, str]] = []
    for module in modules:
        moves = sorted({code for row in coding if row["module"] == module for code in codes(row)})
        for move in moves:
            containing = []
            first_positions = []
            eligible = [paper for paper in papers if grouped[(paper, module)]]
            for paper in eligible:
                rows = grouped[(paper, module)]
                if any(move in codes(row) for row in rows):
                    containing.append(paper)
                    first = next(i for i, row in enumerate(rows, 1) if move in codes(row))
                    first_positions.append(first / len(rows))
            percent = 100 * len(containing) / max(1, len(eligible))
            coverage.append({
                "module": module,
                "move": move,
                "papers_with_move": str(len(containing)),
                "eligible_papers": str(len(eligible)),
                "article_coverage_percent": f"{percent:.1f}",
                "stability_tier": tier(percent),
                "median_normalized_first_position": f"{statistics.median(first_positions):.3f}" if first_positions else "",
                "papers": "; ".join(containing),
            })

        counter: Counter[tuple[str, str]] = Counter()
        for paper in papers:
            sequence = []
            for row in grouped[(paper, module)]:
                move = row["primary_move"]
                if not sequence or sequence[-1] != move:
                    sequence.append(move)
            counter.update(zip(sequence, sequence[1:]))
        total = sum(counter.values())
        for (source, target), count in counter.most_common():
            transitions.append({
                "module": module,
                "source_move": source,
                "target_move": target,
                "transition_count": str(count),
                "share_percent": f"{100 * count / max(1, total):.1f}",
            })

    write_csv(args.output / "move_article_coverage.csv", coverage)
    write_csv(args.output / "move_sequence_transitions.csv", transitions)
    print(f"Analyzed {len(coding)} paragraphs from {len(papers)} development papers")


if __name__ == "__main__":
    main()
