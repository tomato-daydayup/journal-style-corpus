#!/usr/bin/env python3
"""Plan and merge incremental journal-style corpus batches."""

from __future__ import annotations

import argparse
import csv
import hashlib
import subprocess
import sys
from collections import defaultdict, deque
from pathlib import Path


REQUIRED_CODING = {
    "citation_key", "module", "paragraph_id", "paragraph_position",
    "primary_move", "secondary_moves",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def balanced_order(rows: list[dict[str, str]], strata: list[str]) -> list[dict[str, str]]:
    groups: dict[str, deque[dict[str, str]]] = defaultdict(deque)
    for row in sorted(rows, key=lambda r: (r.get("year", ""), r["citation_key"])):
        label = " | ".join(row.get(field, "").strip() or "unknown" for field in strata)
        groups[label].append(row)
    ordered: list[dict[str, str]] = []
    labels = sorted(groups)
    while any(groups.values()):
        labels.sort(key=lambda label: (-len(groups[label]), label))
        for label in labels:
            if groups[label]:
                row = groups[label].popleft()
                row = dict(row)
                row["_stratum"] = label
                ordered.append(row)
    return ordered


def cmd_plan(args: argparse.Namespace) -> None:
    registry = read_csv(args.registry)
    keys = [row.get("citation_key", "").strip() for row in registry]
    if not all(keys) or len(keys) != len(set(keys)):
        raise SystemExit("Registry citation_key values must be non-empty and unique.")
    development = [row for row in registry if row.get("dataset_split") == "development"]
    holdout = [row for row in registry if row.get("dataset_split") == "holdout"]
    other = [row for row in registry if row.get("dataset_split") not in {"development", "holdout"}]
    if other:
        raise SystemExit(
            "Every planned article needs dataset_split=development or holdout: "
            + ", ".join(row["citation_key"] for row in other[:10])
        )
    if args.pilot + args.calibration > len(development):
        raise SystemExit("pilot + calibration exceeds the development article count.")

    ordered = balanced_order(development, args.strata)
    plan: list[dict[str, str]] = []
    for index, row in enumerate(ordered, 1):
        if index <= args.pilot:
            phase, batch_id = "pilot", "pilot"
        elif index <= args.pilot + args.calibration:
            phase, batch_id = "calibration", "calibration"
        else:
            scale_index = index - args.pilot - args.calibration - 1
            phase = "scale"
            batch_id = f"scale_{scale_index // args.batch_size + 1:02d}"
        plan.append({
            "citation_key": row["citation_key"],
            "dataset_split": "development",
            "incremental_phase": phase,
            "batch_id": batch_id,
            "batch_order": str(index),
            "stratum": row["_stratum"],
            "codebook_version": "",
            "coding_status": "planned",
        })
    for index, row in enumerate(sorted(holdout, key=lambda r: r["citation_key"]), 1):
        plan.append({
            "citation_key": row["citation_key"],
            "dataset_split": "holdout",
            "incremental_phase": "holdout",
            "batch_id": "holdout",
            "batch_order": str(index),
            "stratum": " | ".join(row.get(field, "").strip() or "unknown" for field in args.strata),
            "codebook_version": "",
            "coding_status": "planned",
        })
    fields = [
        "citation_key", "dataset_split", "incremental_phase", "batch_id",
        "batch_order", "stratum", "codebook_version", "coding_status",
    ]
    write_csv(args.output, plan, fields)
    batch_counts: dict[str, int] = defaultdict(int)
    for row in plan:
        batch_counts[row["batch_id"]] += 1
    print(f"Wrote {args.output}")
    print(f"Development={len(development)} Holdout={len(holdout)}")
    print("Batches: " + ", ".join(f"{key}={batch_counts[key]}" for key in sorted(batch_counts)))


def row_key(row: dict[str, str]) -> tuple[str, str, str]:
    return row["citation_key"], row["module"], row["paragraph_id"]


def normalized(row: dict[str, str], fields: list[str]) -> tuple[str, ...]:
    return tuple(row.get(field, "") for field in fields)


def cmd_merge(args: argparse.Namespace) -> None:
    root = args.root.expanduser().resolve()
    plan_path = args.plan or root / "01_registry" / "incremental_batch_plan.csv"
    registry_path = root / "01_registry" / "corpus_registry.csv"
    cumulative_path = root / "04_style_analysis" / "cumulative" / "paragraph_move_coding.csv"
    stats_dir = root / "04_style_analysis" / "cumulative" / "statistics"
    packet_dir = root / "04_style_analysis" / "guide_versions" / "delta_packets"
    packet_dir.mkdir(parents=True, exist_ok=True)

    plan = read_csv(plan_path)
    plan_by_key = {row["citation_key"]: row for row in plan}
    batch = read_csv(args.batch_coding)
    if not batch:
        raise SystemExit("Batch coding file is empty.")
    missing = REQUIRED_CODING - set(batch[0])
    if missing:
        raise SystemExit(f"Batch coding missing columns: {sorted(missing)}")

    batch_article_keys = {row["citation_key"] for row in batch}
    invalid = sorted(
        key for key in batch_article_keys
        if key not in plan_by_key
        or plan_by_key[key].get("dataset_split") != "development"
        or plan_by_key[key].get("batch_id") != args.batch_id
    )
    if invalid:
        raise SystemExit(
            "Batch contains unplanned, holdout, or wrong-batch articles: "
            + ", ".join(invalid)
        )

    existing = read_csv(cumulative_path) if cumulative_path.exists() else []
    existing_versions = {row.get("codebook_version", "") for row in existing}
    existing_versions.discard("")
    if existing_versions and existing_versions != {args.codebook_version}:
        raise SystemExit(
            f"Codebook mismatch: cumulative={sorted(existing_versions)}, "
            f"incoming={args.codebook_version}. Run a documented migration first."
        )

    fields = list(existing[0]) if existing else list(batch[0])
    for field in ("codebook_version", "batch_id"):
        if field not in fields:
            fields.append(field)
    existing_by_key = {row_key(row): row for row in existing}
    duplicates_inside: set[tuple[str, str, str]] = set()
    seen_batch: set[tuple[str, str, str]] = set()
    added = 0
    unchanged = 0
    for raw in batch:
        row = dict(raw)
        row["codebook_version"] = args.codebook_version
        row["batch_id"] = args.batch_id
        key = row_key(row)
        if key in seen_batch:
            duplicates_inside.add(key)
            continue
        seen_batch.add(key)
        if key in existing_by_key:
            old = existing_by_key[key]
            if normalized(old, fields) != normalized(row, fields):
                raise SystemExit(f"Conflicting existing paragraph row: {key}")
            unchanged += 1
        else:
            existing_by_key[key] = row
            added += 1
    if duplicates_inside:
        raise SystemExit(f"Duplicate paragraph keys inside batch: {sorted(duplicates_inside)[:10]}")

    merged = sorted(
        existing_by_key.values(),
        key=lambda r: (
            r["citation_key"], r["module"],
            int(r["paragraph_position"].split("/", 1)[0]),
            r["paragraph_id"],
        ),
    )
    write_csv(cumulative_path, merged, fields)

    analyzer = Path(__file__).with_name("analyze_move_coding.py")
    subprocess.run(
        [
            sys.executable, str(analyzer), "--coding", str(cumulative_path),
            "--registry", str(registry_path), "--output", str(stats_dir),
        ],
        check=True,
    )
    digest = hashlib.sha256(cumulative_path.read_bytes()).hexdigest()
    cumulative_articles = len({row["citation_key"] for row in merged})
    packet = packet_dir / f"{args.batch_id}_guide_delta_packet.md"
    packet.write_text(
        "\n".join([
            f"# Guide delta packet: {args.batch_id}",
            "",
            f"- Codebook version: {args.codebook_version}",
            f"- Incoming articles: {len(batch_article_keys)}",
            f"- Added paragraph rows: {added}",
            f"- Unchanged rows on rerun: {unchanged}",
            f"- Cumulative development articles: {cumulative_articles}",
            f"- Cumulative paragraph rows: {len(merged)}",
            f"- Cumulative coding SHA-256: {digest}",
            "",
            "## Inputs for the next guide decision",
            "",
            f"- Cumulative coding: {cumulative_path}",
            f"- Current coverage: {stats_dir / 'move_article_coverage.csv'}",
            f"- Current transitions: {stats_dir / 'move_sequence_transitions.csv'}",
            "- Previous checkpoint statistics: supply the last frozen snapshot",
            "- New-batch QA summary: supply low-confidence and adjudication results",
            "- Current style guide and codebook: supply frozen versions",
            "",
            "## Decision rule",
            "",
            "Update only rules with a tier crossing, material order/transition change, "
            "stable method-specific variant, or contradiction. Otherwise update "
            "denominators or record no material change. Do not load historical prose.",
            "",
        ]) + "\n",
        encoding="utf-8",
    )
    print(f"Merged batch {args.batch_id}: added={added}, unchanged={unchanged}")
    print(f"Cumulative articles={cumulative_articles}, paragraphs={len(merged)}")
    print(f"Delta packet: {packet}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    plan = sub.add_parser("plan", help="Create a deterministic balanced batch plan")
    plan.add_argument("--registry", required=True, type=Path)
    plan.add_argument("--output", required=True, type=Path)
    plan.add_argument("--pilot", type=int, default=12)
    plan.add_argument("--calibration", type=int, default=28)
    plan.add_argument("--batch-size", type=int, default=20)
    plan.add_argument("--strata", nargs="+", default=["method_group", "article_type"])
    plan.set_defaults(func=cmd_plan)

    merge = sub.add_parser("merge", help="Merge one coded batch and update statistics")
    merge.add_argument("--root", required=True, type=Path)
    merge.add_argument("--batch-coding", required=True, type=Path)
    merge.add_argument("--batch-id", required=True)
    merge.add_argument("--codebook-version", required=True)
    merge.add_argument("--plan", type=Path)
    merge.set_defaults(func=cmd_merge)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if getattr(args, "pilot", 0) < 0 or getattr(args, "calibration", 0) < 0:
        raise SystemExit("pilot and calibration counts cannot be negative.")
    if getattr(args, "batch_size", 1) <= 0:
        raise SystemExit("batch-size must be positive.")
    args.func(args)


if __name__ == "__main__":
    main()
