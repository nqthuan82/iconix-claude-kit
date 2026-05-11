---
description: Run the full ICONIX pipeline on the next unprocessed use case
---

Invoke the iconix-orchestrator agent. Tell it:

"Pick the next use case in `use-cases/` that has no robustness diagram yet, or if all UCs are processed, pick the next UC with no sequence diagram. Route the work through the appropriate agents (Analyst → Architect → Developer → Tester) in order. After each agent finishes, invoke the iconix-traceability agent to validate.

**Gate protocol — apply at M1, M2, and M3 without exception:**
1. Run Traceability to produce the readiness report for that gate.
2. STOP. Print the readiness report and the gate name (e.g., `## Milestone 1: Requirements Review — waiting for approval`).
3. Wait for the user to type an explicit approval (e.g., 'approve', 'proceed', 'yes', or similar) before dispatching any downstream agent.
4. Do NOT auto-approve any gate, regardless of how clean the readiness report looks.

Do not proceed to Phase 9 (implementation) until the user has explicitly approved M3."
