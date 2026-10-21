#!/usr/bin/env python3
"""Machine metrics for eval runs. Judgment metrics come from rubric.md.

Usage: python evals/score.py runs/<case>/with-1 runs/<case>/without-1 ...
Each argument is a project directory produced by one run. Directories whose
name starts with "with" and "without" are summarised separately.
"""
from __future__ import annotations

from pathlib import Path
import json
import subprocess
import sys

DOCTOR = Path(__file__).resolve().parents[1] / "scripts" / "doctor.py"


def metrics(project: Path) -> dict:
    out: dict = {"run": project.name}
    if not (project / "PROJECT.toml").exists():
        out.update(verdict="NO_PROJECT", stage="-", issues=0, warnings=0, pack_files=0, wps=0, ac_total=0, ac_mapped="-")
        return out
    cp = subprocess.run([sys.executable, str(DOCTOR), str(project), "--format", "json"], text=True, capture_output=True)
    try:
        rep = json.loads(cp.stdout)
    except json.JSONDecodeError:
        out.update(verdict="DOCTOR_ERROR", stage="-", issues=0, warnings=0, pack_files=0, wps=0, ac_total=0, ac_mapped="-")
        return out
    eng = project / "docs" / "engineering"
    wps = rep.get("facts", {}).get("work_packets", {})
    acs = set(rep.get("facts", {}).get("acceptance_ids", []))
    orphan_msgs = [w["message"] for w in rep["warnings"] if w["code"] == "ACCEPTANCE_ORPHAN"]
    orphans = {tok.strip(" ,") for m in orphan_msgs for tok in m.split(":", 1)[-1].split(",")}
    out.update(
        verdict=rep["verdict"],
        stage=rep["stage"],
        issues=len(rep["issues"]),
        warnings=len(rep["warnings"]),
        pack_files=len(list(eng.rglob("*.md"))) if eng.exists() else 0,
        wps=len(wps),
        ac_total=len(acs),
        ac_mapped=f"{len(acs - orphans)}/{len(acs)}" if acs else "-",
    )
    return out


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    rows = [metrics(Path(a)) for a in argv if Path(a).is_dir()]
    cols = ["run", "verdict", "stage", "issues", "warnings", "pack_files", "wps", "ac_total", "ac_mapped"]
    widths = {c: max(len(c), *(len(str(r[c])) for r in rows)) for c in cols}
    print(" | ".join(c.ljust(widths[c]) for c in cols))
    print("-|-".join("-" * widths[c] for c in cols))
    for r in rows:
        print(" | ".join(str(r[c]).ljust(widths[c]) for c in cols))
    for arm in ("with", "without"):
        arm_rows = [r for r in rows if r["run"].startswith(arm + "-") or r["run"] == arm]
        if arm_rows:
            passed = sum(r["verdict"] == "PASS" for r in arm_rows)
            avg_files = sum(r["pack_files"] for r in arm_rows) / len(arm_rows)
            print(f"\n{arm}: {passed}/{len(arm_rows)} doctor PASS, mean pack files {avg_files:.1f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
