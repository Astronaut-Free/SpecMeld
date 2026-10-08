<!-- sps:readiness=READY -->
# Implementation Plan

owner: Engineering Owner
baseline: greenfield

## Target State
A secure mini-program vertical slice where session creation survives AI outage and every AI response has a bounded fallback.

## Dependency DAG
`WP-001`

## Delivery Strategy
Implement contract and authorization boundary first, then session persistence and async AI behavior, then mini-program weak-network and release checks.
