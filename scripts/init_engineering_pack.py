#!/usr/bin/env python3
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

ROOT = Path(__file__).resolve().parents[1]
T = ROOT / "templates"
CORE = {
    "docs/engineering/ENGINEERING_INDEX.md": T / "ENGINEERING_INDEX.md",
    "docs/engineering/IMPLEMENTATION_ENTRY.md": T / "IMPLEMENTATION_ENTRY.md",
    "docs/engineering/IMPLEMENTATION_PLAN.md": T / "IMPLEMENTATION_PLAN.md",
    "docs/engineering/acceptance/ACCEPTANCE.md": T / "ACCEPTANCE.md",
}


def toml_literal(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def set_scalar(text: str, section: str, key: str, value: str) -> str:
    """Set one scalar key inside a TOML section; fail loudly if structure is unexpected."""
    lines = text.splitlines()
    in_section = False
    hits = 0
    section_re = re.compile(r"^\s*\[([^\]]+)\]\s*$")
    key_re = re.compile(rf"^(\s*{re.escape(key)}\s*=\s*)([^#]*?)(\s*(?:#.*)?)$")

    for i, line in enumerate(lines):
        sm = section_re.match(line)
        if sm:
            in_section = sm.group(1).strip() == section
            continue
        if in_section:
            km = key_re.match(line)
            if km:
                lines[i] = f"{km.group(1)}{toml_literal(value)}{km.group(3)}"
                hits += 1
    if hits != 1:
        raise ValueError(f"expected exactly one [{section}].{key}, found {hits}")
    rendered = "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    tomllib.loads(rendered)
    return rendered


def main() -> int:
    p = argparse.ArgumentParser(description="Create minimal Engineering Pack control files after product intent is sufficiently stable.")
    p.add_argument("project_root", nargs="?", default=".")
    args = p.parse_args()
    dst = Path(args.project_root).resolve()
    project_file = dst / "PROJECT.toml"
    if not project_file.exists():
        raise SystemExit("PROJECT.toml missing; initialize the project control plane first")

    initial_data = tomllib.loads(project_file.read_text(encoding="utf-8"))
    if initial_data.get("profile") == "nano":
        print("SKIP nano profile does not use the full Engineering Pack; keep PROJECT.toml + docs/PROJECT.md as the merged truth.")
        return 0

    for rel, src in CORE.items():
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            print(f"SKIP {rel} (exists)")
            continue
        target.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"CREATE {rel}")

    for rel in ["docs/engineering/specs", "docs/engineering/lld", "docs/engineering/work", "contracts", "schemas"]:
        (dst / rel).mkdir(parents=True, exist_ok=True)

    text = project_file.read_text(encoding="utf-8")
    data = tomllib.loads(text)
    current = data.get("engineering_pack", {}).get("status", "NOT_COMPILED")
    if current == "NOT_COMPILED":
        text = set_scalar(text, "engineering_pack", "status", "DRAFT")
        project_file.write_text(text, encoding="utf-8")
        print("UPDATE PROJECT.toml engineering_pack.status -> DRAFT")
    else:
        print(f"KEEP engineering_pack.status={current}")

    print("READY engineering pack control files created; specialized specs/LLDs/WPs must be compiled from project needs, not bulk-scaffolded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
