<!-- sps:readiness=READY -->
# Coding Agent Implementation Entry

entry_state: READY
baseline_sha: greenfield
base_branch: main
current_wp: `docs/engineering/work/WP-001.md`
agent_model_tier: strong

## Mission
Build the consent → consult session → advisory AI/fallback vertical slice without adding payment collection or autonomous legal actions.

## Read First
1. `docs/engineering/work/WP-001.md`
2. `docs/engineering/specs/SECURITY_PRIVACY.md`
3. `docs/engineering/specs/AI_QA.md`
4. `docs/engineering/specs/MOBILE_MINI_PROGRAM.md`
5. `contracts/openapi.yaml`

## Stop Conditions
Stop for new PII categories, payment scope, public sharing, or any AI behavior that changes the advisory-only rule.
