#!/usr/bin/env python3
"""Migrate v1.0–1.1 Work Packets (line metadata) to the 1.2 TOML frontmatter format.

Dry-run by default; pass --write to modify files. Files that already start with
`+++` frontmatter are skipped. The migration is mechanical: it never invents
commands, paths or approvals. Anything it cannot extract is left empty so that
`doctor.py` reports it as a gap instead of hiding it.
"""
from __future__ import annotations

from pathlib import Path
import argparse
import json
import re
import sys

try:
    import tomllib
except ImportError:
    print("Python 3.11+ required for tomllib", file=sys.stderr)
    raise SystemExit(2)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from doctor import (  # noqa: E402
    AC_ID_RE, BACKTICK_RE, LEGACY_RISK, WP_ID_RE, normalize_risk, path_like, section_body,
)

SCALAR_KEYS = [
    "status", "owner", "timebox", "issue_ref", "integrator", "change",
    "branch_or_worktree", "base_branch", "baseline_sha", "final_sha", "pr",
]
LIST_KEYS = ["affected_surface"]
APPROVAL_KEYS = ["authored_by", "approved_by"]
MOVED_KEYS = set(SCALAR_KEYS + LIST_KEYS + APPROVAL_KEYS + ["governance_level", "risk_level", "depends_on", "dependencies", "parallel_safe_with"])
META_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)[ \t]*:[ \t]*(.*)$")


def toml_value(value) -> str:
    if isinstance(value, list):
        return "[" + ", ".join(json.dumps(v, ensure_ascii=False) for v in value) + "]"
    return json.dumps(value, ensure_ascii=False)


def clean_enum(value: str) -> str:
    """Template enum lists like `PLANNED | READY` are not a value."""
    return "" if "|" in value else value.strip().strip("`\"'")


def migrate_text(text: str, path: Path, authored_by: str = "") -> tuple[str, dict]:
    lines = text.splitlines()
    title_line_idx = next((i for i, l in enumerate(lines) if l.startswith("# ")), None)
    first_section = next((i for i, l in enumerate(lines) if l.startswith("## ")), len(lines))
    meta: dict[str, str] = {}
    moved_idx: set[int] = set()
    for i in range(0, first_section):
        m = META_RE.match(lines[i].strip())
        if m and m.group(1) in MOVED_KEYS:
            meta[m.group(1)] = m.group(2).strip()
            moved_idx.add(i)

    stem = WP_ID_RE.search(path.name)
    wp_id = stem.group(0) if stem else path.stem
    title = ""
    if title_line_idx is not None:
        title = re.sub(r"^#\s*(WP-\d+\s*[:：]\s*)?", "", lines[title_line_idx]).strip()

    data: dict = {"id": wp_id, "title": title}
    for key in SCALAR_KEYS:
        v = clean_enum(meta.get(key, ""))
        if v:
            data[key] = v
    raw_risk = clean_enum(meta.get("risk_level", "") or meta.get("governance_level", ""))
    level, _ = normalize_risk(raw_risk)
    data["risk_level"] = level or ""
    for key in LIST_KEYS:
        v = clean_enum(meta.get(key, ""))
        data[key] = [x.strip() for x in v.split(",") if x.strip()] if v else []

    deps_sec = section_body(text, ("dependencies", "依赖")) or ""
    deps_src = meta.get("depends_on", "") + " " + meta.get("dependencies", "") + "\n" + deps_sec
    data["depends_on"] = sorted(set(WP_ID_RE.findall(deps_src)) - {wp_id})
    data["parallel_safe_with"] = sorted(set(WP_ID_RE.findall(meta.get("parallel_safe_with", ""))) - {wp_id})

    def paths_in(titles: tuple[str, ...]) -> list[str]:
        sec = section_body(text, titles) or ""
        return [t for t in BACKTICK_RE.findall(sec) if path_like(t)]

    data["read_set"] = paths_in(("read set",))
    data["write_set"] = paths_in(("write set",))
    data["acceptance_refs"] = sorted(set(AC_ID_RE.findall(text)))

    done_sec = section_body(text, ("done condition", "完成条件")) or section_body(text, ("done",), exact=True) or ""
    tokens = BACKTICK_RE.findall(done_sec)
    commands = [t for t in tokens if " " in t.strip()]
    artifacts = [t for t in tokens if t not in commands and path_like(t)]

    out = ["+++"]
    for key in ["id", "title", "status", "owner", "risk_level", "affected_surface", "depends_on",
                "parallel_safe_with", "read_set", "write_set", "acceptance_refs"]:
        out.append(f"{key} = {toml_value(data.get(key, '' if key not in ('affected_surface',) else []))}")
    for key in SCALAR_KEYS:
        if key in data and key not in ("status", "owner"):
            out.append(f"{key} = {toml_value(data[key])}")
    out += ["", "[done]", f"commands = {toml_value(commands)}", f"artifacts = {toml_value(artifacts)}"]
    out += ["", "[approval]",
            f"authored_by = {toml_value(clean_enum(meta.get('authored_by', '')) or authored_by)}",
            f"approved_by = {toml_value(clean_enum(meta.get('approved_by', '')))}",
            "+++"]
    fm = "\n".join(out)
    tomllib.loads("\n".join(out[1:-1]))  # validate before writing anything

    body = [l for i, l in enumerate(lines) if i not in moved_idx]
    # Collapse blank lines left behind by moved metadata directly under the title.
    collapsed: list[str] = []
    for l in body:
        if not l.strip() and collapsed and not collapsed[-1].strip():
            continue
        collapsed.append(l)
    new_text = fm + "\n\n" + "\n".join(collapsed).strip() + "\n"
    report = {
        "risk_level": data["risk_level"] or "<unset>",
        "legacy_risk": raw_risk if raw_risk in LEGACY_RISK else "",
        "read_set": len(data["read_set"]),
        "write_set": len(data["write_set"]),
        "done_commands": len(commands),
        "done_artifacts": len(artifacts),
    }
    return new_text, report


def main() -> int:
    ap = argparse.ArgumentParser(description="Migrate legacy Work Packets to 1.2 TOML frontmatter.")
    ap.add_argument("paths", nargs="+", help="WP files or directories (directories are searched for WP-*.md)")
    ap.add_argument("--write", action="store_true", help="write changes (default: dry run)")
    ap.add_argument("--authored-by", default="", help="record who compiled these WPs (enables independent-approval checks)")
    args = ap.parse_args()

    files: list[Path] = []
    for p in map(Path, args.paths):
        files.extend(sorted(p.rglob("WP-*.md")) if p.is_dir() else [p])
    changed = 0
    for f in files:
        text = f.read_text(encoding="utf-8")
        if text.startswith("+++"):
            print(f"SKIP {f} (already frontmatter)")
            continue
        new_text, info = migrate_text(text, f, args.authored_by)
        changed += 1
        summary = ", ".join(f"{k}={v}" for k, v in info.items() if v not in ("", 0))
        print(f"{'WRITE' if args.write else 'WOULD WRITE'} {f}: {summary}")
        if args.write:
            f.write_text(new_text, encoding="utf-8")
    if not args.write and changed:
        print("DRY RUN: re-run with --write to apply. Then run doctor.py and fill the gaps it reports "
              "(empty read/write sets, [done] commands, approval for R2/R3).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
