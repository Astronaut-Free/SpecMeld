# Changelog

## 1.1.1 — Bilingual Open-Source README

Documentation-only open-source readiness patch. No G0–G4, L1–L3, doctor gate, compiler, template-count, or runtime behavior semantics changed.

- `README.md` is now the default English project homepage.
- Added `README.zh-CN.md` as the Simplified Chinese homepage, with explicit language switching in both directions.
- Both README files keep the same product positioning, Quick Start, Nano, mature Brownfield, Design Governance, Progressive Governance, doctor boundary, examples, feedback loop, and open-source entry points.
- Version markers are synchronized to `1.1.1`.
  - Tests: `test_bilingual_readmes_cross_link_and_cover_same_entry_points`, `test_open_source_branding_and_mit_license_are_present`, `test_p2_retrospective_feedback_loop_exists`, `test_version_is_consistent`.

## 1.1.0 — SpecMeld Brand + Design Governance + Progressive Governance

V1.1.0 是基于真实项目反馈的能力升级，不改变 G0–G4、Change Class L1–L3、nano/right-sized compilation 的核心语义。品牌升级为 **SpecMeld（构序）**，同时保留 v1.x 技术 Skill ID `software-project-standardizer`，避免既有安装和 `PROJECT.toml` 失效。

### Brand / open-source readiness
- README / SKILL 对外品牌统一为 `SpecMeld（构序）`；`PROJECT.toml` 增加 `brand = "SpecMeld"`，但 `standard = "software-project-standardizer/1.1.0"` 继续作为 v1.x 兼容标识。
- LICENSE 从保守保留版权切换为 MIT；新增 `CONTRIBUTING.md`、`SECURITY.md`，README 增加安装、兼容性和公开发布说明。
  - Tests: `test_open_source_branding_and_mit_license_are_present`, `test_version_is_consistent`.

### Design Authority / Physical Reality Audit
- 新增 `references/DESIGN_GOVERNANCE.md`，把 Brownfield 设计从“Reality awareness”提升到“Reality arbitration”：区分 Intent Authority 与 Reality Evidence，禁止 Agent 在冲突时自行折中。
- 定义 `IMPLEMENTATION_DRIFT / DOCUMENT_DRIFT / DRAFT_DRIFT / CONTRACT_GAP / AUTHORITY_CONFLICT / CONTROLLED_AMENDMENT_REQUIRED / PHYSICAL_REALITY_BLOCKED`。
- `LLD.md` 新增按需 `Physical Reality Matrix / Permission Matrix / Transaction Matrix`，以及 `authority_status`、`physical_reality_audit` 机器字段。
- doctor 对 **Brownfield + governance L2/L3** 的 LLD 强制检查 Authority 状态和 Reality Audit；声明 `PASS` 但无 matrix evidence 会失败，L1 不触发重型检查。
  - Tests: `test_brownfield_l2_lld_blocks_unresolved_authority`, `test_brownfield_l2_lld_claimed_reality_pass_requires_matrix_evidence`, `test_brownfield_l2_lld_passes_with_aligned_authority_and_matrix_evidence`, `test_brownfield_l1_lld_does_not_require_heavy_reality_gate`.

### Progressive Governance / Right-Sizing
- 新增 `references/GOVERNANCE.md`，治理强度由 `Stage + Risk + Affected Surface + Blast Radius` 决定。
- `L1 Development` 用于普通 feature/bug；`L2 Critical Surface` 用于 schema/migration/shared contract/core runtime/canonical；`L3 Production/Security` 用于 identity/permission/canonical authority/release control plane 等高风险面。
- `PROJECT.toml` 新增 `[governance].default_level = "auto"`；Change/WP/LLD 增加 `governance_level`，doctor 校验项目默认值和 WP/LLD 合法性。
- 明确高风险 Gate 只冻结 dependency/write-set 相关工作，不得自动让无依赖 workstream 全停。
  - Tests: `test_progressive_governance_is_wired_and_project_default_is_validated`, `test_doctor_rejects_invalid_wp_governance_level`.

### Design lifecycle / archive boundary
- `LIFECYCLE.md` 增加设计资产验证链：`DRAFT → PHYSICAL_AUDIT → AUTHORITY_CHECK → CONSISTENCY_CHECK → SCENARIO_VALIDATION → INDEPENDENT_REVIEW → FREEZE_CANDIDATE → EXACT_SHA → FROZEN`，但不要求为每一步新建文档。
- `SYNC.md` / `ARTIFACTS.md` 明确 ZIP、release bundle、milestone snapshot 只做 archive/evidence，不承担 Current Truth；archive 里的旧 Draft 不能自动覆盖当前 repository authority。
  - Test: `test_archive_snapshot_is_explicitly_not_current_truth`.

### Mature Brownfield route
- `EXECUTION.md` 增加已上线/长期维护项目路径：`Production/Repo Reality → Authority & Truth Audit → Drift/Gap → G0–G4 Assessment → Right-sized Compilation → Evolution Plan → READY WPs`。
- `COMPILER.md` 在 Artifact Plan 前新增 governance pass；Brownfield L2/L3 在冻结 LLD 前必须执行 Design Governance。
  - Regression coverage: three golden examples remain doctor-pass; existing Brownfield/nano/G1 tests remain enabled.

### Compatibility / package discipline
- `VERSION = 1.1.0`；SKILL 标题、PROJECT template、三个 golden examples 同步。
- `SKILL.md` 继续控制在 380 行以内，新增 reference 通过 progressive disclosure 按需加载。
  - Tests: `test_version_is_consistent`, `test_skill_progressive_disclosure_limits`, `test_all_references_are_indexed_from_skill`.

## 1.0.2 — Right-sized Profiles & Deterministic Quality Gates

V1.0.2 不改变 G0–G4 / L1–L3 核心语义；重点是把小项目路径、移动/小程序、golden examples、语义启发、provider 抽象和文档治理做成可测试机制。

### P0 — Nano profile
- 新增 `profile = "nano"`。初始化只创建 `PROJECT.toml + docs/PROJECT.md`；`init_engineering_pack.py` 对 nano 明确跳过；doctor 走独立轻量路径，只检查 name、stage、truth 文件存在和 secrets。
  - Tests: `test_nano_init_creates_only_project_truth`, `test_nano_doctor_uses_light_path_even_at_g1`, `test_nano_secret_scan_blocks_leaks`.

### P0 — Mobile / Mini Program spec module
- `COMPILER.md` 新增 `MOBILE_MINI_PROGRAM`：设备权限、签名/主体、商店/小程序审核、灰度发布、版本兼容、分包、离线/弱网；`SKILL.md` spec 列表和 `COVERAGE.md` Product & UX 检查同步引用。
  - Test: `test_mobile_mini_program_catalog_and_coverage_are_wired`.

### P0 — Golden example expansion
- 新增 `examples/legal-consult-mini-app/`：mini-program archetype，覆盖 Security/Privacy、AI Q&A、合规约束、payments DEFERRED owner/trigger/target、MOBILE_MINI_PROGRAM。
  - Test: `test_legal_consult_golden_passes_and_is_bounded`.
- 新增 `examples/knowledge-graph-atlas/`：data archetype，覆盖 SOURCE_PROVENANCE_ENTITY_RESOLUTION、图存储 trade-off ADR、数据血缘和数据质量。
  - Test: `test_knowledge_graph_golden_passes_and_is_bounded`.
- CI self-test 现在运行三个 golden examples 的 doctor。
  - Regression tests: `test_golden_example_passes_g1`, `test_legal_consult_golden_passes_and_is_bounded`, `test_knowledge_graph_golden_passes_and_is_bounded`.

### P0 — Deterministic semantic heuristics
- Acceptance Criteria 为空或占位符时 warning。
  - Test: `test_doctor_warns_on_empty_acceptance`.
- WP Done Condition 没有可执行命令或可验证产物时 warning。
  - Test: `test_doctor_warns_on_unverifiable_wp_done_condition`.
- ADR 无 alternatives/options 列表时 warning。
  - Test: `test_doctor_warns_on_adr_without_options`.
- Engineering Spec / Work Packet 缺 owner 时 issue。
  - Test: `test_doctor_issues_on_spec_or_wp_without_owner`.
- `IMPLEMENTATION_ENTRY.baseline_sha` 与可读取的当前 Git HEAD 不一致时 warning。
  - Test: `test_doctor_warns_when_entry_baseline_differs_from_git_head`.
- secrets 扫描覆盖 `PROJECT.toml`、`docs/`、`contracts/`，命中 AKIA / sk- / api_key= / private key / password= 时 issue。
  - Tests: `test_nano_secret_scan_blocks_leaks`, `test_doctor_scans_contracts_for_secrets`.

### P1 — Provider-neutral collaboration
- `[collaboration]` 增加 `provider = github | gitlab | gitee | local`；doctor 校验 provider。
- `DELIVERY.md` 把 CODEOWNERS / Merge Queue 明确标为“GitHub 专属，其他平台使用等价机制”。
- `COLLABORATION.md` 增加 GitHub / GitLab / Gitee / local worktree 的机制映射；EXECUTION / COMPILER / README / SKILL 的协作表述同步去 GitHub 单一化。
  - Test: `test_collaboration_provider_is_validated_and_documented`.

### P1 — Truth document governance & drift
- `SYNC.md` 增加 truth 文档的 Git 审计流程、commit message 规范、revert/forward-fix 规则。
- doctor 在 Git 可用时检查 `engineering_pack.last_converged_sha`；落后 HEAD 超过 50 commits 给 warning。
  - Test: `test_doctor_warns_when_last_converged_sha_is_over_50_commits_behind`.

### P1 — Human UAT sign-off
- `PROJECT.toml` 新增 `[release].uat_signed_by`；`LIFECYCLE.md` G3 增加人工 UAT 签字；doctor 对 G3+ 强制非空。
  - Test: `test_g3_requires_human_uat_signoff`.

### P1 — WP timebox
- `WORK_PACKET.md` 新增 `timebox`；`COMPILER.md` 给 L1 半天、L2 1–3 天、L3 按周的规划参考，并明确不是硬限制。
  - Test: `test_wp_template_and_compiler_include_timebox_guidance`.

### P2 — Low-churn additions included
- `IMPLEMENTATION_ENTRY.md` 新增 `agent_model_tier` guidance；机械性 WP 可使用较弱模型，架构/安全/迁移/跨模块 WP 优先强模型，且模型等级不能降低 Gate。
  - Test: `test_p2_agent_model_tier_guidance_exists`.
- `LIFECYCLE.md` 新增 Sunset / Retirement：README 替代指引、native truth 下架、消费者迁移、归档与审计历史。
  - Test: `test_p2_sunset_flow_exists`.
- `WORK_PACKET.md` 新增 `issue_ref`，`DELIVERY.md` 定义 issue tracker 映射规则。
  - Test: `test_p2_issue_tracker_mapping_exists`.
- `README.md` 新增“项目复盘反哺”闭环：repeatable spec pattern / blind spot / invalid rule 以证据 + 回归测试进入 skill。
  - Test: `test_p2_retrospective_feedback_loop_exists`.

### Intentionally deferred
- P2 “模板标题统一语言”未在 1.0.2 执行：它是大面积文案 churn，当前无功能缺陷证据，且会增加回归噪声。doctor 继续保持语言无关结构检查。

### Release-candidate portability hardening
- `doctor.py` 的 secret 命中路径统一输出 POSIX `/` 分隔符，避免 Windows 上 `contracts\leak.txt` 与跨平台测试/日志格式漂移。
  - Regression tests: `test_doctor_scans_contracts_for_secrets`, `test_selftest_ci_covers_windows_and_linux`；CI matrix 现在同时覆盖 `ubuntu-latest` 与 `windows-latest`，Python 3.11 / 3.13。

### Package / compatibility evidence
- `VERSION = 1.0.2`；`SKILL.md`、`PROJECT.toml` template、三个 golden example 的 standard 版本同步。
  - Tests: `test_version_is_consistent`, `test_skill_progressive_disclosure_limits`, `test_all_references_are_indexed_from_skill`.
- 保留并继续通过 1.0.1 的初始化、幂等、G0/G1、unknown/exception、golden example、package hygiene 回归测试。
  - Tests: `test_init_project_renders_valid_toml`, `test_init_is_idempotent_and_does_not_overwrite`, `test_init_engineering_pack_moves_status_to_draft`, `test_doctor_g0_skeleton_pass_is_scoped`, `test_doctor_g1_rejects_uncompiled_draft`, `test_g1_blocks_unknowns`, `test_g1_validates_exception_fields`, `test_gitignore_excludes_python_cache`.

## 1.0.1 — Baseline Hardening

这是 V1.0.0 的质量加固版本，不改变核心工作流。

### Tooling / Evidence
- 新增可执行 `unittest` 自测和 GitHub Actions self-test。
- 新增可通过 G1 doctor 的 `examples/mini-ticket-triage/` golden example。
- `doctor.py` 明确只证明 declared-stage structural/readiness，不再暗示功能正确。
- G1 增加机器可读 `sps:readiness` Gate、Work Packet 最小要求、Brownfield baseline 要求。

### Consistency
- Engineering Pack 状态只以 `PROJECT.toml [engineering_pack].status` 为权威。
- `ENGINEERING_INDEX.md` 不再维护第二份 pack status；`IMPLEMENTATION_ENTRY.md` 改用独立 `entry_state`。
- `unknowns.items` 与 `[[exception]]` 纳入 doctor 校验。
- 增加 `artifact_paths`，明确 Spec / LLD / WP / ADR / Change / Handover / PR template 的默认落位。
- Engineering Index 表格增加真实 Path 列。

### Robustness
- `init_project.py` 改为专用 token rendering，并在落盘前用 `tomllib` 验证，避免依赖模板空格/整行字符串替换。
- `init_engineering_pack.py` 创建 Pack 后安全推进 `NOT_COMPILED → DRAFT`，并校验 TOML。
- doctor 移除对英文标题/短语的硬编码内容匹配，改用语言无关 readiness marker 和结构字段。
- 补全 SKILL reference index；SKILL 主入口压缩，更多细节通过 progressive disclosure 按需读取。
- 扩充 Coverage 判定标准。

### Packaging
- 移除 `__pycache__` / `.pyc`。
- 新增 `.gitignore`。
- 新增保守 LICENSE（All Rights Reserved；公开分发前可由所有者替换）。

## 1.0.0 — First Stable Baseline

首次统一稳定基线。此前 V1/V1.1/V2/V3.x 均视为 pre-1.0 内部设计迭代，不作为正式发布历史。
