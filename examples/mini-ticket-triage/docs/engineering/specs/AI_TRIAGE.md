# AI Triage Engineering Spec

status: APPROVED
owner: Engineering Owner

## Purpose
Generate advisory `category`, `priority`, and `confidence` from ticket text.

## Contract
Input: ticket id and text. Output: category enum, priority enum, confidence 0..1, analysis version. Confidence below 0.70 maps to `NEEDS_REVIEW`.

## Failure
Timeout, malformed output, or provider error produces `NEEDS_REVIEW`; no autonomous customer-facing action is allowed.

## Eval
Golden set must cover normal tickets, ambiguous text, empty/short text, and provider failure. Regression in invalid-output rate blocks release.
