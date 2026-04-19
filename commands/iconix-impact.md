---
description: "Analyze downstream impact of changing an upstream artifact. Usage: /iconix-impact REQ-042"
argument-hint: "<ARTIFACT-ID>"
---

Invoke the iconix-traceability agent with the argument: $ARGUMENTS

Ask it to produce a change impact report showing every downstream artifact (UC, RB, SD, CLS, TC) that depends on $ARGUMENTS, ordered by blast radius. Do not modify any artifacts — analysis only.
