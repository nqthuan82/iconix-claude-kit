---
description: Run the full ICONIX pipeline on the next unprocessed use case
---

Invoke the iconix-orchestrator agent. Tell it:

"Pick the next use case in `use-cases/` that has no robustness diagram yet, or if all UCs are processed, pick the next UC with no sequence diagram. Route the work through the appropriate agents (Analyst → Architect → Developer → Tester) in order. After each agent finishes, invoke the iconix-traceability agent to validate. Stop before any milestone gate and produce a readiness report — do not auto-approve gates."
