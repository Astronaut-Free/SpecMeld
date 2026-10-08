#!/usr/bin/env python3
from pathlib import Path
import argparse
import json
import sys

try:
    import tomllib
except ImportError:
    print("Python 3.11+ required for tomllib", file=sys.stderr)
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parents[1]
T = ROOT / "templates"

STANDARD_CORE = {
    "PROJECT.toml": T / "PROJECT.toml",
    "docs/PRODUCT.md": T / "PRODUCT.md",
    "docs/SYSTEM.md": T / "SYSTEM.md",
    "docs/DELIVERY.md": T / "DELIVERY.md",
}
NANO_CORE = {
    "PROJECT.toml": T / "PROJECT.toml",
    "docs/PROJECT.md": T / "PROJECT.md",
}

TOKENS = {
    "__PROJECT_NAME__": "name",
    "__MODE__": "mode",
    "__PROFILE__": "profile",
    "__ARCHETYPE__": "archetype",
}


def toml_string_content(value: str) -> str:
    """Return JSON/TOML-basic-string compatible content without outer quotes."""
    return json.dumps(value, ensure_ascii=False)[1:-1]


def render_project_template(text: str, values: dict[str, str]) -> str:
    rendered = text
    for token, key in TOKENS.items():
        if token not in rendered:
            raise ValueError(f"required template token missing: {token}")
        rendered = rendered.replace(token, toml_string_content(values[key]))
    leftovers = [t for t in TOKENS if t in rendered]
    if leftovers:
        raise ValueError("unresolved template tokens: " + ", ".join(leftovers))
    tomllib.loads(rendered)
    return rendered


def main() -> int:
    p = argparse.ArgumentParser(description="Initialize the minimal Software Project Standardizer control plane.")
    p.add_argument("project_root", nargs="?", default=".")
    p.add_argument("--name", required=True)
    p.add_argument("--mode", choices=["greenfield", "brownfield", "client"], default="greenfield")
    p.add_argument("--profile", choices=["nano", "lite", "standard", "critical"], default="standard")
    p.add_argument(
        "--archetype",
        choices=["web", "mobile", "mini-program", "api", "saas", "ai", "data", "platform", "library", "internal", "custom"],
        default="custom",
    )
    args = p.parse_args()

    dst = Path(args.project_root).resolve()
    dst.mkdir(parents=True, exist_ok=True)
    values = {"name": args.name, "mode": args.mode, "profile": args.profile, "archetype": args.archetype}
    core = NANO_CORE if args.profile == "nano" else STANDARD_CORE

    for rel, src in core.items():
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            print(f"SKIP {rel} (exists)")
            continue
        content = src.read_text(encoding="utf-8")
        if rel == "PROJECT.toml":
            content = render_project_template(content, values)
        target.write_text(content, encoding="utf-8")
        print(f"CREATE {rel}")

    if args.profile != "nano":
        (dst / "changes").mkdir(exist_ok=True)
        (dst / "decisions").mkdir(exist_ok=True)
        print(f"READY minimal control plane created for mode={args.mode}; no extra documents generated.")
        if args.mode == "brownfield":
            print("NEXT brownfield compiler must run Reality Scan before G1; initializer intentionally does not create empty analysis docs.")
    else:
        print("READY nano control plane created: PROJECT.toml + docs/PROJECT.md only; full Engineering Pack is intentionally skipped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
