# Change Impact Report — CI-<date>

## Trigger
- **Changed artifact:** REQ-XXX | UC-XXX
- **Change summary:** <one sentence describing what changed>
- **Requested by:** <stakeholder / ticket>

## Blast radius

```
REQ-XXX (changed)
  └─► UC-XXX, UC-YYY          (UCs citing this REQ)
        ├─► RB-XXX, RB-YYY    (robustness diagrams for those UCs)
        │     └─► SD-XXX      (sequence diagrams citing those RBs)
        │           └─► CLS-<Name>
        │                 └─► TC-XXX, TC-YYY
        └─► UC-ZZZ            (other UCs sharing affected classes)
```

## Affected artifacts (flat list, ordered by blast radius)

| ID | Type | File | Action required |
|---|---|---|---|
| UC-XXX | Use Case | `use-cases/UC-XXX-<slug>.md` | Update two-column flow |
| RB-XXX | Robustness | `robustness/RB-XXX-<slug>.puml` | Redraw affected elements |
| SD-XXX | Sequence | `sequence/SD-XXX-<slug>.puml` | Update affected messages |
| TC-XXX | Test Case | `test-cases/TC-XXX-<slug>.md` | Revise steps/expected results |

## Artifacts NOT affected
<list any artifacts in the chain that were analysed and confirmed unchanged, or "none">

## Recommended dispatch order
1. Product Owner — update UCs listed above (Change mode)
2. M1 gate — Traceability re-validates REQ→UC links
3. Analyst — update RBs listed above (Change mode)
4. M2 gate — Traceability re-validates UC→RB links
5. Developer + Tester in parallel — update SDs and TCs (Change mode)
6. M3 gate — Traceability re-validates SD→CLS→TC links
