"""Behavior tests for the 1.2 G1 gate.

Each test builds a project that is wrong in one specific way and asserts on the
stable issue code from `doctor.py --format json`. Tests assert behavior, not wording.
"""
from pathlib import Path
import json
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]
DOCTOR = ROOT / "scripts" / "doctor.py"
MIGRATE = ROOT / "scripts" / "migrate_wp.py"
GOLDEN = ROOT / "examples" / "mini-ticket-triage"
EXAMPLES = sorted(p for p in (ROOT / "examples").iterdir() if (p / "PROJECT.toml").exists())


def run(*args) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, *map(str, args)], text=True, capture_output=True, check=False)


def doctor(project: Path, *flags: str) -> tuple[int, dict]:
    cp = run(DOCTOR, project, "--format", "json", *flags)
    try:
        return cp.returncode, json.loads(cp.stdout)
    except json.JSONDecodeError as exc:  # pragma: no cover - diagnostic
        raise AssertionError(f"doctor did not emit JSON: {cp.stdout}\n{cp.stderr}") from exc


def codes(report: dict, kind: str = "issues") -> set[str]:
    return {item["code"] for item in report[kind]}


def set_field(path: Path, key: str, toml_value: str) -> None:
    """Replace one top-level frontmatter key (adds it if absent)."""
    text = path.read_text(encoding="utf-8")
    fm_end = text.index("\n+++", 3)
    fm, rest = text[:fm_end], text[fm_end:]
    pattern = re.compile(rf"(?m)^{re.escape(key)}\s*=.*$")
    if pattern.search(fm):
        fm = pattern.sub(f"{key} = {toml_value}", fm, count=1)
    else:
        fm = fm.replace("+++\n", f"+++\n{key} = {toml_value}\n", 1)
    path.write_text(fm + rest, encoding="utf-8")


def set_table_field(path: Path, table: str, key: str, toml_value: str) -> None:
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(rf"(?ms)(^\[{re.escape(table)}\]\n.*?^){re.escape(key)}\s*=.*?$")
    assert pattern.search(text), (table, key)
    path.write_text(pattern.sub(lambda m: f"{m.group(1)}{key} = {toml_value}", text, count=1), encoding="utf-8")


class GateTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._td = tempfile.TemporaryDirectory()
        self.project = Path(self._td.name) / "golden"
        shutil.copytree(GOLDEN, self.project)
        self.work = self.project / "docs/engineering/work"
        self.wp1 = self.work / "WP-001.md"
        self.wp2 = self.work / "WP-002.md"

    def tearDown(self) -> None:
        self._td.cleanup()

    def assertBlocks(self, code: str, *flags: str) -> dict:
        rc, report = doctor(self.project, *flags)
        self.assertNotEqual(rc, 0, report)
        self.assertIn(code, codes(report), report)
        return report

    def assertWarns(self, code: str, *flags: str) -> dict:
        rc, report = doctor(self.project, *flags)
        self.assertEqual(rc, 0, report)
        self.assertIn(code, codes(report, "warnings"), report)
        return report


class GoldenExamplesTests(unittest.TestCase):
    def test_every_golden_example_passes_strict(self):
        self.assertGreaterEqual(len(EXAMPLES), 3)
        for ex in EXAMPLES:
            with self.subTest(example=ex.name):
                rc, report = doctor(ex, "--strict")
                self.assertEqual(rc, 0, report)
                self.assertEqual(report["warnings"], [], report)

    def test_json_report_shape_and_topological_order(self):
        rc, report = doctor(GOLDEN)
        self.assertEqual(rc, 0, report)
        self.assertEqual(report["verdict"], "PASS")
        self.assertEqual(report["stage"], "G1_BUILD_READY")
        self.assertEqual(report["facts"]["wp_order"], ["WP-001", "WP-002"])
        self.assertEqual(report["facts"]["acceptance_ids"], ["AC-01", "AC-02", "AC-03", "AC-04"])
        self.assertIn("not proof of functional correctness", report["note"])


class DagTests(GateTestCase):
    def test_dependency_cycle_blocks(self):
        set_field(self.wp1, "depends_on", '["WP-002"]')
        report = self.assertBlocks("WP_DEPENDENCY_CYCLE")
        self.assertNotIn("wp_order", report["facts"])

    def test_unknown_dependency_blocks(self):
        set_field(self.wp2, "depends_on", '["WP-001", "WP-404"]')
        self.assertBlocks("WP_DEPENDENCY_UNKNOWN")

    def test_duplicate_id_blocks(self):
        set_field(self.wp2, "id", '"WP-001"')
        self.assertBlocks("WP_DUPLICATE_ID")

    def test_invalid_frontmatter_blocks(self):
        self.wp1.write_text(self.wp1.read_text(encoding="utf-8").replace('status = "READY"', "status = READY"), encoding="utf-8")
        self.assertBlocks("WP_FRONTMATTER_INVALID")

    def test_template_id_left_unchanged_warns(self):
        set_field(self.wp2, "id", '"WP-XXX"')
        self.assertWarns("WP_ID_MISMATCH")

    def test_no_ready_work_packet_blocks(self):
        set_field(self.wp1, "status", '"PLANNED"')
        self.assertBlocks("WP_NONE_READY")


class ReadSetTests(GateTestCase):
    def test_dangling_read_set_blocks_active_wp(self):
        set_field(self.wp1, "read_set", '["docs/SYSTEM.md", "contracts/does_not_exist.yaml"]')
        self.assertBlocks("WP_READ_SET_UNRESOLVED")

    def test_read_set_may_be_produced_by_a_dependency(self):
        # WP-002 reads src/tickets/**, which only WP-001 writes. Activating WP-002 must still pass.
        set_field(self.wp2, "status", '"READY"')
        set_table_field(self.wp2, "approval", "approved_by", '"Reviewer"')
        rc, report = doctor(self.project)
        self.assertEqual(rc, 0, report)
        self.assertNotIn("WP_READ_SET_UNRESOLVED", codes(report) | codes(report, "warnings"))

    def test_read_set_not_produced_once_dependency_is_removed(self):
        set_field(self.wp2, "status", '"READY"')
        set_field(self.wp2, "depends_on", "[]")
        self.assertBlocks("WP_READ_SET_UNRESOLVED")

    def test_planned_wp_dangling_read_set_only_warns(self):
        set_field(self.wp2, "read_set", '["docs/nope.md"]')
        self.assertWarns("WP_READ_SET_UNRESOLVED")


class ParallelismTests(GateTestCase):
    def _make_unordered_overlap(self) -> None:
        set_field(self.wp2, "depends_on", "[]")
        set_field(self.wp2, "read_set", '["contracts/openapi.yaml"]')
        set_field(self.wp2, "write_set", '["src/tickets/confirm.py"]')

    def test_declared_parallel_with_overlapping_write_set_blocks(self):
        self._make_unordered_overlap()
        set_field(self.wp1, "parallel_safe_with", '["WP-002"]')
        self.assertBlocks("WP_PARALLEL_WRITE_OVERLAP")

    def test_unordered_overlap_warns(self):
        self._make_unordered_overlap()
        self.assertWarns("WP_UNORDERED_WRITE_OVERLAP")

    def test_dependency_order_makes_overlap_safe(self):
        set_field(self.wp2, "write_set", '["src/tickets/confirm.py"]')
        rc, report = doctor(self.project, "--strict")
        self.assertEqual(rc, 0, report)


class DoneAndAcceptanceTests(GateTestCase):
    def test_unverifiable_done_blocks_active_wp(self):
        set_table_field(self.wp1, "done", "commands", "[]")
        set_table_field(self.wp1, "done", "artifacts", "[]")
        self.assertBlocks("WP_DONE_UNVERIFIABLE")

    def test_unverifiable_done_on_planned_wp_only_warns(self):
        set_table_field(self.wp2, "done", "commands", "[]")
        self.assertWarns("WP_DONE_UNVERIFIABLE")

    def test_unknown_acceptance_ref_blocks(self):
        set_field(self.wp1, "acceptance_refs", '["AC-01", "AC-99"]')
        self.assertBlocks("WP_ACCEPTANCE_REF_UNKNOWN")

    def test_orphan_acceptance_item_warns(self):
        acc = self.project / "docs/engineering/acceptance/ACCEPTANCE.md"
        acc.write_text(acc.read_text(encoding="utf-8") + "| AC-05 | Export to CSV | PRODUCT | — | e2e | required |\n", encoding="utf-8")
        report = self.assertWarns("ACCEPTANCE_ORPHAN")
        self.assertTrue(any("AC-05" in w["message"] for w in report["warnings"]))


class RiskAndApprovalTests(GateTestCase):
    def test_r2_without_approver_blocks(self):
        set_table_field(self.wp1, "approval", "approved_by", '""')
        self.assertBlocks("WP_APPROVAL_MISSING")

    def test_r2_self_approval_blocks(self):
        set_table_field(self.wp1, "approval", "approved_by", '"agent:specmeld-compiler"')
        self.assertBlocks("WP_SELF_APPROVED")

    def test_finished_r2_wp_does_not_need_live_approval(self):
        set_table_field(self.wp1, "approval", "approved_by", '""')
        set_field(self.wp1, "status", '"DONE"')
        set_field(self.wp2, "status", '"READY"')
        set_table_field(self.wp2, "approval", "approved_by", '"Reviewer"')
        rc, report = doctor(self.project)
        self.assertEqual(rc, 0, report)

    def test_understated_risk_warns(self):
        # The 1.1 golden example labelled a schema + public API packet as the lowest level.
        set_field(self.wp1, "risk_level", '"R1"')
        self.assertWarns("WP_RISK_UNDERSTATED")

    def test_invalid_risk_level_blocks(self):
        set_field(self.wp1, "risk_level", '"R9"')
        self.assertBlocks("WP_RISK_INVALID")

    def test_legacy_governance_level_is_accepted_as_alias(self):
        text = self.wp1.read_text(encoding="utf-8").replace('risk_level = "R2"', 'governance_level = "L2"')
        self.wp1.write_text(text, encoding="utf-8")
        report = self.assertWarns("WP_RISK_LEGACY_ALIAS")
        self.assertEqual(report["facts"]["work_packets"]["WP-001"]["risk_level"], "R2")


class PackApprovalTests(GateTestCase):
    def _project_toml(self, old: str, new: str) -> None:
        p = self.project / "PROJECT.toml"
        text = p.read_text(encoding="utf-8")
        self.assertIn(old, text)
        p.write_text(text.replace(old, new, 1), encoding="utf-8")

    def test_missing_pack_approver_warns_for_standard_profile(self):
        self._project_toml('approved_by = "Tech Lead (example)"', 'approved_by = ""')
        self.assertWarns("PACK_APPROVAL_MISSING")

    def test_missing_pack_approver_blocks_for_critical_profile(self):
        self._project_toml('approved_by = "Tech Lead (example)"', 'approved_by = ""')
        self._project_toml('profile = "standard"', 'profile = "critical"')
        self.assertBlocks("PACK_APPROVAL_MISSING")

    def test_pack_self_approval_blocks(self):
        self._project_toml('approved_by = "Tech Lead (example)"', 'approved_by = "agent:specmeld-compiler"')
        self.assertBlocks("PACK_SELF_APPROVED")


class EntryAndNativeTruthTests(GateTestCase):
    def test_missing_native_truth_blocks_at_g1(self):
        (self.project / "contracts/openapi.yaml").unlink()
        self.assertBlocks("NATIVE_TRUTH_MISSING")

    def test_entry_current_wp_must_exist(self):
        entry = self.project / "docs/engineering/IMPLEMENTATION_ENTRY.md"
        entry.write_text(entry.read_text(encoding="utf-8").replace("work/WP-001.md", "work/WP-404.md"), encoding="utf-8")
        self.assertBlocks("ENTRY_CURRENT_WP_MISSING")


class AdversarialRegressionTests(GateTestCase):
    """The exact pack that v1.1.1 reported as PASS (G1_BUILD_READY)."""

    def test_v111_false_pass_is_now_a_fail(self):
        self.wp1.write_text(
            "# WP-001: Do stuff\nstatus: READY\nowner: x\ngovernance_level: L1\ndependencies: WP-002\n"
            "## Read Set\n`contracts/does_not_exist.yaml`\n## Done\nIt should pass.\n",
            encoding="utf-8",
        )
        self.wp2.write_text(
            "# WP-002: More stuff\nstatus: PLANNED\nowner: x\ngovernance_level: L1\ndependencies: WP-001\n"
            "## Done\nGolden eval passes.\n",
            encoding="utf-8",
        )
        (self.project / "contracts/openapi.yaml").unlink()
        report = self.assertBlocks("WP_DEPENDENCY_CYCLE")
        for code in ["WP_READ_SET_UNRESOLVED", "WP_DONE_UNVERIFIABLE", "NATIVE_TRUTH_MISSING"]:
            self.assertIn(code, codes(report))
        self.assertIn("WP_LEGACY_FORMAT", codes(report, "warnings"))

    def test_compat_mode_downgrades_new_gates_only(self):
        self.test_v111_false_pass_is_now_a_fail()
        rc, report = doctor(self.project, "--compat", "1.1")
        self.assertEqual(rc, 0, report)
        self.assertIn("COMPAT_ACTIVE", codes(report, "warnings"))
        self.assertIn("WP_DEPENDENCY_CYCLE", codes(report, "warnings"))
        # Pre-existing 1.1 gates still block in compat mode.
        p = self.project / "PROJECT.toml"
        p.write_text(p.read_text(encoding="utf-8").replace("items = []", 'items = ["decide tenant model"]'), encoding="utf-8")
        rc, report = doctor(self.project, "--compat", "1.1")
        self.assertNotEqual(rc, 0)
        self.assertIn("UNKNOWNS_BLOCKING", codes(report))

    def test_expired_compat_mode_blocks(self):
        p = self.project / "PROJECT.toml"
        p.write_text(p.read_text(encoding="utf-8").replace(
            "progressive = true", 'progressive = true\ndoctor_compat = "1.1"\ndoctor_compat_until = "2020-01-01"'), encoding="utf-8")
        self.assertBlocks("COMPAT_EXPIRED")


class StrictModeTests(GateTestCase):
    def test_strict_turns_warnings_into_failure(self):
        set_field(self.wp1, "risk_level", '"R1"')
        rc, _ = doctor(self.project)
        self.assertEqual(rc, 0)
        rc, report = doctor(self.project, "--strict")
        self.assertNotEqual(rc, 0)
        self.assertEqual(report["verdict"], "FAIL")
        self.assertEqual(report["issues"], [])


@unittest.skipUnless(shutil.which("git"), "git required")
class DriftGuardTests(GateTestCase):
    def setUp(self) -> None:
        super().setUp()
        g = lambda *a: subprocess.run(["git", "-C", str(self.project), *a], capture_output=True, text=True, check=False)  # noqa: E731
        self.git = g
        self.assertEqual(g("init", "-q").returncode, 0)
        g("config", "user.email", "t@example.com")
        g("config", "user.name", "T")
        g("add", ".")
        self.assertEqual(g("commit", "-qm", "base").returncode, 0)

    def test_contract_change_without_truth_sync_blocks(self):
        c = self.project / "contracts/openapi.yaml"
        c.write_text(c.read_text(encoding="utf-8") + "  /tickets/{id}/archive: {}\n", encoding="utf-8")
        report = self.assertBlocks("DRIFT_UNSYNCED_NATIVE_TRUTH", "--changed-since", "HEAD")
        self.assertEqual(report["facts"]["changed_since"]["native_truth_changed"], ["contracts/openapi.yaml"])

    def test_contract_change_with_truth_sync_passes(self):
        c = self.project / "contracts/openapi.yaml"
        c.write_text(c.read_text(encoding="utf-8") + "  /tickets/{id}/archive: {}\n", encoding="utf-8")
        s = self.project / "docs/SYSTEM.md"
        s.write_text(s.read_text(encoding="utf-8") + "\nArchive endpoint added (see changes/).\n", encoding="utf-8")
        rc, report = doctor(self.project, "--changed-since", "HEAD")
        self.assertEqual(rc, 0, report)

    def test_new_untracked_schema_counts_as_change(self):
        (self.project / "schemas/002_add_archive.sql").write_text("ALTER TABLE ticket ADD archived BOOLEAN;\n", encoding="utf-8")
        self.assertBlocks("DRIFT_UNSYNCED_NATIVE_TRUTH", "--changed-since", "HEAD")

    def test_unresolvable_base_blocks(self):
        self.assertBlocks("DRIFT_BASE_UNRESOLVED", "--changed-since", "no-such-ref")


class MigrationTests(unittest.TestCase):
    LEGACY = (
        "# WP-007: Billing Export\n\nstatus: READY\nowner: Finance Eng\ntimebox: L2 / 1-3 days\n"
        "governance_level: L2\naffected_surface: schema, export job\n\n"
        "## Dependencies\nWP-003 integrated.\n\n## Read Set\n`docs/SYSTEM.md`, `schemas/001_billing.sql`, SYSTEM.\n\n"
        "## Write Set\n`src/export/**`, repository layer.\n\n"
        "## Done Condition\n`pytest tests/export -q` passes and `contracts/export.csv.schema.json` is updated.\n"
    )

    def test_migration_is_mechanical_and_does_not_invent_approval(self):
        with tempfile.TemporaryDirectory() as td:
            wp = Path(td) / "WP-007.md"
            wp.write_text(self.LEGACY, encoding="utf-8")
            dry = run(MIGRATE, wp)
            self.assertEqual(dry.returncode, 0, dry.stderr)
            self.assertEqual(wp.read_text(encoding="utf-8"), self.LEGACY, "dry run must not modify files")

            cp = run(MIGRATE, wp, "--write", "--authored-by", "agent:compiler")
            self.assertEqual(cp.returncode, 0, cp.stderr + cp.stdout)
            text = wp.read_text(encoding="utf-8")
            data = tomllib.loads(text.split("+++")[1])
            self.assertEqual(data["id"], "WP-007")
            self.assertEqual(data["title"], "Billing Export")
            self.assertEqual(data["risk_level"], "R2")
            self.assertEqual(data["affected_surface"], ["schema", "export job"])
            self.assertEqual(data["depends_on"], ["WP-003"])
            self.assertEqual(data["read_set"], ["docs/SYSTEM.md", "schemas/001_billing.sql"])
            self.assertEqual(data["write_set"], ["src/export/**"])
            self.assertEqual(data["done"]["commands"], ["pytest tests/export -q"])
            self.assertEqual(data["done"]["artifacts"], ["contracts/export.csv.schema.json"])
            self.assertEqual(data["approval"]["authored_by"], "agent:compiler")
            self.assertEqual(data["approval"]["approved_by"], "")
            self.assertNotIn("governance_level", text)
            self.assertIn("## Done Condition", text)

            again = run(MIGRATE, wp, "--write")
            self.assertIn("SKIP", again.stdout)
            self.assertEqual(wp.read_text(encoding="utf-8"), text, "migration must be idempotent")

    def test_migrated_pack_surfaces_gaps_instead_of_hiding_them(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td) / "golden"
            shutil.copytree(GOLDEN, project)
            (project / "docs/engineering/work/WP-001.md").write_text(
                "# WP-001: Ticket API\n\nstatus: READY\nowner: E\ngovernance_level: L2\n\n"
                "## Read Set\n`contracts/openapi.yaml`\n\n## Done\nContract tests pass.\n", encoding="utf-8")
            self.assertEqual(run(MIGRATE, project / "docs/engineering/work", "--write").returncode, 0)
            rc, report = doctor(project)
            self.assertNotEqual(rc, 0)
            self.assertIn("WP_DONE_UNVERIFIABLE", codes(report))
            self.assertIn("WP_APPROVAL_MISSING", codes(report))
            self.assertNotIn("WP_LEGACY_FORMAT", codes(report, "warnings"))


class TemplateContractTests(unittest.TestCase):
    """The WP template and doctor must agree on field names; wording is free to change."""

    def test_wp_template_frontmatter_is_valid_and_complete(self):
        text = (ROOT / "templates/WORK_PACKET.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("+++\n"))
        data = tomllib.loads(text.split("+++")[1])
        for key in ["id", "status", "owner", "risk_level", "affected_surface", "depends_on", "parallel_safe_with",
                    "read_set", "write_set", "acceptance_refs", "checkpoints"]:
            self.assertIn(key, data, key)
        self.assertEqual(set(data["done"]), {"commands", "artifacts"})
        self.assertEqual(set(data["approval"]), {"authored_by", "approved_by"})

    def test_reference_wp_fills_every_template_field(self):
        template = tomllib.loads((ROOT / "templates/WORK_PACKET.md").read_text(encoding="utf-8").split("+++")[1])
        ref = tomllib.loads((GOLDEN / "docs/engineering/work/WP-001.md").read_text(encoding="utf-8").split("+++")[1])
        for key in ["id", "title", "status", "owner", "risk_level", "affected_surface", "read_set", "write_set",
                    "acceptance_refs", "checkpoints"]:
            self.assertTrue(ref.get(key), key)
        self.assertTrue(ref["done"]["commands"])
        self.assertTrue(ref["approval"]["approved_by"])
        self.assertNotEqual(ref["approval"]["approved_by"], ref["approval"]["authored_by"])
        self.assertLessEqual(set(ref) - {"execution", "integrator"}, set(template) | {"title"})

    def test_acceptance_template_has_id_column(self):
        text = (ROOT / "templates/ACCEPTANCE.md").read_text(encoding="utf-8")
        self.assertRegex(text, r"\|\s*ID\s*\|")


if __name__ == "__main__":
    unittest.main()
