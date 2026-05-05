# ICONIX Claude Code Kit

A reusable set of Claude Code sub-agents and commands that apply the ICONIX
software-development process (Rosenberg & Stephens) to any project.

## What's inside

```
iconix-kit/
├── iconix-init              # installer CLI (bash)
├── iconix-init.ps1          # installer CLI (PowerShell)
├── iconix-state-machine.puml  # PlantUML state machine of the full kit workflow
├── agents/                  # Claude Code sub-agent definitions
│   ├── iconix-orchestrator.md
│   ├── iconix-product-owner.md
│   ├── iconix-analyst.md
│   ├── iconix-architect.md
│   ├── iconix-developer.md
│   ├── iconix-tester.md
│   ├── iconix-traceability.md
│   ├── iconix-reviewer.md     # code ↔ design drift detection
│   ├── iconix-docs.md         # user / dev / API doc generation
│   └── iconix-migration.md    # retrofit ICONIX onto legacy code (Graphify-aware in v0.3.0+)
├── commands/                # Claude Code slash commands
│   ├── iconix-next.md
│   ├── iconix-status.md
│   ├── iconix-impact.md
│   ├── iconix-review.md
│   ├── iconix-docs.md
│   ├── iconix-migrate.md
│   └── iconix-graphify.md     # bootstrap Graphify integration (optional)
└── templates/               # per-project templates
    ├── iconix.config.yaml
    ├── req-template.md          # atomic requirement
    ├── use-case-template.md
    ├── robustness-template.puml # includes UC scenario text as comment block
    ├── sequence-template.puml   # UC steps as group blocks
    ├── test-case-template.md
    ├── test-plan-template.md
    ├── adr-template.md          # architecture decision record
    ├── change-impact-template.md
    └── graphify-setup.md        # Graphify integration setup guide
```

## Install into a project

```bash
# Option A: from a local clone of this kit
./iconix-init --source /path/to/iconix-kit --prefix MYPRJ --language csharp

# Option B: globally (agents available in every project on your machine)
./iconix-init --global --source /path/to/iconix-kit

# Option C: from a git repository
./iconix-init --source https://github.com/your-org/iconix-claude-kit.git --prefix ACME
```

## Project scope vs user scope

- **Project scope** (`./iconix-init`): installs into `./.claude/` and seeds
  `iconix.config.yaml` + the ICONIX folder structure. Recommended when
  different projects have different prefixes, stacks, or architectures.
- **User scope** (`--global`): installs into `~/.claude/` — agents are
  available in every project on your machine, but configuration is
  still per-project via `iconix.config.yaml`.

When both scopes define the same agent, project scope wins (Claude Code behavior).

## Required tooling

- [Claude Code](https://docs.claude.com/en/docs/claude-code/overview) installed and authenticated
- `bash`, `git`, `sed` (standard on macOS/Linux; use WSL on Windows)
- Optional: a PlantUML renderer for diagrams

## Per-project configuration

Edit `iconix.config.yaml` at your project root:

- `project.prefix` — ID prefix (e.g., `RGS` → `RGS-UC-017`)
- `stack.language` + `stack.test_framework` — drives Developer & Tester output
- `architecture.containers` — list of containers the Architect maps UCs to
- `milestones.max_revisions_per_artifact` — anti-analysis-paralysis guardrail

## Usage

In Claude Code:

```text
/agents                 # confirm agents loaded
/iconix-next            # next pipeline step
/iconix-status          # milestone readiness
/iconix-impact REQ-042  # downstream impact of a change
```

Or invoke agents explicitly:

> "Use the iconix-product-owner agent to draft use cases from stakeholder-notes.md"
> "Use the iconix-analyst agent to produce robustness diagrams for UC-017 and UC-018"

## How agents hand off

Every artifact ends with a `## Traceability` block citing upstream IDs. The
`iconix-traceability` agent validates these links at every milestone gate.
If a link is missing or an ID is reused, downstream work is frozen until the
issue is resolved.

## Command → Agent communication flow

### Command routing

| Command | Dispatches to | Purpose |
|---|---|---|
| `/iconix-next` | Orchestrator → current phase agent | Advance the pipeline one step |
| `/iconix-status` | Traceability (read-only) | Artifact inventory, NFR coverage, test matrix, open CI reports, milestone readiness, next action |
| `/iconix-impact <ID>` | Traceability | Downstream blast-radius of a change |
| `/iconix-review` | Reviewer | Code ↔ design drift on current git diff |
| `/iconix-docs <type> [scope]` | Docs | Generate user / dev / API / release / ops docs |
| `/iconix-migrate [path]` | Migration | Reverse-engineer ICONIX artifacts from legacy code |
| `/iconix-graphify` | Migration setup | Bootstrap Graphify graph and patch config |

### `/iconix-next` pipeline

The Orchestrator inspects the current artifact state and dispatches to whichever phase is
incomplete. It never produces artifacts itself.

```
/iconix-next
  └─► Orchestrator
          │
          ▼
   [phase detection]
          │
          ├─► Product Owner    — draft REQs, UCs, glossary
          │        │
          │    [M1 gate] ── Traceability ── validates REQ→UC links; freezes on failure
          │
          ├─► Analyst          — robustness diagrams, domain model
          │
          ├─► Architect        — container mapping, NFRs, ADRs, testability seams
          │        │
          │    [M2 gate] ── Traceability ── validates UC→RB→container links;
          │                                 checks every NFR cited by ≥1 ADR
          │
          ├─► Developer        — sequence diagrams, class model, code skeletons
          │
          ├─► Tester           — test cases, Gherkin, coverage matrix, test plan
          │        │
          │    [M3 gate] ── Traceability ── validates SD→CLS→TC links;
          │                                 checks test-plan exists and is complete
          │
          └─► (done — all phases complete)
```

Traceability runs **at every gate**, not just at the end. If a link is missing or an ID is
reused, it freezes downstream work until resolved.

### Handling a new REQ that affects existing use cases (Change mode)

When a `new` or `changed` requirement touches use cases that already have downstream artifacts
(robustness diagrams, sequence diagrams, test cases), the pipeline does **not** restart
from scratch — only the affected slice is updated.

**Step 1 — Run impact check before touching anything**

```text
/iconix-impact REQ-XXX
```

Traceability maps the full blast radius and produces `change-impact/CI-<date>.md`:

```
New/changed REQ-XXX
  └─► UC-005, UC-012, UC-019        (UCs that cite this REQ)
        ├─► RB-005, RB-012, RB-019  (robustness diagrams for those UCs)
        │     └─► SD-008, SD-014    (sequence diagrams citing those RBs)
        │           └─► CLS-PaymentService, CLS-OrderCart
        │                 └─► TC-022, TC-031, TC-047
        └─► any other UC sharing the affected classes → also flagged
```

**Step 2 — Product Owner updates requirements and affected UCs**

- Creates `REQ-XXX.md` for the new requirement
- Revises each affected UC's two-column flow
- Updates `## Traceability` block in each UC to cite the new REQ

**Step 3 — M1 gate re-runs (scoped to changed UCs)**

Traceability re-validates only the touched UCs. Freezes downstream if any check fails.

**Step 4 — Analyst updates only the affected robustness diagrams**

Only `RB-005`, `RB-012`, `RB-019` — unaffected RBs are untouched.

**Step 5 — M2 gate re-runs (scoped)**

**Step 6 — Developer and Tester update in parallel (scoped)**

- Developer revises only the SDs and class model entries in the blast radius
- Tester revises only the TCs linked to the affected UCs

**Step 7 — M3 gate re-runs**

Full chain validated for the changed slice. Artifacts outside the blast radius are not
re-validated and do not block the gate.

> **Change mode:** The Orchestrator has a `# REQ change flow` that drives this entire
> sequence automatically via `/iconix-next`. Product Owner, Analyst, and Tester each have
> a `# Change mode` section — the Orchestrator passes the CI report path in its dispatch
> plan so each agent self-scopes to the blast radius only.
>
> **Brand new REQ (empty CI report):** If no UC currently cites the new REQ, Traceability
> produces an empty CI report. The Product Owner's change mode detects this, reads all
> existing UCs to identify candidates with semantic overlap, and presents a confirmed list
> to the user before editing anything. Uncertain candidates are flagged `[VERIFY]`.

### Handling a bug that affects existing use cases

Bugs must be triaged before routing — the defect may be in the code or in the design.
Never go straight to Developer without a triage step.

**Step 1 — Always triage first**

Invoke the Reviewer against the affected UC or source file. It classifies the bug in
a `## Bug triage` section of its report:

| Type | Meaning | Indicator |
|---|---|---|
| **Type 1 — Implementation bug** | Code diverges from a correct design | Code does not match the SD |
| **Type 2 — Design bug** | Design is wrong; code faithfully implements the wrong thing | Code matches the SD but behaviour is still wrong |

**Type 1 flow — implementation bug**

```
Reviewer (triage → Type 1)
  └─► Developer — bug fix mode
        │  fix code to match existing SD only; no artifacts change
        └─► Tester — bug verification mode
              re-run failing TCs; check for regressions in UCs sharing touched classes
```

No ICONIX artifacts change. Traceability chain stays intact.

**Type 2 flow — design bug**

```
Reviewer (triage → Type 2)
  └─► /iconix-impact UC-XXX (Traceability) → produces CI report
        └─► follow the REQ change flow from this point
              (Product Owner → M1 → Analyst → M2 → Developer + Tester → M3)
```

> **Bug modes:** Reviewer has a `# Bug triage` section; Developer has `# Bug fix mode`;
> Tester has `# Bug verification mode`. The Orchestrator's `# Bug flow` drives the full
> sequence automatically via `/iconix-next` when a bug is reported.
>
> **Review checklist:** After each review the Reviewer appends recurring defect patterns
> to `reviews/review-checklist.md`. Over time this becomes a project-specific checklist
> of the most common drift types, used to front-load future reviews.

### `/iconix-migrate` — code-walking vs. graph-assisted mode

```
/iconix-migrate [path]
  └─► Migration agent
          │
          ├─ knowledge_graph.enabled = false (default)
          │       └─► walk source code directly → 7-phase extraction
          │
          └─ knowledge_graph.enabled = true
                  └─► query Graphify graph (graphify-out/graph.json)
                          └─► faster extraction with provenance labels:
                              EXTRACTED / INFERRED / AMBIGUOUS
```

Enable graph-assisted mode with `/iconix-graphify` (builds the graph and patches
`knowledge_graph.enabled = true` in `iconix.config.yaml`).

### Migration → pipeline handoff

Migration is a **one-time bootstrap** for legacy codebases. It produces only DRAFTs;
the normal pipeline resumes once Traceability promotes them to permanent IDs.

```
[Legacy codebase]
  └─► Migration agent
          │
          ├─► migration/survey-<date>.md       }
          ├─► class-model/class-model.puml      }  all stamped DRAFT
          ├─► sequence/SD-DRAFT-*.puml          }  until human review
          ├─► robustness/RB-DRAFT-*.puml        }
          ├─► use-cases/UC-DRAFT-*.md           }
          └─► migration/coverage-gaps.md
                  │
                  ▼
          Traceability agent
          (human review → promotes DRAFT IDs to permanent REQ/UC/RB/SD/CLS IDs)
                  │
                  ▼
          Normal pipeline resumes
          Analyst → Architect → [M2 gate] → Developer → Tester → [M3 gate]
```

| Downstream agent | Consumes from Migration |
|---|---|
| **Traceability** | All DRAFT artifacts — re-allocates permanent IDs after review |
| **Analyst** | `UC-DRAFT-*.md`, `RB-DRAFT-*.puml` — validates and promotes through M1/M2 |
| **Architect** | `class-model.puml` — maps to containers, produces ADRs |
| **Developer** | `SD-DRAFT-*.puml`, `class-model.puml` — starting point for detailed design |
| **Tester** | `coverage-gaps.md` — identifies which use cases lack test coverage |

DRAFT IDs are **unstable** — downstream agents must not treat them as permanent until
Traceability has assigned real IDs.

## Plan mode

Claude Code's `/plan` toggle puts the session into read-only mode — `Write` and `Bash`
are blocked. ICONIX agents behave differently depending on whether they need to write
artifacts.

### Which agents work in plan mode

| Agent | Plan mode behaviour |
|---|---|
| **Orchestrator** | Full — reads artifact state and outputs a dispatch plan without writing |
| **Traceability** | Full — `/iconix-status` and `/iconix-impact` are read-only by nature |
| **Analyst, Architect, Developer, Tester, Reviewer, Docs, Product Owner** | Partial — can describe what they would produce but cannot write `.puml` / `.md` files to disk |
| **Migration** | Most restricted — loses both `Write` and `Bash`; can survey the codebase but cannot output any DRAFT artifacts |

### Recommended plan mode workflows

Use plan mode **before** committing to a pipeline step:

```text
/plan
/iconix-next          # Orchestrator shows what it would dispatch — review before approving
/iconix-status        # Traceability reads artifact state — works fully
/iconix-impact UC-017 # Blast-radius check — works fully
/plan                 # exit plan mode, then run the actual step
```

Avoid plan mode when you need artifacts written (robustness diagrams, sequence diagrams,
use cases, test cases). Exit plan mode first, then invoke the agent.

### Current limitation

ICONIX agents have no built-in plan mode awareness — they will simply stall at the first
`Write` call rather than gracefully switching to inline output. If you regularly use plan
mode for design review, consider adding a `# Plan mode` section to the relevant agent
files instructing them to emit artifact content inline when `Write` is unavailable.

## Updating the kit

Re-run the installer with `--force` to overwrite agent definitions. Your
`iconix.config.yaml` and generated artifacts are never touched.

## Portable across projects — what does and doesn't change

| Layer | Reusable across projects | Per-project |
|---|---|---|
| Agent system prompts | ✅ | |
| Sub-agent validators | ✅ | |
| Slash commands | ✅ | |
| ID schema | ✅ | ✅ prefix only |
| `iconix.config.yaml` | | ✅ |
| Architecture document | | ✅ |
| Glossary / domain model | | ✅ |
| Generated artifacts | | ✅ |

## Versioning

Treat this kit like any other dependency:

- Check agent files into the project repo (via `--source` at install time)
- Pin to a commit/tag when cloning from git
- When refining an agent, bump a version note in its frontmatter and
  document the change in a commit message

## Notation & abbreviations

### Traceability ID types

| Abbreviation | Full name | Description |
|---|---|---|
| `REQ` | Requirement | Functional or business requirement captured by the Product Owner |
| `UC` | Use Case | Actor–system interaction in two-column format |
| `RB` | Robustness Diagram | Boundary / Controller / Entity analysis linking UC to design |
| `SD` | Sequence Diagram | Detailed interaction diagram showing message flow between objects |
| `CLS` | Class | Class model element (used in traceability chain SD → CLS) |
| `TC` | Test Case | Verifiable test derived from a UC or SD |
| `CI` | Change Impact report | Blast-radius report produced by Traceability via `/iconix-impact`; filed as `change-impact/CI-<date>.md` |

### Process & methodology terms

| Abbreviation | Full name | Description |
|---|---|---|
| ICONIX | ICONIX Process | Lightweight OO software development methodology by Rosenberg & Stephens |
| NFR | Non-Functional Requirement | Quality attribute or constraint (performance[], availability[], security[], scalability[], compliance[], observability[]) |
| ADR | Architecture Decision Record | Documented architectural decision with context and consequences |
| M1 | Milestone 1 — Requirements Review | Gate: Traceability validates all REQ → UC links before analysis begins |
| M2 | Milestone 2 — Preliminary Design Review (PDR) | Gate: Traceability validates UC → RB → container links before detailed design |
| M3 | Milestone 3 — Critical Design Review (CDR) | Gate: Traceability validates SD → CLS → TC links before implementation |

### Technical abbreviations

| Abbreviation | Full name |
|---|---|
| CLI | Command-Line Interface |
| API | Application Programming Interface |
| WSL | Windows Subsystem for Linux |
| BRD | Business Requirements Document |

## What the kit intentionally does not cover

These gaps are by design — they require human judgment, physical meetings, or tooling outside Claude Code's scope. Knowing they exist prevents teams from assuming the kit handles everything.

| Gap | Why it's out of scope | Recommended practice |
|---|---|---|
| **UI storyboards / screen mock-ups** | Wireframing requires a design tool; Claude Code cannot render or validate UI prototypes | Use Figma, Balsamiq, or hand-drawn sketches; attach images to UC files as references |
| **Stakeholder review meetings** | Requirements Review (M1) and PDR (M2) should include customers, end users, and marketing — the kit only produces the artifacts for those meetings | Run the meeting with human participants; use the kit's milestone report as the agenda |
| **Persona analysis** | Persona creation requires primary user research; no agent currently models this | Define personas externally and reference them in `iconix.config.yaml` or a `personas/` folder |
| **Effort estimation** | ICONIX recommends estimating from UC scenarios, not functional requirements — this requires team velocity data the kit cannot access | Count controllers per RB as a proxy for complexity; map to story points manually |
| **Code header / stub generation** | Generating compilable code skeletons from class diagrams is language- and framework-specific | Use IDE code-generation features seeded from `class-model.puml` |
| **TDD red-green-refactor cycle** | The kit derives TCs from RBs before coding, which sets up test-first thinking, but it does not drive the red-green loop | Write the generated TC stubs as failing tests before implementing the corresponding SD operations |

## Philosophy

Faithful to ICONIX's minimalism: ten agents, seven commands, one pipeline.
No ceremony beyond what drives the work from use case to code.
