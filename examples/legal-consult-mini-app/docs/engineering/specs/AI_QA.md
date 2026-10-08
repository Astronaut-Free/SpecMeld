# AI Q&A Engineering Spec

status: APPROVED
owner: Engineering Owner

## Purpose
Generate an informational answer from user-provided text without claiming professional representation or taking autonomous legal action.

## Output Contract
Return answer text, limitation notice, confidence/risk classification, and whether human follow-up is recommended. Unsupported or provider-failed cases become `HUMAN_REVIEW`.

## Eval
Golden cases cover common civil questions, ambiguous facts, requests requiring professional judgment, prompt-injection attempts, and provider failure. Any unsafe autonomy or hidden-data disclosure blocks release.
