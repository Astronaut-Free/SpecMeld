#!/usr/bin/env python3
"""SpecMeld doctor: deterministic control-plane and declared-stage readiness gate.

PASS means the machine-checkable constraints for the declared stage hold.
It never proves business correctness, deployment success or production acceptance.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from fnmatch import fnmatch
from pathlib import Path
import argparse
import json
import re
import subprocess
import sys

try:
    import tomllib
except ImportError:
    print("Python 3.11+ required for tomllib", file=sys.stderr)
    raise SystemExit(2)

DOCTOR_VERSION = "1.2.0"

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
RISK_LEVELS = {"R1", "R2", "R3"}
LEGACY_RISK = {"L1": "R1", "L2": "R2", "L3": "R3"}
RISK_DEFAULTS = {"auto"} | RISK_LEVELS | set(LEGACY_RISK)
AUTHORITY_STATUSES = {"NOT_ASSESSED", "ALIGNED", "DRIFT_REPAIRED", "AMENDMENT_REQUIRED", "CONFLICT", "UNKNOWN"}
REALITY_AUDIT_STATES = {"NOT_APPLICABLE", "REQUIRED", "PASS", "BLOCKED"}
WP_STATUSES = {
    "PLANNED", "READY", "IN_PROGRESS", "BUILT", "VERIFIED",
    "INTEGRATION_READY", "INTEGRATED", "DONE", "BLOCKED",
}
WP_INACTIVE = {"PLANNED", "BLOCKED"}
WP_FINISHED = {"INTEGRATED", "DONE"}
READINESS_RE = re.compile(r"<!--\s*sps:readiness=(DRAFT|READY|STALE)\b[^>]*-->")
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
# Blocking checks introduced in 1.2.0. In compat mode ("1.1") they are reported as warnings so
# projects already at G1 can upgrade first and close the gaps on a schedule.
NEW_IN_1_2_BLOCKING = {
    "WP_DEPENDENCY_UNKNOWN", "WP_DEPENDENCY_CYCLE", "WP_DONE_UNVERIFIABLE", "WP_READ_SET_UNRESOLVED",
    "WP_ACCEPTANCE_REF_UNKNOWN", "WP_APPROVAL_MISSING", "WP_SELF_APPROVED", "WP_PARALLEL_WRITE_OVERLAP",
    "WP_NONE_READY", "NATIVE_TRUTH_MISSING", "ENTRY_CURRENT_WP_MISSING", "PACK_APPROVAL_MISSING", "PACK_SELF_APPROVED",
}
WP_ID_RE = re.compile(r"\bWP-\d{3,}\b")
AC_ID_RE = re.compile(r"\bAC-\d{2,}\b")
BACKTICK_RE = re.compile(r"`([^`\n]+)`")
TABLE_SEP_RE = re.compile(r"\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?")
GLOB_CHARS = set("*?[")

# Surface keywords used only for advisory risk-consistency warnings.
R3_SURFACE = re.compile(r"(?i)identity|permission|authz|authn|\bauth\b|rbac|tenant isolation|release control|secret|payment|canonical authority")
R2_SURFACE = re.compile(r"(?i)schema|migration|shared contract|public api|openapi|asyncapi|proto|canonical|core runtime|event contract")
R2_PATH = re.compile(r"(?i)(^|/)(schemas?|migrations?|contracts?)/|\.sql$|openapi|asyncapi|\.proto$")


# --------------------------------------------------------------------------- report

@dataclass
class Report:
    stage: str = "UNKNOWN"
    issues: list[dict] = field(default_factory=list)
    warnings: list[dict] = field(default_factory=list)
    facts: dict = field(default_factory=dict)
    compat: str | None = None

    def issue(self, code: str, message: str) -> None:
        if self.compat == "1.1" and code in NEW_IN_1_2_BLOCKING:
            self.warnings.append({"code": code, "message": f"(compat 1.1: would block in 1.2) {message}"})
            return
        self.issues.append({"code": code, "message": message})

    def warn(self, code: str, message: str) -> None:
        self.warnings.append({"code": code, "message": message})

    def gate(self, blocking: bool, code: str, message: str) -> None:
        (self.issue if blocking else self.warn)(code, message)

    def verdict(self, strict: bool) -> str:
        if self.issues:
            return "FAIL"
        if strict and self.warnings:
            return "FAIL"
        return "PASS"

    def emit(self, fmt: str, strict: bool) -> int:
        verdict = self.verdict(strict)
        if fmt == "json":
            print(json.dumps({
                "doctor_version": DOCTOR_VERSION,
                "stage": self.stage,
                "verdict": verdict,
                "strict": strict,
                "issues": self.issues,
                "warnings": self.warnings,
                "facts": self.facts,
                "note": "PASS is not proof of functional correctness, deployment success, or production acceptance.",
            }, ensure_ascii=False, indent=2))
        else:
            if self.issues:
                print("FAIL")
                for item in self.issues:
                    print(f"- [{item['code']}] {item['message']}")
            elif verdict == "FAIL":
                print("FAIL (strict: warnings are blocking)")
            else:
                print(f"PASS declared-stage structural/readiness checks ({self.stage})")
                print("NOTE PASS is not proof of functional correctness, deployment success, or production acceptance.")
            if self.warnings:
                print("WARNINGS")
                for item in self.warnings:
                    print(f"- [{item['code']}] {item['message']}")
        return 0 if verdict == "PASS" else 1


# --------------------------------------------------------------------------- text helpers

def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def rel(root: Path, path: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


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
    in_fence = False
    for i, line in enumerate(lines):
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
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


def section_body(text: str, title_terms: tuple[str, ...], exact: bool = False) -> str | None:
    for title, body in heading_sections(text):
        t = title.lower().strip()
        if exact:
            if t in {term.lower() for term in title_terms}:
                return body
        elif any(term.lower() in t for term in title_terms):
            return body
    return None


def meaningful_lines(body: str) -> list[str]:
    out: list[str] = []
    for raw in body.splitlines():
        line = raw.strip()
        if not line or line.startswith("<!--") or line.startswith("```"):
            continue
        if TABLE_SEP_RE.fullmatch(line):
            continue
        cleaned = re.sub(r"^[\-*>#|\s]+|[|\s]+$", "", line).strip()
        if not cleaned:
            continue
        if PLACEHOLDER_ONLY_RE.fullmatch(cleaned) or (cleaned.startswith("<") and cleaned.endswith(">")):
            continue
        if re.fullmatch(r"[A-Za-z0-9 _/()\-]+:\s*", cleaned):
            continue
        out.append(cleaned)
    return out


def table_rows(body: str) -> list[str]:
    rows = []
    for line in body.splitlines():
        s = line.strip()
        if s.startswith("|") and not TABLE_SEP_RE.fullmatch(s):
            rows.append(s)
    return rows


def acceptance_is_empty(path: Path) -> bool:
    text = read_text(path)
    body = section_body(text, ("acceptance criteria", "验收标准"))
    if body is not None:
        return not meaningful_lines(body)
    if "acceptance" in path.name.lower():
        if len(table_rows(text)) >= 2:
            return False
        return not meaningful_lines(text)
    return False


def adr_has_options(path: Path) -> bool:
    body = section_body(read_text(path), ("options considered", "alternatives", "options", "备选", "候选方案"))
    if body is None:
        return False
    bullets = [s for s in (l.strip() for l in body.splitlines()) if re.match(r"^[-*+]\s+\S", s)]
    return len(table_rows(body)) >= 2 or bool(bullets)


def table_has_data(text: str, title_terms: tuple[str, ...]) -> bool:
    body = section_body(text, title_terms)
    return body is not None and len(table_rows(body)) >= 2


def physical_audit_has_evidence(path: Path) -> bool:
    text = read_text(path)
    return any(table_has_data(text, (t,)) for t in ("physical reality matrix", "permission matrix", "transaction matrix"))


def normalize_risk(value: str) -> tuple[str | None, bool]:
    """Return (R-level or None, used_legacy_alias)."""
    v = str(value or "").strip().split()[0] if str(value or "").strip() else ""
    if v in RISK_LEVELS:
        return v, False
    if v in LEGACY_RISK:
        return LEGACY_RISK[v], True
    return None, False


# --------------------------------------------------------------------------- work packets

@dataclass
class WorkPacket:
    path: Path
    id: str
    legacy: bool
    status: str = ""
    owner: str = ""
    risk: str | None = None
    risk_raw: str = ""
    risk_legacy_alias: bool = False
    affected_surface: list[str] = field(default_factory=list)
    depends_on: list[str] = field(default_factory=list)
    parallel_safe_with: list[str] = field(default_factory=list)
    read_set: list[str] = field(default_factory=list)
    write_set: list[str] = field(default_factory=list)
    acceptance_refs: list[str] = field(default_factory=list)
    done_commands: list[str] = field(default_factory=list)
    done_artifacts: list[str] = field(default_factory=list)
    done_text: str = ""
    authored_by: str = ""
    approved_by: str = ""
    parse_error: str = ""

    @property
    def active(self) -> bool:
        return self.status not in WP_INACTIVE

    @property
    def done_verifiable(self) -> bool:
        if self.done_commands or self.done_artifacts:
            return True
        if not self.legacy:
            # Structured WPs are judged only by [done]; prose in the body cannot substitute for it.
            return False
        # Legacy fallback: an inline command/path or a fenced block. Prose like "tests pass" is not enough.
        return "```" in self.done_text or bool(BACKTICK_RE.search(self.done_text))


def split_frontmatter(text: str) -> tuple[str | None, str]:
    if not text.startswith("+++"):
        return None, text
    lines = text.splitlines()
    if lines[0].strip() != "+++":
        return None, text
    for i in range(1, len(lines)):
        if lines[i].strip() == "+++":
            return "\n".join(lines[1:i]), "\n".join(lines[i + 1:])
    return None, text


def as_list(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [v.strip() for v in re.split(r"[,\n]", value) if v.strip()]
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    return [str(value)]


def path_like(token: str) -> bool:
    t = token.strip()
    if " " in t or not t or t.startswith(("http://", "https://")):
        return False
    return "/" in t or bool(re.search(r"\.[A-Za-z0-9]{1,6}$", t))


def legacy_section_paths(body: str, titles: tuple[str, ...]) -> list[str]:
    sec = section_body(body, titles)
    if not sec:
        return []
    return [m for m in BACKTICK_RE.findall(sec) if path_like(m)]


def load_wp(path: Path) -> WorkPacket:
    text = read_text(path)
    stem_id = WP_ID_RE.search(path.name)
    default_id = stem_id.group(0) if stem_id else path.stem
    fm, body = split_frontmatter(text)
    if fm is not None:
        wp = WorkPacket(path=path, id=default_id, legacy=False)
        try:
            data = tomllib.loads(fm)
        except Exception as exc:  # noqa: BLE001 - surface parser message
            wp.parse_error = str(exc)
            return wp
        wp.id = str(data.get("id", default_id)).strip() or default_id
        wp.status = str(data.get("status", "")).strip()
        wp.owner = str(data.get("owner", "")).strip()
        raw = data.get("risk_level") or data.get("governance_level") or ""
        wp.risk_raw = str(raw)
        wp.risk, wp.risk_legacy_alias = normalize_risk(wp.risk_raw)
        if "governance_level" in data and "risk_level" not in data:
            wp.risk_legacy_alias = True
        wp.affected_surface = as_list(data.get("affected_surface"))
        wp.depends_on = as_list(data.get("depends_on"))
        wp.parallel_safe_with = as_list(data.get("parallel_safe_with"))
        wp.read_set = as_list(data.get("read_set"))
        wp.write_set = as_list(data.get("write_set"))
        wp.acceptance_refs = as_list(data.get("acceptance_refs"))
        done = data.get("done", {}) if isinstance(data.get("done", {}), dict) else {}
        wp.done_commands = as_list(done.get("commands"))
        wp.done_artifacts = as_list(done.get("artifacts"))
        wp.done_text = section_body(body, ("done condition", "完成条件")) or section_body(body, ("done",), exact=True) or ""
        approval = data.get("approval", {}) if isinstance(data.get("approval", {}), dict) else {}
        wp.authored_by = str(approval.get("authored_by", "")).strip()
        wp.approved_by = str(approval.get("approved_by", "")).strip()
        return wp

    # Legacy (v1.0–1.1) line metadata.
    wp = WorkPacket(path=path, id=default_id, legacy=True)
    wp.status = metadata_value(text, "status").split("|")[0].strip()
    wp.owner = metadata_value(text, "owner")
    wp.risk_raw = metadata_value(text, "risk_level") or metadata_value(text, "governance_level")
    wp.risk, wp.risk_legacy_alias = normalize_risk(wp.risk_raw)
    if metadata_value(text, "governance_level") and not metadata_value(text, "risk_level"):
        wp.risk_legacy_alias = True
    wp.affected_surface = as_list(metadata_value(text, "affected_surface"))
    deps_line = metadata_value(text, "depends_on") or metadata_value(text, "dependencies")
    deps_sec = section_body(text, ("dependencies", "依赖")) or ""
    wp.depends_on = sorted(set(WP_ID_RE.findall(deps_line + "\n" + deps_sec)) - {wp.id})
    wp.parallel_safe_with = WP_ID_RE.findall(metadata_value(text, "parallel_safe_with"))
    wp.read_set = legacy_section_paths(text, ("read set",))
    wp.write_set = legacy_section_paths(text, ("write set",))
    wp.acceptance_refs = sorted(set(AC_ID_RE.findall(text)))
    wp.done_text = section_body(text, ("done condition", "完成条件")) or section_body(text, ("done",), exact=True) or ""
    wp.authored_by = metadata_value(text, "authored_by")
    wp.approved_by = metadata_value(text, "approved_by")
    return wp


def static_prefix(pattern: str) -> str:
    out = []
    for part in pattern.split("/"):
        if any(c in GLOB_CHARS for c in part):
            break
        out.append(part)
    return "/".join(out)


def has_glob(pattern: str) -> bool:
    return any(c in GLOB_CHARS for c in pattern)


def patterns_overlap(a: str, b: str) -> bool:
    a, b = a.strip().rstrip("/"), b.strip().rstrip("/")
    if not a or not b:
        return False
    if a == b or fnmatch(a, b) or fnmatch(b, a):
        return True
    pa, pb = static_prefix(a), static_prefix(b)
    if has_glob(a) and pa and (pb + "/").startswith(pa + "/"):
        return True
    if has_glob(b) and pb and (pa + "/").startswith(pb + "/"):
        return True
    # Directory written as plain path covers its children.
    if not has_glob(a) and (b + "/").startswith(a + "/"):
        return True
    if not has_glob(b) and (a + "/").startswith(b + "/"):
        return True
    return False


def path_exists(root: Path, entry: str) -> bool:
    entry = entry.strip()
    if not entry:
        return True
    if has_glob(entry):
        try:
            return any(root.glob(entry))
        except (ValueError, NotImplementedError):
            return False
    return (root / entry).exists()


def find_cycle(graph: dict[str, list[str]]) -> list[str] | None:
    WHITE, GREY, BLACK = 0, 1, 2
    color = {n: WHITE for n in graph}
    stack: list[str] = []

    def visit(n: str) -> list[str] | None:
        color[n] = GREY
        stack.append(n)
        for m in graph.get(n, []):
            if m not in color:
                continue
            if color[m] == GREY:
                return stack[stack.index(m):] + [m]
            if color[m] == WHITE:
                found = visit(m)
                if found:
                    return found
        stack.pop()
        color[n] = BLACK
        return None

    for node in sorted(graph):
        if color[node] == WHITE:
            found = visit(node)
            if found:
                return found
    return None


def ancestors(graph: dict[str, list[str]], node: str) -> set[str]:
    seen: set[str] = set()
    todo = list(graph.get(node, []))
    while todo:
        n = todo.pop()
        if n in seen or n not in graph:
            continue
        seen.add(n)
        todo.extend(graph.get(n, []))
    return seen


def topo_order(graph: dict[str, list[str]]) -> list[str]:
    order: list[str] = []
    done: set[str] = set()

    def visit(n: str) -> None:
        if n in done:
            return
        done.add(n)
        for m in sorted(graph.get(n, [])):
            if m in graph:
                visit(m)
        order.append(n)

    for n in sorted(graph):
        visit(n)
    return order


def check_work_packets(root: Path, r: Report, wps: list[WorkPacket], stage_level: int,
                       acceptance_ids: set[str], acceptance_path: Path | None) -> None:
    by_id: dict[str, WorkPacket] = {}
    for wp in wps:
        p = rel(root, wp.path)
        if wp.parse_error:
            r.issue("WP_FRONTMATTER_INVALID", f"Work Packet frontmatter is not valid TOML ({wp.parse_error}): {p}")
            continue
        if wp.id in by_id:
            r.issue("WP_DUPLICATE_ID", f"duplicate Work Packet id {wp.id}: {p} and {rel(root, by_id[wp.id].path)}")
        by_id[wp.id] = wp

    graph = {wid: [d for d in wp.depends_on if d != wid] for wid, wp in by_id.items()}
    g1 = stage_level >= 1

    for wid, wp in sorted(by_id.items()):
        p = rel(root, wp.path)
        file_id = WP_ID_RE.search(wp.path.name)
        if file_id and file_id.group(0) != wid:
            r.warn("WP_ID_MISMATCH", f"Work Packet id {wid} does not match its file name: {p}")
        if wp.legacy:
            r.warn("WP_LEGACY_FORMAT", f"Work Packet uses legacy line metadata; run scripts/migrate_wp.py to adopt TOML frontmatter: {p}")
        if not wp.owner:
            r.issue("WP_OWNER_MISSING", f"Work Packet missing owner: {p}")
        if not wp.status:
            r.warn("WP_STATUS_MISSING", f"Work Packet has no status: {p}")
        elif wp.status not in WP_STATUSES:
            r.issue("WP_STATUS_INVALID", f"Work Packet invalid status {wp.status}: {p}")
        if not wp.risk_raw:
            r.warn("WP_RISK_MISSING", f"Work Packet missing risk_level; right-size controls before execution: {p}")
        elif wp.risk is None:
            r.issue("WP_RISK_INVALID", f"Work Packet invalid risk_level {wp.risk_raw}: {p}")
        elif wp.risk_legacy_alias:
            r.warn("WP_RISK_LEGACY_ALIAS", f"governance_level {wp.risk_raw} is a deprecated alias; use risk_level = \"{wp.risk}\": {p}")

        # Dependencies.
        for dep in wp.depends_on:
            if dep not in by_id:
                r.gate(g1, "WP_DEPENDENCY_UNKNOWN", f"{wid} depends on unknown Work Packet {dep}: {p}")

        # Done condition.
        if not wp.done_verifiable:
            blocking = g1 and wp.active
            r.gate(blocking, "WP_DONE_UNVERIFIABLE",
                   f"Work Packet Done Condition lacks executable command or verifiable artifact "
                   f"(set [done].commands/artifacts or cite a backticked command/path): {p}")

        # Read set resolution: must exist now or be produced by a transitive dependency.
        dep_writes = [w for a in ancestors(graph, wid) for w in by_id[a].write_set]
        for entry in wp.read_set:
            if path_exists(root, entry):
                continue
            if any(patterns_overlap(entry, w) for w in dep_writes):
                continue
            r.gate(g1 and wp.active, "WP_READ_SET_UNRESOLVED",
                   f"{wid} read_set entry does not exist and is not produced by a dependency: {entry} ({p})")

        if not wp.legacy and wp.active and not wp.write_set:
            r.warn("WP_WRITE_SET_EMPTY", f"{wid} has no write_set; parallel safety cannot be checked: {p}")

        # Acceptance traceability.
        for ref in wp.acceptance_refs:
            if acceptance_ids and ref not in acceptance_ids:
                r.gate(g1, "WP_ACCEPTANCE_REF_UNKNOWN", f"{wid} references {ref}, which is not defined in acceptance: {p}")
        if g1 and wp.active and acceptance_ids and not wp.acceptance_refs and not wp.legacy:
            r.warn("WP_ACCEPTANCE_REFS_EMPTY", f"{wid} is active but maps to no acceptance item (acceptance_refs): {p}")

        # Risk consistency (advisory) and independent approval (blocking for R2/R3 at G1).
        surface_text = " ".join(wp.affected_surface)
        suggested = None
        if R3_SURFACE.search(surface_text):
            suggested = "R3"
        elif R2_SURFACE.search(surface_text) or any(R2_PATH.search(w) for w in wp.write_set):
            suggested = "R2"
        if wp.risk and suggested and int(suggested[1]) > int(wp.risk[1]):
            r.warn("WP_RISK_UNDERSTATED",
                   f"{wid} declares {wp.risk} but its surface/write_set suggests {suggested}; "
                   f"confirm or record the down-grade reason: {p}")
        if wp.risk in {"R2", "R3"} and wp.active and wp.status not in WP_FINISHED:
            if not wp.approved_by:
                r.gate(g1, "WP_APPROVAL_MISSING",
                       f"{wid} is {wp.risk} and {wp.status or 'unset'} but has no approval.approved_by: {p}")
            elif wp.authored_by and wp.authored_by.strip().lower() == wp.approved_by.strip().lower():
                r.gate(g1, "WP_SELF_APPROVED", f"{wid} approval.approved_by equals authored_by; {wp.risk} needs an independent approver: {p}")
            elif not wp.authored_by:
                r.warn("WP_AUTHOR_UNKNOWN", f"{wid} records approved_by but not authored_by; independence cannot be checked: {p}")

    cycle = find_cycle(graph)
    if cycle:
        r.gate(g1, "WP_DEPENDENCY_CYCLE", "Work Packet dependency cycle: " + " -> ".join(cycle))
    else:
        r.facts["wp_order"] = topo_order(graph)

    # Write-set overlap between WPs that are not ordered by the DAG.
    ids = sorted(i for i, wp in by_id.items() if wp.status not in WP_FINISHED)
    anc = {i: ancestors(graph, i) for i in ids} if not cycle else {i: set() for i in ids}
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            if b in anc[a] or a in anc[b]:
                continue
            overlap = sorted({x for x in by_id[a].write_set for y in by_id[b].write_set if patterns_overlap(x, y)})
            if not overlap:
                continue
            declared = b in by_id[a].parallel_safe_with or a in by_id[b].parallel_safe_with
            if declared:
                r.gate(g1, "WP_PARALLEL_WRITE_OVERLAP",
                       f"{a} and {b} are declared parallel_safe_with but share write_set: {', '.join(overlap)}")
            else:
                r.warn("WP_UNORDERED_WRITE_OVERLAP",
                       f"{a} and {b} have no dependency order but share write_set ({', '.join(overlap)}); "
                       f"serialize with depends_on or assign a hotspot owner")

    # Acceptance coverage.
    if g1 and acceptance_path is not None and acceptance_path.exists():
        if not acceptance_ids:
            r.warn("ACCEPTANCE_NO_IDS", f"acceptance has no stable AC-xx IDs; WP ↔ acceptance traceability cannot be checked: {rel(root, acceptance_path)}")
        else:
            referenced = {ref for wp in by_id.values() for ref in wp.acceptance_refs}
            orphans = sorted(acceptance_ids - referenced)
            if orphans:
                r.warn("ACCEPTANCE_ORPHAN", "acceptance items not mapped to any Work Packet: " + ", ".join(orphans))

    if g1:
        executable = [w for w in by_id.values() if w.status in WP_STATUSES - WP_INACTIVE]
        if by_id and not executable:
            r.issue("WP_NONE_READY", "G1+ requires at least one Work Packet in READY or a later status")
    r.facts["work_packets"] = {
        wid: {"status": wp.status, "risk_level": wp.risk, "depends_on": wp.depends_on,
              "legacy": wp.legacy, "path": rel(root, wp.path)}
        for wid, wp in sorted(by_id.items())
    }


# --------------------------------------------------------------------------- git

def git(root: Path, *args: str) -> subprocess.CompletedProcess[str] | None:
    try:
        return subprocess.run(["git", "-C", str(root), *args], text=True, capture_output=True, check=False)
    except FileNotFoundError:
        return None


def git_head(root: Path) -> str | None:
    cp = git(root, "rev-parse", "HEAD")
    return cp.stdout.strip() if cp and cp.returncode == 0 else None


def git_commits_since(root: Path, old_sha: str) -> int | None:
    cp = git(root, "rev-list", "--count", f"{old_sha}..HEAD")
    if not cp or cp.returncode != 0:
        return None
    try:
        return int(cp.stdout.strip())
    except ValueError:
        return None


def git_changed_files(root: Path, base: str) -> list[str] | None:
    top = git(root, "rev-parse", "--show-toplevel")
    if not top or top.returncode != 0:
        return None
    repo = Path(top.stdout.strip()).resolve()
    diff = git(root, "diff", "--name-only", base)
    if not diff or diff.returncode != 0:
        return None
    untracked = git(root, "ls-files", "--others", "--exclude-standard", "--full-name")
    names = diff.stdout.splitlines() + (untracked.stdout.splitlines() if untracked and untracked.returncode == 0 else [])
    out = []
    for n in names:
        absolute = (repo / n).resolve()
        try:
            out.append(absolute.relative_to(root).as_posix())
        except ValueError:
            continue
    return sorted(set(out))


def check_drift(root: Path, r: Report, data: dict, base: str) -> None:
    changed = git_changed_files(root, base)
    if changed is None:
        r.issue("DRIFT_BASE_UNRESOLVED", f"--changed-since {base}: not a git repository or ref cannot be resolved")
        return
    paths = data.get("artifact_paths", {})
    native_patterns = [p for v in data.get("native_truth", {}).values() if isinstance(v, list) for p in v if p]
    native_patterns += [paths.get("contracts", "contracts") + "/**", paths.get("schemas", "schemas") + "/**"]
    truth_roots = ["docs/", paths.get("changes", "changes") + "/", paths.get("decisions", "decisions") + "/"]
    truth_files = {str(v) for v in data.get("truth", {}).values() if v}

    def is_native(f: str) -> bool:
        return any(patterns_overlap(f, pat) for pat in native_patterns)

    native_changed = [f for f in changed if is_native(f) and not f.endswith(".gitkeep")]
    truth_changed = [f for f in changed if f in truth_files or any(f.startswith(t) for t in truth_roots)]
    r.facts["changed_since"] = {"base": base, "native_truth_changed": native_changed, "truth_changed": truth_changed}
    if native_changed and not truth_changed:
        r.issue("DRIFT_UNSYNCED_NATIVE_TRUTH",
                "native truth changed without any Truth/Spec/Change/ADR update in the same change set: "
                + ", ".join(native_changed[:10]))


# --------------------------------------------------------------------------- secrets

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
                hits.append(f"possible secret in {rel(root, path)}: {label}")
    return sorted(set(hits))


# --------------------------------------------------------------------------- main checks

def run_checks(root: Path, r: Report, changed_since: str | None) -> None:
    project_file = root / "PROJECT.toml"
    if not project_file.exists():
        r.issue("PROJECT_MISSING", "missing PROJECT.toml")
        return
    try:
        data = tomllib.loads(read_text(project_file))
    except Exception as exc:  # noqa: BLE001
        r.issue("PROJECT_INVALID", f"invalid PROJECT.toml: {exc}")
        return

    stage = data.get("stage", "")
    r.stage = stage or "UNKNOWN"
    stage_level = STAGE_ORDER.get(stage)
    if stage_level is None:
        r.issue("STAGE_UNKNOWN", f"unknown stage: {stage}")
        stage_level = 0
    g1 = stage_level >= 1

    if str(data.get("name", "")).strip() in {"", "REPLACE_ME", "__PROJECT_NAME__"}:
        r.issue("NAME_UNSET", "project name is unset")

    for hit in secret_hits(root):
        r.issue("SECRET", hit)

    if changed_since:
        check_drift(root, r, data, changed_since)

    governance = data.get("governance", {})
    compat = str(governance.get("doctor_compat", "") or "").strip() or r.compat
    if compat:
        if compat != "1.1":
            r.issue("COMPAT_INVALID", f"governance.doctor_compat supports only \"1.1\", got {compat}")
        else:
            r.compat = "1.1"
            until = str(governance.get("doctor_compat_until", "")).strip()
            try:
                expired = bool(until) and date.fromisoformat(until) < date.today()
            except ValueError:
                expired = False
                r.issue("COMPAT_UNTIL_INVALID", "governance.doctor_compat_until must be YYYY-MM-DD")
            if expired:
                r.compat = None
                r.issue("COMPAT_EXPIRED", f"governance.doctor_compat expired on {until}; 1.2 gates are now enforced")
            else:
                r.warn("COMPAT_ACTIVE", "doctor is running in 1.1 compatibility mode: new 1.2 gates are downgraded to warnings"
                       + (f" until {until}" if until else " (set doctor_compat_until to bound the transition)"))
    governance_default = str(governance.get("default_level", "auto"))
    if governance_default not in RISK_DEFAULTS:
        r.issue("RISK_DEFAULT_INVALID", f"governance.default_level invalid: {governance_default}")
    elif governance_default in LEGACY_RISK:
        r.warn("RISK_LEGACY_ALIAS", f"governance.default_level {governance_default} is a deprecated alias; use {LEGACY_RISK[governance_default]}")
    if not isinstance(governance.get("progressive", True), bool):
        r.issue("GOVERNANCE_PROGRESSIVE_TYPE", "governance.progressive must be boolean")

    profile = data.get("profile", "standard")
    if profile == "nano":
        truth_rel = str(data.get("truth", {}).get("project", "")).strip()
        if not truth_rel:
            r.issue("NANO_TRUTH_MISSING", "nano profile requires truth.project")
        elif not (root / truth_rel).exists():
            r.issue("NANO_TRUTH_MISSING", f"nano truth.project target missing: {truth_rel}")
        return

    if profile not in PROFILES:
        r.issue("PROFILE_INVALID", f"invalid profile: {profile}")

    standard = str(data.get("standard", ""))
    if not standard.startswith("software-project-standardizer/"):
        r.warn("STANDARD_ID", f"unexpected standard identifier: {standard or '<missing>'}")

    truth = data.get("truth", {})
    truth_paths: dict[str, Path] = {}
    for key in ["product", "system", "delivery"]:
        rp = truth.get(key)
        if not rp:
            r.issue("TRUTH_MISSING", f"truth.{key} missing")
            continue
        p = root / rp
        truth_paths[key] = p
        if not p.exists():
            r.issue("TRUTH_MISSING", f"truth.{key} target missing: {rp}")

    cov = data.get("coverage", {})
    notes = data.get("coverage_notes", {})
    missing = COVERAGE_KEYS - set(cov)
    if missing:
        r.issue("COVERAGE_KEYS", "coverage keys missing: " + ", ".join(sorted(missing)))
    for key in sorted(COVERAGE_KEYS):
        status = cov.get(key)
        if status is None:
            continue
        if status not in VALID_COVERAGE:
            r.issue("COVERAGE_STATUS", f"coverage.{key} invalid status: {status}")
            continue
        note = str(notes.get(key, "")).strip()
        if status in {"NOT_APPLICABLE", "DEFERRED", "UNKNOWN"} and not note:
            r.issue("COVERAGE_NOTE", f"coverage.{key}={status} requires coverage_notes.{key}")
        if status == "DEFERRED":
            lower = note.lower()
            if [x for x in ("owner=", "trigger=", "target=") if x not in lower]:
                r.gate(g1, "COVERAGE_DEFERRED", f"coverage.{key}=DEFERRED should record owner=..., trigger=..., target=...")

    unknowns = data.get("unknowns", {}).get("items", [])
    if not isinstance(unknowns, list):
        r.issue("UNKNOWNS_TYPE", "unknowns.items must be an array")
    elif unknowns:
        if g1:
            r.issue("UNKNOWNS_BLOCKING", "G1+ cannot keep blocking unknowns.items: " + "; ".join(map(str, unknowns[:8])))
        else:
            r.warn("UNKNOWNS_BLOCKING", f"G0 has {len(unknowns)} unresolved blocking unknown(s)")

    exceptions = data.get("exception", [])
    if exceptions and not isinstance(exceptions, list):
        r.issue("EXCEPTION_TYPE", "[[exception]] must parse as an array of tables")
    if isinstance(exceptions, list):
        required = ["id", "reason", "owner", "risk", "expires", "compensating_control"]
        for idx, exc in enumerate(exceptions, start=1):
            missing_fields = [k for k in required if not str(exc.get(k, "")).strip()]
            if missing_fields:
                r.gate(g1, "EXCEPTION_FIELDS", f"exception[{idx}] missing: {', '.join(missing_fields)}")
                continue
            try:
                expiry = date.fromisoformat(str(exc["expires"]))
            except ValueError:
                r.gate(g1, "EXCEPTION_EXPIRES", f"exception[{idx}].expires must be YYYY-MM-DD")
            else:
                if expiry < date.today():
                    r.issue("EXCEPTION_EXPIRED", f"exception[{idx}] expired on {expiry.isoformat()}")

    owners = data.get("owners", {})
    if g1:
        critical_unknown = [
            k for k in [
                "product_ux", "architecture_code", "data_storage", "api_integration",
                "runtime_infrastructure", "security_supply_chain", "quality_delivery", "organization_change",
            ] if cov.get(k) == "UNKNOWN"
        ]
        if critical_unknown:
            r.issue("COVERAGE_CRITICAL_UNKNOWN", "G1+ cannot keep critical coverage UNKNOWN: " + ", ".join(critical_unknown))
        for owner in ["product", "engineering"]:
            if not str(owners.get(owner, "")).strip():
                r.issue("OWNER_MISSING", f"G1+ owner missing: {owner}")
        if stage_level >= 3 and not str(owners.get("release", "")).strip():
            r.issue("OWNER_MISSING", "G3+ owner missing: release")
        if stage_level >= 4 and data.get("lifecycle") in {"production", "maintained"} and not str(owners.get("operations", "")).strip():
            r.issue("OWNER_MISSING", "G4 production/maintained project owner missing: operations")

    if stage_level >= 3 and not str(data.get("release", {}).get("uat_signed_by", "")).strip():
        r.issue("UAT_SIGNOFF_MISSING", "G3+ requires release.uat_signed_by human UAT sign-off")

    pack = data.get("engineering_pack", {})
    pack_status = pack.get("status", "NOT_COMPILED")
    if pack_status not in PACK_STATUS:
        r.issue("PACK_STATUS_INVALID", f"engineering_pack.status invalid: {pack_status}")

    core_pack_paths: dict[str, Path] = {}
    artifact_paths = data.get("artifact_paths", {})
    if g1:
        if pack_status not in {"DEVELOPMENT_READY", "CONVERGED"}:
            r.issue("PACK_NOT_READY", f"G1+ requires engineering_pack.status DEVELOPMENT_READY or CONVERGED, got {pack_status}")
        if stage_level >= 3 and pack_status != "CONVERGED":
            r.issue("PACK_NOT_CONVERGED", f"G3+ requires engineering_pack.status CONVERGED, got {pack_status}")

        # Readiness is attested by someone other than the compiler for high-rigor profiles.
        approver = str(pack.get("approved_by", "")).strip()
        compiler = str(pack.get("compiled_by", "")).strip()
        if not approver:
            r.gate(profile == "critical", "PACK_APPROVAL_MISSING",
                   "G1+ engineering_pack.approved_by is empty; READY markers are self-attested until a human/independent reviewer approves")
        elif compiler and compiler.lower() == approver.lower():
            r.gate(profile in {"standard", "critical"}, "PACK_SELF_APPROVED",
                   "engineering_pack.approved_by equals compiled_by; approval must be independent of the compiler")

        for key in ["index", "entry", "plan", "acceptance"]:
            rp = pack.get(key)
            if not rp:
                r.issue("PACK_PATH_MISSING", f"engineering_pack.{key} missing")
                continue
            p = root / rp
            core_pack_paths[key] = p
            if not p.exists():
                r.issue("PACK_PATH_MISSING", f"engineering_pack.{key} target missing: {rp}")

        for p in list(truth_paths.values()) + list(core_pack_paths.values()):
            if not p.exists():
                continue
            state = readiness(p)
            if state is None:
                r.issue("READINESS_MARKER_MISSING", f"G1+ required file missing sps:readiness marker: {rel(root, p)}")
            elif state != "READY":
                r.issue("READINESS_NOT_READY", f"G1+ required file not READY: {rel(root, p)} ({state})")
            placeholders = check_placeholders(p)
            if placeholders:
                r.issue("PLACEHOLDERS", f"G1+ unresolved template placeholders in {rel(root, p)}: {', '.join(placeholders)}")

        for key in ["engineering_specs", "lld", "work", "acceptance", "contracts", "schemas"]:
            rp = artifact_paths.get(key)
            if not rp:
                r.issue("ARTIFACT_PATH_MISSING", f"G1+ artifact_paths.{key} missing")
            elif not (root / rp).exists():
                r.issue("ARTIFACT_PATH_MISSING", f"G1+ artifact path missing: {rp}")

    mode = data.get("mode")
    if mode == "brownfield" and g1 and not str(pack.get("baseline_sha", "")).strip():
        r.issue("BROWNFIELD_BASELINE", "brownfield G1+ requires engineering_pack.baseline_sha from verified repository reality")

    collab = data.get("collaboration", {})
    collab_mode = collab.get("mode", "single")
    provider = collab.get("provider", "github")
    if collab_mode not in COLLAB_MODES:
        r.issue("COLLAB_MODE", f"collaboration.mode invalid: {collab_mode}")
    if provider not in COLLAB_PROVIDERS:
        r.issue("COLLAB_PROVIDER", f"collaboration.provider invalid: {provider}")
    if g1 and collab_mode != "single":
        for key in ["merge_authority", "integration_strategy", "work_isolation"]:
            if not str(collab.get(key, "")).strip():
                r.issue("COLLAB_FIELD", f"G1+ multi-actor project requires collaboration.{key}")

    if mode == "client" and stage_level >= 4:
        handover_rel = truth.get("handover")
        if not handover_rel:
            r.issue("HANDOVER", "client G4 requires truth.handover")
        else:
            hp = root / handover_rel
            if not hp.exists():
                r.issue("HANDOVER", f"handover target missing: {handover_rel}")
            elif readiness(hp) != "READY":
                r.issue("HANDOVER", f"client G4 handover must be READY: {handover_rel}")

    # Declared native truth is a design input. Missing at G1+ means the pack points at nothing.
    native = data.get("native_truth", {})
    for domain, paths in native.items():
        if not isinstance(paths, list):
            r.warn("NATIVE_TRUTH_TYPE", f"native_truth.{domain} should be an array")
            continue
        for rp in paths:
            if rp and not path_exists(root, rp):
                r.gate(g1, "NATIVE_TRUTH_MISSING", f"declared native truth not found: native_truth.{domain} -> {rp}")

    # Truth/acceptance heuristics (never claim business correctness).
    product_path = truth_paths.get("product")
    if product_path and product_path.exists() and acceptance_is_empty(product_path):
        r.warn("ACCEPTANCE_EMPTY", f"acceptance criteria section is empty or placeholder-only: {rel(root, product_path)}")
    acceptance_path = core_pack_paths.get("acceptance") or (root / pack["acceptance"] if pack.get("acceptance") else None)
    acceptance_ids: set[str] = set()
    if acceptance_path and acceptance_path.exists():
        if acceptance_is_empty(acceptance_path):
            r.warn("ACCEPTANCE_EMPTY", f"acceptance artifact is empty or placeholder-only: {rel(root, acceptance_path)}")
        acceptance_ids = set(AC_ID_RE.findall(read_text(acceptance_path)))
    r.facts["acceptance_ids"] = sorted(acceptance_ids)

    spec_dir = root / artifact_paths.get("engineering_specs", "docs/engineering/specs")
    if spec_dir.exists():
        for spec in sorted(spec_dir.glob("*.md")):
            if not owner_present(spec):
                r.issue("SPEC_OWNER_MISSING", f"Engineering Spec missing owner: {rel(root, spec)}")

    work_dir = root / artifact_paths.get("work", "docs/engineering/work")
    wps = [load_wp(p) for p in sorted(work_dir.glob("WP-*.md"))] if work_dir.exists() else []
    if g1 and not wps:
        r.issue("WP_NONE", "G1+ requires at least one compiled Work Packet in artifact_paths.work")
    check_work_packets(root, r, wps, stage_level, acceptance_ids, acceptance_path if g1 else None)

    index_path = core_pack_paths.get("index")
    if index_path and index_path.exists():
        index_text = read_text(index_path)
        for wp in wps:
            rp = rel(root, wp.path)
            if wp.path.name not in index_text and rp not in index_text:
                r.warn("WP_NOT_INDEXED", f"Work Packet not indexed in ENGINEERING_INDEX: {rp}")

    entry_path = core_pack_paths.get("entry")
    if g1 and entry_path and entry_path.exists():
        current = metadata_value(read_text(entry_path), "current_wp")
        if current:
            if not (root / current).exists():
                r.issue("ENTRY_CURRENT_WP_MISSING", f"IMPLEMENTATION_ENTRY current_wp does not exist: {current}")
        else:
            r.warn("ENTRY_CURRENT_WP_UNSET", "IMPLEMENTATION_ENTRY has no current_wp; the agent has no explicit start point")

    changes_dir = root / artifact_paths.get("changes", "changes")
    if changes_dir.exists():
        for change in sorted(changes_dir.glob("*.md")):
            text = read_text(change)
            level = metadata_value(text, "risk_level") or metadata_value(text, "governance_level")
            if level and normalize_risk(level)[0] is None and "|" not in level:
                r.issue("CHANGE_RISK_INVALID", f"Change invalid risk_level {level}: {rel(root, change)}")

    lld_dir = root / artifact_paths.get("lld", "docs/engineering/lld")
    if lld_dir.exists():
        for lld in sorted(lld_dir.glob("*.md")):
            text = read_text(lld)
            lp = rel(root, lld)
            if not owner_present(lld):
                r.issue("LLD_OWNER_MISSING", f"LLD missing owner: {lp}")
            raw = metadata_value(text, "risk_level") or metadata_value(text, "governance_level")
            level, _ = normalize_risk(raw)
            if raw and level is None and "|" not in raw:
                r.issue("LLD_RISK_INVALID", f"LLD invalid risk_level {raw}: {lp}")
            if mode == "brownfield" and g1 and level in {"R2", "R3"}:
                authority = metadata_value(text, "authority_status")
                reality = metadata_value(text, "physical_reality_audit")
                if authority not in AUTHORITY_STATUSES:
                    r.issue("LLD_AUTHORITY", f"Brownfield {level} LLD requires valid authority_status: {lp}")
                elif authority in {"NOT_ASSESSED", "AMENDMENT_REQUIRED", "CONFLICT", "UNKNOWN"}:
                    r.issue("LLD_AUTHORITY", f"Brownfield {level} LLD authority is unresolved ({authority}): {lp}")
                if reality not in REALITY_AUDIT_STATES:
                    r.issue("LLD_REALITY", f"Brownfield {level} LLD requires valid physical_reality_audit: {lp}")
                elif reality in {"REQUIRED", "BLOCKED"}:
                    r.issue("LLD_REALITY", f"Brownfield {level} LLD physical reality audit not cleared ({reality}): {lp}")
                elif reality == "PASS" and not physical_audit_has_evidence(lld):
                    r.issue("LLD_REALITY", f"Brownfield {level} LLD claims physical reality PASS without matrix evidence: {lp}")

    decisions_dir = root / artifact_paths.get("decisions", "decisions")
    if decisions_dir.exists():
        for adr in sorted(decisions_dir.glob("ADR-*.md")):
            if not adr_has_options(adr):
                r.warn("ADR_NO_OPTIONS", f"ADR has no alternatives/options list: {rel(root, adr)}")

    head = git_head(root)
    if head and entry_path and entry_path.exists():
        entry_baseline = metadata_value(read_text(entry_path), "baseline_sha")
        if entry_baseline and entry_baseline.lower() not in {"greenfield", "n/a", "na", "not_applicable"}:
            if not head.startswith(entry_baseline) and not entry_baseline.startswith(head):
                r.warn("ENTRY_BASELINE_DRIFT", f"IMPLEMENTATION_ENTRY baseline_sha differs from current git HEAD: {entry_baseline} != {head}")

    last_converged = str(pack.get("last_converged_sha", "")).strip()
    if head and last_converged:
        count = git_commits_since(root, last_converged)
        if count is None:
            r.warn("CONVERGENCE_SHA_UNRESOLVED", f"engineering_pack.last_converged_sha is not resolvable in current git history: {last_converged}")
        elif count > 50:
            r.warn("CONVERGENCE_STALE", f"documentation convergence is stale: last_converged_sha is {count} commits behind current HEAD")

    eng_root = root / pack.get("root", "docs/engineering")
    if eng_root.exists():
        md_files = list(eng_root.rglob("*.md"))
        thin = [rel(root, p) for p in md_files if len(read_text(p).strip()) < 120]
        if thin:
            r.warn("PACK_THIN_FILES", "engineering pack has very thin files; remove unused placeholders: " + ", ".join(thin[:8]))
        if len(md_files) > 35:
            r.warn("PACK_TOO_MANY_FILES", f"engineering pack has {len(md_files)} markdown files; verify the project truly needs this many")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check project control-plane and declared-stage structural readiness.")
    parser.add_argument("project_root", nargs="?", default=".")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="output format (json is for agents/CI)")
    parser.add_argument("--strict", action="store_true", help="treat warnings as blocking")
    parser.add_argument("--changed-since", metavar="GIT_REF",
                        help="fail if native truth changed since GIT_REF without a Truth/Spec/Change/ADR update (drift guard for pre-commit/CI)")
    parser.add_argument("--compat", choices=["1.1"], help="downgrade gates introduced in 1.2 to warnings (upgrade transition only)")
    parser.add_argument("--version", action="version", version=f"specmeld-doctor {DOCTOR_VERSION}")
    args = parser.parse_args(argv)
    root = Path(args.project_root).resolve()
    report = Report(compat=args.compat)
    run_checks(root, report, args.changed_since)
    return report.emit(args.format, args.strict)


if __name__ == "__main__":
    raise SystemExit(main())
