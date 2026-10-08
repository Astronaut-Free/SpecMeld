<!-- sps:readiness=READY -->
# Product Current Truth — Legal Consult Mini App

## Problem & Users
Users need a low-friction way to describe a legal question, receive a bounded informational AI response, and decide whether to request human follow-up.

## Scope
V1 supports consent, text question intake, advisory AI answer, source/limitation notice, and callback request. It does not provide binding legal conclusions, autonomous filing, evidence strategy, or payment collection.

## Core User Flow
Consent → enter question → create consult session → AI answer with uncertainty/limits → optional human callback request → history view.

## Business Rules
AI output is informational and must not present itself as a lawyer. High-risk or unsupported requests route to human follow-up. Sensitive fields are minimized and access is role-scoped.

## Mini-program UX Constraints
The experience must define permission prompts, weak-network retry, loading/error states, package-size boundaries, version compatibility, and review-safe copy before submission to the mini-program platform.

## NFR / Architecture Drivers
Initial target is under 1,000 daily active users. Question submission must not be lost during model outage. PII must not be included in logs. Model completion is asynchronous and may take up to 15 seconds without blocking session creation.

## Acceptance Criteria
A user can submit after consent, receive either an advisory answer or a clear human-review fallback, recover from weak-network retry without duplicate consults, and never expose another user's session.
