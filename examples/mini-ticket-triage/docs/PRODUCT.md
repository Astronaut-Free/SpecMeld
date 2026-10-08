<!-- sps:readiness=READY -->
# Product Current Truth — Mini Ticket Triage

## Problem & Users
Support agents receive text tickets and need a consistent first-pass category and priority suggestion without replacing human judgment.

## Scope
Users can create a ticket, receive an AI suggestion, override it, and inspect the final stored result. No auto-closing, customer messaging, or autonomous action is in scope.

## Core Flow
Create ticket → persist ticket → request async triage → show pending → show suggestion with confidence → agent confirms/overrides → persist final category/priority.

## Business Rules
AI output is advisory. Low-confidence or provider-failure results become `NEEDS_REVIEW`. Human confirmation is authoritative.

## NFR / Architecture Drivers
Target: internal team under 100 concurrent users, normal response under 300 ms excluding async model completion, model result target under 10 s, no need for microservices, provider outage must not block ticket creation.

## Acceptance
Ticket creation always succeeds when DB is healthy; AI outage degrades to manual review; every final classification records whether it was AI-accepted or human-overridden.
