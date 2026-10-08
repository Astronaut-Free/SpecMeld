#!/usr/bin/env python3
from pathlib import Path
import argparse
from datetime import date
import re
import subprocess
import sys

try:
    import tomllib
except ImportError:
    print("Python 3.11+ required for tomllib", file=sys.stderr)
    raise SystemExit(2)

VALID_COVERAGE = {"APPLICABLE", "NOT_APPLICABLE", "DEFERRED", "UNKNOWN"}
COVERAGE_KEYS = {
    "product_ux", "architecture_code", "data_storage", "api_integration",
    "runtime_infrastructure", "security_supply_chain", "quality_delivery",
    "reliability_operations", "organization_change", "conditional",
}
STAGE_ORDER = {
    "G0_INTENT_STABLE": 0,
    "G1_BUILD_READY": 1,
    "G2_INTEGRATION_READY": 2,
    "G3_RELEASE_READY": 3,
    "G4_OPERABLE_HANDOVER_READY": 4,
}
PACK_STATUS = {"NOT_COMPILED", "DRAFT", "DEVELOPMENT_READY", "STALE", "CONVERGED"}
PROFILES = {"nano", "lite", "standard", "critical"}
COLLAB_MODES = {"single", "multi-human", "multi-agent", "hybrid"}
COLLAB_PROVIDERS = {"github", "gitlab", "gitee", "local"}
GOVERNANCE_DEFAULTS = {"auto", "L1", "L2", "L3"}
GOVERNANCE_LEVELS = {"L1", "L2", "L3"}
AUTHORITY_STATUSES = {"NOT_ASSESSED", "ALIGNED", "DRIFT_REPAIRED", "AMENDMENT_REQUIRED", "CONFLICT", "UNKNOWN"}
REALITY_AUDIT_STATES = {"NOT_APPLICABLE", "REQUIRED", "PASS", "BLOCKED"}
READINESS_RE = re.compile(r"<!--\s*sps:readiness=(DRAFT|READY|STALE)\s*-->")
PLACEHOLDERS = {
    "REPLACE_ME", "__PROJECT_NAME__", "__MODE__", "__PROFILE__", "__ARCHETYPE__",
    "<WP path>", "<linked spec/lld>", "<contract/schema if needed>", "<WP DAG>",
}
SECRET_PATTERNS = {
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{8,}\b"),
    "API secret key": re.compile(r"\bsk-[A-Za-z0-9_-]{8,}"),
    "api_key assignment": re.compile(r"(?i)\bapi[_-]?key\s*=\s*[^\s#]+"),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|BEGIN PRIVATE KEY"),
    "password assignment": re.compile(r"(?i)\bpassword\s*=\s*[^\s#]+"),
}
PLACEHOLDER_ONLY_RE = re.compile(r"(?i)^(?:tbd|todo|tbc|n/?a|none|null|placeholder|replace[_ -]?me|待定|占位|暂无|\.{3})$")
VERIFIABLE_RE = re.compile(
    r"(?i)\b(?:pytest|unittest|python\s+-m|npm\s+(?:test|run)|pnpm|yarn|go\s+test|cargo\s+test|mvn|gradle|make|curl|docker|contract|schema|migration|artifact|endpoint|snapshot|benchmark|test|tests|eval|evidence|pass|output|file)\b|测试|验收|产物|接口|命令|通过|可验证"
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def readiness(path: Path) -> str | None:
    if not path.exists():
        return None
    m = READINESS_RE.search(read_text(path))
    return m.group(1) if m else None


def check_placeholders(path: Path) -> list[str]:
    if not path.exists():
        return []
    text = read_text(path)
    return sorted(p for p in PLACEHOLDERS if p in text)


def metadata_value(text: str, key: str) -> str:
    m = re.search(rf"(?mi)^[ \t]*{re.escape(key)}[ \t]*:[ \t]*([^\r\n]*)$", text)
    return m.group(1).strip().strip("`\"'") if m else ""


def owner_present(path: Path) -> bool:
    return bool(metadata_value(read_text(path), "owner"))


def heading_sections(text: str) -> list[tuple[str, str]]:
    lines = text.splitlines()
    headings: list[tuple[int, int, str]] = []
    for i, line in enumerate(lines):
        m = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if m:
            headings.append((i, len(m.group(1)), m.group(2).strip()))
    result: list[tuple[str, str]] = []
    for n, (start, level, title) in enumerate(headings):
        end = len(lines)
        for next_start, next_level, _ in headings[n + 1:]:
            if next_level <= level:
                end = next_start
                break
        result.append((title, "\n".join(lines[start + 1:end]).strip()))
    return result


def section_body(text: str, title_terms: tuple[str, ...]) -> str | None:
    for title, body in heading_sections(text):
        t = title.lower()
        if any(term.lower() in t for term in title_terms):
            return body
    return None


def meaningful_lines(body: str) -> list[str]:
    out: list[str] = []
    for raw in body.splitlines():
        line = raw.strip()
        if not line or line.startswith("<!--") or line.startswith("```"):
            continue
        if re.fullmatch(r"\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?", line):
            continue
        cleaned = re.sub(r"^[\-*>#|\s]+|[|\s]+$", "", line).strip()
        if not cleaned:
            continue
        if PLACEHOLDER_ONLY_RE.fullmatch(cleaned) or (cleaned.startswith("<") and cleaned.endswith(">")):
            continue
        # Empty metadata/bullet labels are not content.
        if re.fullmatch(r"[A-Za-z0-9 _/()\-]+:\s*", cleaned):
            continue
        out.append(cleaned)
    return out


def acceptance_is_empty(path: Path) -> bool:
    text = read_text(path)
    body = section_body(text, ("acceptance criteria", "验收标准"))
    if body is not None:
        return not meaningful_lines(body)
    if "acceptance" in path.name.lower():
        table_rows = []
        for line in text.splitlines():
            s = line.strip()
            if not s.startswith("|"):
                continue
            if re.fullmatch(r"\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?", s):
                continue
            table_rows.append(s)
        # One row is normally the header; two or more means at least one data row.
        if len(table_rows) >= 2:
            return False
        return not meaningful_lines(text)
    return False


def wp_done_is_verifiable(path: Path) -> bool:
    text = read_text(path)
    body = section_body(text, ("done condition", "## done", "完成条件"))
    if body is None:
        # Exact heading helper above strips hashes, so match plain title as fallback.
        for title, candidate in heading_sections(text):
            if title.strip().lower() in {"done", "done condition"} or "完成条件" in title:
                body = candidate
                break
    if not body:
        return False
    if "```" in body or re.search(r"`[^`]+`", body):
        return True
    return bool(VERIFIABLE_RE.search(body))


def adr_has_options(path: Path) -> bool:
    text = read_text(path)
    body = section_body(text, ("options considered", "alternatives", "options", "备选", "候选方案"))
    if body is None:
        return False
    rows = []
    bullets = []
    for line in body.splitlines():
        s = line.strip()
        if s.startswith("|") and not re.fullmatch(r"\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?", s):
            rows.append(s)
        if re.match(r"^[-*+]\s+\S", s):
            bullets.append(s)
    return len(rows) >= 2 or bool(bullets)


def table_has_data(text: str, title_terms: tuple[str, ...]) -> bool:
    body = section_body(text, title_terms)
    if body is None:
        return False
    rows = []
    for line in body.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        if re.fullmatch(r"\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?", s):
            continue
        rows.append(s)
    # header + at least one data row
    return len(rows) >= 2


def physical_audit_has_evidence(path: Path) -> bool:
    text = read_text(path)
    return any([
        table_has_data(text, ("physical reality matrix",)),
        table_has_data(text, ("permission matrix",)),
        table_has_data(text, ("transaction matrix",)),
    ])


def secret_hits(root: Path) -> list[str]:
    candidates = [root / "PROJECT.toml"]
    for dirname in ("docs", "contracts"):
        base = root / dirname
        if base.exists():
            candidates.extend(p for p in base.rglob("*") if p.is_file())
    hits: list[str] = []
    for path in candidates:
        if not path.exists() or not path.is_file():
            continue
        text = read_text(path)
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                try:
                    rel = path.relative_to(root)
                except ValueError:
                    rel = path
                hits.append(f"possible secret in {Path(rel).as_posix()}: {label}")
    return sorted(set(hits))


def git_head(root: Path) -> str | None:
    cp = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], text=True, capture_output=True, check=False)
    return cp.stdout.strip() if cp.returncode == 0 else None


def git_commits_since(root: Path, old_sha: str) -> int | None:
    cp = subprocess.run(
        ["git", "-C", str(root), "rev-list", "--count", f"{old_sha}..HEAD"],
        text=True,
        capture_output=True,
        check=False,
    )
    if cp.returncode != 0:
        return None
    try:
        return int(cp.stdout.strip())
    except ValueError:
        return None


def report(stage: str, issues: list[str], warnings: list[str]) -> None:
    if issues:
        print("FAIL")
        for item in issues:
            print("-", item)
    else:
        print(f"PASS declared-stage structural/readiness checks ({stage})")
        print("NOTE PASS is not proof of functional correctness, deployment success, or production acceptance.")
    if warnings:
        print("WARNINGS")
        for item in warnings:
            print("-", item)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check project control-plane and declared-stage structural readiness.")
    parser.add_argument("project_root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    issues: list[str] = []
    warnings: list[str] = []

    project_file = root / "PROJECT.toml"
    if not project_file.exists():
        issues.append("missing PROJECT.toml")
        report("UNKNOWN", issues, warnings)
        return 1

    try:
        data = tomllib.loads(read_text(project_file))
    except Exception as exc:
        issues.append(f"invalid PROJECT.toml: {exc}")
        report("UNKNOWN", issues, warnings)
        return 1

    stage = data.get("stage", "")
    stage_level = STAGE_ORDER.get(stage)
    if stage_level is None:
        issues.append(f"unknown stage: {stage}")
        stage_level = 0

    if str(data.get("name", "")).strip() in {"", "REPLACE_ME", "__PROJECT_NAME__"}:
        issues.append("project name is unset")

    for hit in secret_hits(root):
        issues.append(hit)

    governance = data.get("governance", {})
    governance_default = governance.get("default_level", "auto")
    if governance_default not in GOVERNANCE_DEFAULTS:
        issues.append(f"governance.default_level invalid: {governance_default}")
    progressive = governance.get("progressive", True)
    if not isinstance(progressive, bool):
        issues.append("governance.progressive must be boolean")

    profile = data.get("profile", "standard")
    if profile == "nano":
        truth_rel = str(data.get("truth", {}).get("project", "")).strip()
        if not truth_rel:
            issues.append("nano profile requires truth.project")
        elif not (root / truth_rel).exists():
            issues.append(f"nano truth.project target missing: {truth_rel}")
        report(stage, issues, warnings)
        return 1 if issues else 0

    if profile not in PROFILES:
        issues.append(f"invalid profile: {profile}")

    standard = str(data.get("standard", ""))
    if not standard.startswith("software-project-standardizer/"):
        warnings.append(f"unexpected standard identifier: {standard or '<missing>'}")

    truth = data.get("truth", {})
    truth_paths: dict[str, Path] = {}
    for key in ["product", "system", "delivery"]:
        rel = truth.get(key)
        if not rel:
            issues.append(f"truth.{key} missing")
            continue
        p = root / rel
        truth_paths[key] = p
        if not p.exists():
            issues.append(f"truth.{key} target missing: {rel}")

    cov = data.get("coverage", {})
    notes = data.get("coverage_notes", {})
    missing = COVERAGE_KEYS - set(cov)
    if missing:
        issues.append("coverage keys missing: " + ", ".join(sorted(missing)))
    for key in COVERAGE_KEYS:
        status = cov.get(key)
        if status is None:
            continue
        if status not in VALID_COVERAGE:
            issues.append(f"coverage.{key} invalid status: {status}")
            continue
        note = str(notes.get(key, "")).strip()
        if status in {"NOT_APPLICABLE", "DEFERRED", "UNKNOWN"} and not note:
            issues.append(f"coverage.{key}={status} requires coverage_notes.{key}")
        if status == "DEFERRED":
            lower = note.lower()
            missing_fields = [x for x in ("owner=", "trigger=", "target=") if x not in lower]
            if missing_fields:
                msg = f"coverage.{key}=DEFERRED should record owner=..., trigger=..., target=..."
                (issues if stage_level >= 1 else warnings).append(msg)

    unknowns = data.get("unknowns", {}).get("items", [])
    if not isinstance(unknowns, list):
        issues.append("unknowns.items must be an array")
    elif unknowns:
        if stage_level >= 1:
            issues.append("G1+ cannot keep blocking unknowns.items: " + "; ".join(map(str, unknowns[:8])))
        else:
            warnings.append(f"G0 has {len(unknowns)} unresolved blocking unknown(s)")

    exceptions = data.get("exception", [])
    if exceptions and not isinstance(exceptions, list):
        issues.append("[[exception]] must parse as an array of tables")
    if isinstance(exceptions, list):
        required = ["id", "reason", "owner", "risk", "expires", "compensating_control"]
        for idx, exc in enumerate(exceptions, start=1):
            missing_fields = [k for k in required if not str(exc.get(k, "")).strip()]
            if missing_fields:
                msg = f"exception[{idx}] missing: {', '.join(missing_fields)}"
                (issues if stage_level >= 1 else warnings).append(msg)
                continue
            try:
                expiry = date.fromisoformat(str(exc["expires"]))
            except ValueError:
                msg = f"exception[{idx}].expires must be YYYY-MM-DD"
                (issues if stage_level >= 1 else warnings).append(msg)
            else:
                if expiry < date.today():
                    issues.append(f"exception[{idx}] expired on {expiry.isoformat()}")

    if stage_level >= 1:
        critical_unknown = [
            k for k in [
                "product_ux", "architecture_code", "data_storage", "api_integration",
                "runtime_infrastructure", "security_supply_chain", "quality_delivery", "organization_change",
            ] if cov.get(k) == "UNKNOWN"
        ]
        if critical_unknown:
            issues.append("G1+ cannot keep critical coverage UNKNOWN: " + ", ".join(critical_unknown))

        owners = data.get("owners", {})
        for owner in ["product", "engineering"]:
            if not str(owners.get(owner, "")).strip():
                issues.append(f"G1+ owner missing: {owner}")
        if stage_level >= 3 and not str(owners.get("release", "")).strip():
            issues.append("G3+ owner missing: release")
        if stage_level >= 4 and data.get("lifecycle") in {"production", "maintained"} and not str(owners.get("operations", "")).strip():
            issues.append("G4 production/maintained project owner missing: operations")

    if stage_level >= 3 and not str(data.get("release", {}).get("uat_signed_by", "")).strip():
        issues.append("G3+ requires release.uat_signed_by human UAT sign-off")

    pack = data.get("engineering_pack", {})
    pack_status = pack.get("status", "NOT_COMPILED")
    if pack_status not in PACK_STATUS:
        issues.append(f"engineering_pack.status invalid: {pack_status}")

    core_pack_paths: dict[str, Path] = {}
    if stage_level >= 1:
        if pack_status not in {"DEVELOPMENT_READY", "CONVERGED"}:
            issues.append(f"G1+ requires engineering_pack.status DEVELOPMENT_READY or CONVERGED, got {pack_status}")
        if stage_level >= 3 and pack_status != "CONVERGED":
            issues.append(f"G3+ requires engineering_pack.status CONVERGED, got {pack_status}")

        for key in ["index", "entry", "plan", "acceptance"]:
            rel = pack.get(key)
            if not rel:
                issues.append(f"engineering_pack.{key} missing")
                continue
            p = root / rel
            core_pack_paths[key] = p
            if not p.exists():
                issues.append(f"engineering_pack.{key} target missing: {rel}")

        required_ready = list(truth_paths.values()) + list(core_pack_paths.values())
        for p in required_ready:
            if not p.exists():
                continue
            r = readiness(p)
            if r is None:
                issues.append(f"G1+ required file missing sps:readiness marker: {p.relative_to(root)}")
            elif r != "READY":
                issues.append(f"G1+ required file not READY: {p.relative_to(root)} ({r})")
            placeholders = check_placeholders(p)
            if placeholders:
                issues.append(f"G1+ unresolved template placeholders in {p.relative_to(root)}: {', '.join(placeholders)}")

        work_dir = root / data.get("artifact_paths", {}).get("work", "docs/engineering/work")
        work_packets = sorted(work_dir.glob("WP-*.md")) if work_dir.exists() else []
        if not work_packets:
            issues.append("G1+ requires at least one compiled Work Packet in artifact_paths.work")
        index_path = core_pack_paths.get("index")
        if index_path and index_path.exists():
            index_text = read_text(index_path)
            for wp in work_packets:
                rel = str(wp.relative_to(root)).replace("\\", "/")
                if wp.name not in index_text and rel not in index_text:
                    warnings.append(f"Work Packet not indexed in ENGINEERING_INDEX: {rel}")

    mode = data.get("mode")
    if mode == "brownfield" and stage_level >= 1 and not str(pack.get("baseline_sha", "")).strip():
        issues.append("brownfield G1+ requires engineering_pack.baseline_sha from verified repository reality")

    collab = data.get("collaboration", {})
    collab_mode = collab.get("mode", "single")
    provider = collab.get("provider", "github")
    if collab_mode not in COLLAB_MODES:
        issues.append(f"collaboration.mode invalid: {collab_mode}")
    if provider not in COLLAB_PROVIDERS:
        issues.append(f"collaboration.provider invalid: {provider}")
    if stage_level >= 1 and collab_mode != "single":
        for key in ["merge_authority", "integration_strategy", "work_isolation"]:
            if not str(collab.get(key, "")).strip():
                issues.append(f"G1+ multi-actor project requires collaboration.{key}")

    if mode == "client" and stage_level >= 4:
        handover_rel = truth.get("handover")
        if not handover_rel:
            issues.append("client G4 requires truth.handover")
        else:
            hp = root / handover_rel
            if not hp.exists():
                issues.append(f"handover target missing: {handover_rel}")
            elif readiness(hp) != "READY":
                issues.append(f"client G4 handover must be READY: {handover_rel}")

    native = data.get("native_truth", {})
    for domain, paths in native.items():
        if not isinstance(paths, list):
            warnings.append(f"native_truth.{domain} should be an array")
            continue
        for rel in paths:
            if rel and not (root / rel).exists():
                warnings.append(f"native truth path not found yet: {rel}")

    artifact_paths = data.get("artifact_paths", {})
    if stage_level >= 1:
        for key in ["engineering_specs", "lld", "work", "acceptance", "contracts", "schemas"]:
            rel = artifact_paths.get(key)
            if not rel:
                issues.append(f"G1+ artifact_paths.{key} missing")
            elif not (root / rel).exists():
                issues.append(f"G1+ artifact path missing: {rel}")

    # Deterministic semantic heuristics. These never claim business correctness.
    product_path = truth_paths.get("product")
    if product_path and product_path.exists() and acceptance_is_empty(product_path):
        warnings.append(f"acceptance criteria section is empty or placeholder-only: {product_path.relative_to(root)}")
    acceptance_path = core_pack_paths.get("acceptance")
    if acceptance_path and acceptance_path.exists() and acceptance_is_empty(acceptance_path):
        warnings.append(f"acceptance artifact is empty or placeholder-only: {acceptance_path.relative_to(root)}")

    spec_dir = root / artifact_paths.get("engineering_specs", "docs/engineering/specs")
    if spec_dir.exists():
        for spec in sorted(spec_dir.glob("*.md")):
            if not owner_present(spec):
                issues.append(f"Engineering Spec missing owner: {spec.relative_to(root)}")

    work_dir = root / artifact_paths.get("work", "docs/engineering/work")
    if work_dir.exists():
        for wp in sorted(work_dir.glob("WP-*.md")):
            wp_text = read_text(wp)
            if not owner_present(wp):
                issues.append(f"Work Packet missing owner: {wp.relative_to(root)}")
            wp_governance = metadata_value(wp_text, "governance_level")
            if not wp_governance:
                warnings.append(f"Work Packet missing governance_level; right-size controls before execution: {wp.relative_to(root)}")
            elif wp_governance not in GOVERNANCE_LEVELS:
                issues.append(f"Work Packet invalid governance_level {wp_governance}: {wp.relative_to(root)}")
            if not wp_done_is_verifiable(wp):
                warnings.append(f"Work Packet Done Condition lacks executable command or verifiable artifact: {wp.relative_to(root)}")

    changes_dir = root / artifact_paths.get("changes", "changes")
    if changes_dir.exists():
        for change in sorted(changes_dir.glob("*.md")):
            change_text = read_text(change)
            level = metadata_value(change_text, "governance_level")
            if level and level not in GOVERNANCE_LEVELS:
                issues.append(f"Change invalid governance_level {level}: {change.relative_to(root)}")

    lld_dir = root / artifact_paths.get("lld", "docs/engineering/lld")
    if lld_dir.exists():
        for lld in sorted(lld_dir.glob("*.md")):
            lld_text = read_text(lld)
            if not owner_present(lld):
                issues.append(f"LLD missing owner: {lld.relative_to(root)}")
            level = metadata_value(lld_text, "governance_level")
            if level and level not in GOVERNANCE_LEVELS:
                issues.append(f"LLD invalid governance_level {level}: {lld.relative_to(root)}")
            if mode == "brownfield" and stage_level >= 1 and level in {"L2", "L3"}:
                authority = metadata_value(lld_text, "authority_status")
                reality = metadata_value(lld_text, "physical_reality_audit")
                if authority not in AUTHORITY_STATUSES:
                    issues.append(f"Brownfield {level} LLD requires valid authority_status: {lld.relative_to(root)}")
                elif authority in {"NOT_ASSESSED", "AMENDMENT_REQUIRED", "CONFLICT", "UNKNOWN"}:
                    issues.append(f"Brownfield {level} LLD authority is unresolved ({authority}): {lld.relative_to(root)}")
                if reality not in REALITY_AUDIT_STATES:
                    issues.append(f"Brownfield {level} LLD requires valid physical_reality_audit: {lld.relative_to(root)}")
                elif reality in {"REQUIRED", "BLOCKED"}:
                    issues.append(f"Brownfield {level} LLD physical reality audit not cleared ({reality}): {lld.relative_to(root)}")
                elif reality == "PASS" and not physical_audit_has_evidence(lld):
                    issues.append(f"Brownfield {level} LLD claims physical reality PASS without matrix evidence: {lld.relative_to(root)}")

    decisions_dir = root / artifact_paths.get("decisions", "decisions")
    if decisions_dir.exists():
        for adr in sorted(decisions_dir.glob("ADR-*.md")):
            if not adr_has_options(adr):
                warnings.append(f"ADR has no alternatives/options list: {adr.relative_to(root)}")

    head = git_head(root)
    entry_path = core_pack_paths.get("entry")
    if head and entry_path and entry_path.exists():
        entry_baseline = metadata_value(read_text(entry_path), "baseline_sha")
        if entry_baseline and entry_baseline.lower() not in {"greenfield", "n/a", "na", "not_applicable"}:
            if not head.startswith(entry_baseline) and not entry_baseline.startswith(head):
                warnings.append(f"IMPLEMENTATION_ENTRY baseline_sha differs from current git HEAD: {entry_baseline} != {head}")

    last_converged = str(pack.get("last_converged_sha", "")).strip()
    if head and last_converged:
        count = git_commits_since(root, last_converged)
        if count is None:
            warnings.append(f"engineering_pack.last_converged_sha is not resolvable in current git history: {last_converged}")
        elif count > 50:
            warnings.append(f"documentation convergence is stale: last_converged_sha is {count} commits behind current HEAD")

    eng_root = root / pack.get("root", "docs/engineering")
    if eng_root.exists():
        md_files = list(eng_root.rglob("*.md"))
        thin = []
        for p in md_files:
            try:
                if len(read_text(p).strip()) < 120:
                    thin.append(str(p.relative_to(root)))
            except Exception:
                pass
        if thin:
            warnings.append("engineering pack has very thin files; remove unused placeholders: " + ", ".join(thin[:8]))
        if len(md_files) > 35:
            warnings.append(f"engineering pack has {len(md_files)} markdown files; verify the project truly needs this many")

    report(stage, issues, warnings)
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
