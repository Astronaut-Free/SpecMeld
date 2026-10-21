from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]
INIT = ROOT / "scripts" / "init_project.py"
INIT_PACK = ROOT / "scripts" / "init_engineering_pack.py"
DOCTOR = ROOT / "scripts" / "doctor.py"
GOLDEN = ROOT / "examples" / "mini-ticket-triage"
LEGAL = ROOT / "examples" / "legal-consult-mini-app"
GRAPH = ROOT / "examples" / "knowledge-graph-atlas"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *map(str, args)],
        text=True,
        capture_output=True,
        check=False,
    )


def git(cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", "-C", str(cwd), *args], text=True, capture_output=True, check=False)


class ToolingTests(unittest.TestCase):
    # Existing 1.0.1 regression coverage
    def test_init_project_renders_valid_toml(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td) / "demo"
            cp = run(INIT, project, "--name", 'demo "quoted"', "--mode", "brownfield", "--profile", "lite", "--archetype", "web")
            self.assertEqual(cp.returncode, 0, cp.stderr + cp.stdout)
            data = tomllib.loads((project / "PROJECT.toml").read_text(encoding="utf-8"))
            self.assertEqual(data["name"], 'demo "quoted"')
            self.assertEqual(data["mode"], "brownfield")
            self.assertEqual(data["profile"], "lite")
            self.assertEqual(data["archetype"], "web")
            self.assertNotIn("__PROJECT_", (project / "PROJECT.toml").read_text(encoding="utf-8"))

    def test_init_is_idempotent_and_does_not_overwrite(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td) / "demo"
            self.assertEqual(run(INIT, project, "--name", "demo").returncode, 0)
            product = project / "docs" / "PRODUCT.md"
            product.write_text("sentinel\n", encoding="utf-8")
            cp = run(INIT, project, "--name", "demo")
            self.assertEqual(cp.returncode, 0, cp.stderr + cp.stdout)
            self.assertEqual(product.read_text(encoding="utf-8"), "sentinel\n")
            self.assertIn("SKIP docs/PRODUCT.md", cp.stdout)

    def test_init_engineering_pack_moves_status_to_draft(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td) / "demo"
            self.assertEqual(run(INIT, project, "--name", "demo").returncode, 0)
            cp = run(INIT_PACK, project)
            self.assertEqual(cp.returncode, 0, cp.stderr + cp.stdout)
            data = tomllib.loads((project / "PROJECT.toml").read_text(encoding="utf-8"))
            self.assertEqual(data["engineering_pack"]["status"], "DRAFT")
            self.assertTrue((project / "docs/engineering/IMPLEMENTATION_ENTRY.md").exists())

    def test_doctor_g0_skeleton_pass_is_scoped(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td) / "demo"
            self.assertEqual(run(INIT, project, "--name", "demo").returncode, 0)
            cp = run(DOCTOR, project)
            self.assertEqual(cp.returncode, 0, cp.stderr + cp.stdout)
            self.assertIn("G0_INTENT_STABLE", cp.stdout)
            self.assertIn("not proof of functional correctness", cp.stdout)

    def test_doctor_g1_rejects_uncompiled_draft(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td) / "demo"
            self.assertEqual(run(INIT, project, "--name", "demo").returncode, 0)
            self.assertEqual(run(INIT_PACK, project).returncode, 0)
            text = (project / "PROJECT.toml").read_text(encoding="utf-8")
            text = text.replace('stage = "G0_INTENT_STABLE"', 'stage = "G1_BUILD_READY"')
            text = text.replace('status = "DRAFT" # NOT_COMPILED', 'status = "DEVELOPMENT_READY" # NOT_COMPILED')
            text = text.replace('product = ""', 'product = "P"', 1)
            text = text.replace('engineering = ""', 'engineering = "E"', 1)
            text = text.replace('data_storage = "UNKNOWN"', 'data_storage = "NOT_APPLICABLE"')
            text = text.replace('data_storage = "verify persistence needs before G1"', 'data_storage = "no persistence"')
            text = text.replace('api_integration = "UNKNOWN"', 'api_integration = "NOT_APPLICABLE"')
            text = text.replace('api_integration = "verify service/integration needs before G1"', 'api_integration = "no API"')
            text = text.replace('runtime_infrastructure = "UNKNOWN"', 'runtime_infrastructure = "NOT_APPLICABLE"')
            text = text.replace('runtime_infrastructure = "verify runtime/deployment needs before G1"', 'runtime_infrastructure = "library only"')
            (project / "PROJECT.toml").write_text(text, encoding="utf-8")
            (project / "docs/engineering/work/WP-001.md").write_text("# WP-001\nstatus: READY\nowner: E\n\n## Goal\ndemo\n\n## Done Condition\n`python -m unittest` passes.\n", encoding="utf-8")
            cp = run(DOCTOR, project)
            self.assertNotEqual(cp.returncode, 0)
            self.assertIn("not READY", cp.stdout)

    def test_golden_example_passes_g1(self):
        cp = run(DOCTOR, GOLDEN)
        self.assertEqual(cp.returncode, 0, cp.stderr + cp.stdout)
        self.assertIn("G1_BUILD_READY", cp.stdout)

    def test_g1_blocks_unknowns(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td) / "golden"
            shutil.copytree(GOLDEN, project)
            p = project / "PROJECT.toml"
            text = p.read_text(encoding="utf-8").replace("items = []", 'items = ["decide tenant model"]')
            p.write_text(text, encoding="utf-8")
            cp = run(DOCTOR, project)
            self.assertNotEqual(cp.returncode, 0)
            self.assertIn("blocking unknowns", cp.stdout)

    def test_g1_validates_exception_fields(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td) / "golden"
            shutil.copytree(GOLDEN, project)
            p = project / "PROJECT.toml"
            p.write_text(p.read_text(encoding="utf-8") + '\n[[exception]]\nid="EX-1"\nreason="temporary"\n', encoding="utf-8")
            cp = run(DOCTOR, project)
            self.assertNotEqual(cp.returncode, 0)
            self.assertIn("exception[1] missing", cp.stdout)

    # P0-1 Nano profile
    def test_nano_init_creates_only_project_truth(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td) / "nano"
            cp = run(INIT, project, "--name", "nano", "--profile", "nano", "--archetype", "internal")
            self.assertEqual(cp.returncode, 0, cp.stderr + cp.stdout)
            files = sorted(str(p.relative_to(project)).replace("\\", "/") for p in project.rglob("*") if p.is_file())
            self.assertEqual(files, ["PROJECT.toml", "docs/PROJECT.md"])
            pack = run(INIT_PACK, project)
            self.assertEqual(pack.returncode, 0, pack.stderr + pack.stdout)
            self.assertIn("SKIP nano profile", pack.stdout)
            self.assertFalse((project / "docs/engineering").exists())
            self.assertIn("Nano: docs/PROJECT.md", (ROOT / "references/ARTIFACTS.md").read_text(encoding="utf-8"))

    def test_nano_doctor_uses_light_path_even_at_g1(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td) / "nano"
            self.assertEqual(run(INIT, project, "--name", "nano", "--profile", "nano").returncode, 0)
            p = project / "PROJECT.toml"
            p.write_text(p.read_text(encoding="utf-8").replace('stage = "G0_INTENT_STABLE"', 'stage = "G1_BUILD_READY"'), encoding="utf-8")
            cp = run(DOCTOR, project)
            self.assertEqual(cp.returncode, 0, cp.stderr + cp.stdout)
            self.assertNotIn("engineering_pack.status", cp.stdout)
            self.assertNotIn("owner missing", cp.stdout)

    def test_nano_secret_scan_blocks_leaks(self):
        samples = [
            "AKIA1234567890ABCDEF",
            "sk-exampleSecret123456",
            "api_key=example-secret",
            "-----BEGIN PRIVATE KEY-----",
            "password=example-secret",
        ]
        for sample in samples:
            with self.subTest(sample=sample), tempfile.TemporaryDirectory() as td:
                project = Path(td) / "nano"
                self.assertEqual(run(INIT, project, "--name", "nano", "--profile", "nano").returncode, 0)
                (project / "docs/PROJECT.md").write_text("# Project\n" + sample + "\n", encoding="utf-8")
                cp = run(DOCTOR, project)
                self.assertNotEqual(cp.returncode, 0)
                self.assertIn("possible secret", cp.stdout)

    # P0-2 mobile/mini-program module
    # P0-3 golden examples
    def test_legal_consult_golden_passes_and_is_bounded(self):
        cp = run(DOCTOR, LEGAL)
        self.assertEqual(cp.returncode, 0, cp.stderr + cp.stdout)
        self.assertLessEqual(sum(1 for p in LEGAL.rglob("*") if p.is_file()), 20)
        project = tomllib.loads((LEGAL / "PROJECT.toml").read_text(encoding="utf-8"))
        self.assertEqual(project["archetype"], "mini-program")
        self.assertIn("payments=DEFERRED", project["coverage_notes"]["conditional"])
        self.assertIn("owner=", project["coverage_notes"]["conditional"])
        self.assertTrue((LEGAL / "docs/engineering/specs/SECURITY_PRIVACY.md").exists())
        self.assertTrue((LEGAL / "docs/engineering/specs/AI_QA.md").exists())
        self.assertTrue((LEGAL / "docs/engineering/specs/MOBILE_MINI_PROGRAM.md").exists())

    def test_knowledge_graph_golden_passes_and_is_bounded(self):
        cp = run(DOCTOR, GRAPH)
        self.assertEqual(cp.returncode, 0, cp.stderr + cp.stdout)
        self.assertLessEqual(sum(1 for p in GRAPH.rglob("*") if p.is_file()), 20)
        project = tomllib.loads((GRAPH / "PROJECT.toml").read_text(encoding="utf-8"))
        self.assertEqual(project["archetype"], "data")
        spec = (GRAPH / "docs/engineering/specs/SOURCE_PROVENANCE_ENTITY_RESOLUTION.md").read_text(encoding="utf-8")
        adr = (GRAPH / "decisions/ADR-0001_GRAPH_STORAGE.md").read_text(encoding="utf-8")
        self.assertIn("Lineage", spec)
        self.assertIn("Data Quality", spec)
        self.assertIn("Options Considered", adr)

    # P0-4 deterministic semantic heuristics
    def test_doctor_warns_on_empty_acceptance(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td) / "golden"
            shutil.copytree(GOLDEN, project)
            p = project / "docs/PRODUCT.md"
            text = p.read_text(encoding="utf-8")
            text = re.sub(r"(?s)## Acceptance\n.*$", "## Acceptance Criteria\nTBD\n", text)
            p.write_text(text, encoding="utf-8")
            cp = run(DOCTOR, project)
            self.assertEqual(cp.returncode, 0, cp.stderr + cp.stdout)
            self.assertIn("acceptance criteria section is empty", cp.stdout)

    def test_doctor_warns_on_adr_without_options(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td) / "golden"
            shutil.copytree(GOLDEN, project)
            (project / "decisions").mkdir(parents=True, exist_ok=True)
            (project / "decisions/ADR-0099.md").write_text("# ADR\nowner: Engineering Owner\n\n## Context\nChoose storage.\n\n## Decision\nUse SQL.\n", encoding="utf-8")
            cp = run(DOCTOR, project)
            self.assertEqual(cp.returncode, 0, cp.stderr + cp.stdout)
            self.assertIn("ADR has no alternatives/options list", cp.stdout)

    def test_doctor_issues_on_spec_or_wp_without_owner(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td) / "golden"
            shutil.copytree(GOLDEN, project)
            spec = project / "docs/engineering/specs/AI_TRIAGE.md"
            spec.write_text(spec.read_text(encoding="utf-8").replace("owner: Engineering Owner", "owner:"), encoding="utf-8")
            wp = project / "docs/engineering/work/WP-001.md"
            wp.write_text(wp.read_text(encoding="utf-8").replace('owner = "Engineering Owner"', 'owner = ""'), encoding="utf-8")
            cp = run(DOCTOR, project)
            self.assertNotEqual(cp.returncode, 0)
            self.assertIn("Engineering Spec missing owner", cp.stdout)
            self.assertIn("Work Packet missing owner", cp.stdout)

    @unittest.skipUnless(shutil.which("git"), "git required")
    def test_doctor_warns_when_entry_baseline_differs_from_git_head(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td) / "golden"
            shutil.copytree(GOLDEN, project)
            self.assertEqual(git(project, "init").returncode, 0)
            git(project, "config", "user.email", "test@example.com")
            git(project, "config", "user.name", "Test")
            git(project, "add", ".")
            self.assertEqual(git(project, "commit", "-m", "initial").returncode, 0)
            entry = project / "docs/engineering/IMPLEMENTATION_ENTRY.md"
            entry.write_text(entry.read_text(encoding="utf-8").replace("baseline_sha: greenfield", "baseline_sha: deadbeef"), encoding="utf-8")
            cp = run(DOCTOR, project)
            self.assertEqual(cp.returncode, 0, cp.stderr + cp.stdout)
            self.assertIn("baseline_sha differs from current git HEAD", cp.stdout)

    def test_doctor_scans_contracts_for_secrets(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td) / "golden"
            shutil.copytree(GOLDEN, project)
            (project / "contracts/leak.txt").write_text("sk-exampleSecret123456\n", encoding="utf-8")
            cp = run(DOCTOR, project)
            self.assertNotEqual(cp.returncode, 0)
            self.assertIn("possible secret in contracts/leak.txt", cp.stdout)

    # P1-5 provider abstraction
    def test_collaboration_provider_is_validated_and_documented(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td) / "golden"
            shutil.copytree(GOLDEN, project)
            p = project / "PROJECT.toml"
            p.write_text(p.read_text(encoding="utf-8").replace('provider = "github"', 'provider = "svn"'), encoding="utf-8")
            cp = run(DOCTOR, project)
            self.assertNotEqual(cp.returncode, 0)
            self.assertIn("collaboration.provider invalid", cp.stdout)

    # P1-6 truth doc governance and drift
    @unittest.skipUnless(shutil.which("git"), "git required")
    def test_doctor_warns_when_last_converged_sha_is_over_50_commits_behind(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td) / "demo"
            self.assertEqual(run(INIT, project, "--name", "demo").returncode, 0)
            self.assertEqual(git(project, "init").returncode, 0)
            git(project, "config", "user.email", "test@example.com")
            git(project, "config", "user.name", "Test")
            git(project, "add", ".")
            self.assertEqual(git(project, "commit", "-m", "initial").returncode, 0)
            old = git(project, "rev-parse", "HEAD").stdout.strip()
            p = project / "PROJECT.toml"
            p.write_text(p.read_text(encoding="utf-8").replace('last_converged_sha = ""', f'last_converged_sha = "{old}"'), encoding="utf-8")
            git(project, "add", "PROJECT.toml")
            self.assertEqual(git(project, "commit", "-m", "record convergence").returncode, 0)
            for i in range(50):
                self.assertEqual(git(project, "commit", "--allow-empty", "-m", f"c{i}").returncode, 0)
            cp = run(DOCTOR, project)
            self.assertEqual(cp.returncode, 0, cp.stderr + cp.stdout)
            self.assertIn("documentation convergence is stale", cp.stdout)

    # P1-7 UAT sign-off
    def test_g3_requires_human_uat_signoff(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td) / "golden"
            shutil.copytree(GOLDEN, project)
            p = project / "PROJECT.toml"
            text = p.read_text(encoding="utf-8")
            text = text.replace('stage = "G1_BUILD_READY"', 'stage = "G3_RELEASE_READY"')
            text = text.replace('status = "DEVELOPMENT_READY"', 'status = "CONVERGED"')
            text = text.replace('release = ""', 'release = "Release Owner"', 1)
            p.write_text(text, encoding="utf-8")
            cp = run(DOCTOR, project)
            self.assertNotEqual(cp.returncode, 0)
            self.assertIn("uat_signed_by", cp.stdout)
            p.write_text(p.read_text(encoding="utf-8").replace('uat_signed_by = ""', 'uat_signed_by = "UAT Lead"'), encoding="utf-8")
            cp2 = run(DOCTOR, project)
            self.assertEqual(cp2.returncode, 0, cp2.stderr + cp2.stdout)

    # P1-8 timebox
    # P2 implemented where low-churn and useful
    # V1.1.0 — SpecMeld branding, design governance, progressive governance
    def test_progressive_governance_is_wired_and_project_default_is_validated(self):
        project_template = tomllib.loads((ROOT / "templates/PROJECT.toml").read_text(encoding="utf-8").replace("__", "x"))
        self.assertEqual(project_template["governance"]["default_level"], "auto")
        with tempfile.TemporaryDirectory() as td:
            project = Path(td) / "golden"
            shutil.copytree(GOLDEN, project)
            p = project / "PROJECT.toml"
            p.write_text(p.read_text(encoding="utf-8").replace('default_level = "auto"', 'default_level = "MAX"'), encoding="utf-8")
            cp = run(DOCTOR, project)
            self.assertNotEqual(cp.returncode, 0)
            self.assertIn("governance.default_level invalid", cp.stdout)

    def test_doctor_rejects_invalid_wp_risk_level(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td) / "golden"
            shutil.copytree(GOLDEN, project)
            wp = project / "docs/engineering/work/WP-001.md"
            wp.write_text(wp.read_text(encoding="utf-8").replace('risk_level = "R2"', 'risk_level = "R9"'), encoding="utf-8")
            cp = run(DOCTOR, project)
            self.assertNotEqual(cp.returncode, 0)
            self.assertIn("invalid risk_level R9", cp.stdout)

    def _make_brownfield_r2_golden(self, project: Path) -> Path:
        shutil.copytree(GOLDEN, project)
        pj = project / "PROJECT.toml"
        text = pj.read_text(encoding="utf-8")
        text = text.replace('mode = "greenfield"', 'mode = "brownfield"')
        text = text.replace('baseline_sha = ""', 'baseline_sha = "abc123"')
        pj.write_text(text, encoding="utf-8")
        lld = project / "docs/engineering/lld/LLD-001_TRIAGE_FLOW.md"
        self.assertIn("risk_level: R2", lld.read_text(encoding="utf-8"))
        return lld

    def test_brownfield_r2_lld_blocks_unresolved_authority(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td) / "golden"
            lld = self._make_brownfield_r2_golden(project)
            text = lld.read_text(encoding="utf-8")
            text = text.replace("authority_status: ALIGNED", "authority_status: CONFLICT")
            text = text.replace("physical_reality_audit: NOT_APPLICABLE", "physical_reality_audit: PASS")
            text += "\n## Authority / Physical Reality Audit\n\n### Physical Reality Matrix\n| Object | Evidence |\n|---|---|\n| ticket | schemas/001_create_ticket.sql |\n"
            lld.write_text(text, encoding="utf-8")
            cp = run(DOCTOR, project)
            self.assertNotEqual(cp.returncode, 0)
            self.assertIn("authority is unresolved (CONFLICT)", cp.stdout)

    def test_brownfield_r2_lld_claimed_reality_pass_requires_matrix_evidence(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td) / "golden"
            lld = self._make_brownfield_r2_golden(project)
            text = lld.read_text(encoding="utf-8")
            text = text.replace("physical_reality_audit: NOT_APPLICABLE", "physical_reality_audit: PASS")
            lld.write_text(text, encoding="utf-8")
            cp = run(DOCTOR, project)
            self.assertNotEqual(cp.returncode, 0)
            self.assertIn("claims physical reality PASS without matrix evidence", cp.stdout)

    def test_brownfield_r2_lld_passes_with_aligned_authority_and_matrix_evidence(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td) / "golden"
            lld = self._make_brownfield_r2_golden(project)
            text = lld.read_text(encoding="utf-8")
            text = text.replace("physical_reality_audit: NOT_APPLICABLE", "physical_reality_audit: PASS")
            text += "\n## Authority / Physical Reality Audit\n\n### Physical Reality Matrix\n| Object | Evidence |\n|---|---|\n| ticket | schemas/001_create_ticket.sql + contract tests |\n"
            lld.write_text(text, encoding="utf-8")
            cp = run(DOCTOR, project)
            self.assertEqual(cp.returncode, 0, cp.stderr + cp.stdout)

    def test_brownfield_r1_lld_does_not_require_heavy_reality_gate(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td) / "golden"
            lld = self._make_brownfield_r2_golden(project)
            text = lld.read_text(encoding="utf-8")
            text = text.replace("risk_level: R2", "risk_level: R1")
            text = text.replace("authority_status: ALIGNED", "authority_status: NOT_ASSESSED")
            lld.write_text(text, encoding="utf-8")
            cp = run(DOCTOR, project)
            self.assertEqual(cp.returncode, 0, cp.stderr + cp.stdout)

    def test_open_source_branding_and_mit_license_are_present(self):
        readme_en = (ROOT / "README.md").read_text(encoding="utf-8")
        readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("# SpecMeld", readme_en)
        self.assertIn("SpecMeld（构序）", readme_zh)
        self.assertIn("SpecMeld（构序）", skill)
        self.assertIn("Current Skill ID (v1.x)", readme_en)
        self.assertIn("MIT License", license_text)
        self.assertTrue((ROOT / "CONTRIBUTING.md").exists())
        self.assertTrue((ROOT / "SECURITY.md").exists())

    def test_bilingual_readmes_cross_link_and_cover_same_entry_points(self):
        readme_en = (ROOT / "README.md").read_text(encoding="utf-8")
        readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
        self.assertIn("README.zh-CN.md", readme_en)
        self.assertIn("README.md", readme_zh)
        for token in [
            "software-project-standardizer",
            "references/DESIGN_GOVERNANCE.md",
            "references/GOVERNANCE.md",
            "scripts/doctor.py",
            "scripts/migrate_wp.py",
            "--changed-since",
            "examples/mini-ticket-triage",
            "MIT",
        ]:
            self.assertIn(token, readme_en, token)
            self.assertIn(token, readme_zh, token)


class PackageHygieneTests(unittest.TestCase):
    def test_gitignore_excludes_python_cache(self):
        ignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("__pycache__/", ignore)
        self.assertIn("*.py[cod]", ignore)

    def test_version_is_consistent(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertRegex(version, r"^\d+\.\d+\.\d+$")
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn(f"V{version}", skill)
        self.assertIn(f"## {version}", (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"))
        template = (ROOT / "templates/PROJECT.toml").read_text(encoding="utf-8")
        self.assertIn(f'software-project-standardizer/{version}', template)
        self.assertIn('brand = "SpecMeld"', template)
        doctor = (ROOT / "scripts/doctor.py").read_text(encoding="utf-8")
        self.assertIn(f'DOCTOR_VERSION = "{version}"', doctor)
        for ex in [GOLDEN, LEGAL, GRAPH]:
            ex_text = (ex / "PROJECT.toml").read_text(encoding="utf-8")
            self.assertIn(f'software-project-standardizer/{version}', ex_text)
            self.assertIn('brand = "SpecMeld"', ex_text)

    def test_skill_progressive_disclosure_limits(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertLessEqual(len(skill.splitlines()), 380)
        m = re.search(r"(?m)^description:\s*(.+)$", skill)
        self.assertIsNotNone(m)
        self.assertLessEqual(len(m.group(1)), 1024)

    def test_selftest_ci_covers_windows_and_linux(self):
        workflow = (ROOT / ".github/workflows/selftest.yml").read_text(encoding="utf-8")
        self.assertIn("ubuntu-latest", workflow)
        self.assertIn("windows-latest", workflow)
        self.assertIn("runs-on: ${{ matrix.os }}", workflow)

    def test_all_references_are_indexed_from_skill(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        for ref in sorted((ROOT / "references").glob("*.md")):
            self.assertIn(f"references/{ref.name}", skill, ref.name)


if __name__ == "__main__":
    unittest.main()
