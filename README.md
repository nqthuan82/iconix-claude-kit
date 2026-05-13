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
│   ├── iconix-git.md          # branch/PR/commit hygiene; provider-agnostic (v0.9.5+)
│   ├── iconix-metrics.md      # project metrics + audit-friendly snapshots (v0.9.7+)
│   ├── iconix-upgrade.md      # kit-version migration; never modifies project artifacts (v0.9.9+)
│   ├── iconix-docs.md         # user / dev / API doc generation
│   └── iconix-migration.md    # retrofit ICONIX onto legacy code (Graphify-aware in v0.3.0+)
├── commands/                # Claude Code slash commands
│   ├── iconix-next.md
│   ├── iconix-status.md
│   ├── iconix-impact.md
│   ├── iconix-review.md
│   ├── iconix-bug.md          # bug triage entry point (Type 1 vs Type 2)
│   ├── iconix-pr.md           # open phase-appropriate PR (v0.9.5+)
│   ├── iconix-trace-check.md  # local trace validation, mirrors CI gate (v0.9.5+)
│   ├── iconix-concurrent.md   # detect class-level conflicts between in-flight UCs (v0.9.6+)
│   ├── iconix-metrics.md      # produce metrics snapshot (markdown + JSON) (v0.9.7+)
│   ├── iconix-upgrade.md      # migrate kit installation to current version (v0.9.9+)
│   ├── iconix-docs.md
│   ├── iconix-migrate.md
│   └── iconix-graphify.md     # bootstrap Graphify integration (optional)
└── templates/               # per-project templates
    ├── iconix.config.yaml
    ├── req-template.md          # atomic requirement
    ├── use-case-template.md
    ├── use-case-diagram-template.puml   # one PlantUML diagram per UC package
    ├── domain-model-initial-template.puml  # PO's initial domain model draft (v0.9.10+)
    ├── robustness-template.puml # includes UC scenario text as comment block
    ├── sequence-template.puml   # UC steps as group blocks
    ├── test-case-template.md
    ├── test-plan-template.md
    ├── adr-template.md          # architecture decision record
    ├── container-mapping-template.md       # per-UC container mapping (v0.9.14+)
    ├── nfr-annotations-template.md         # per-UC NFR enforcement (v0.9.14+)
    ├── nfr-catalog-template.md             # project-wide NFR catalog (v0.9.14+)
    ├── system-architecture-template.md        # canonical architecture doc scaffold (C4-flavoured)
    ├── architecture-package-map-template.md  # CODE/deployment packages (v0.9.14+)
    ├── integration-surface-template.md     # external touchpoints (v0.9.14+)
    ├── milestone-report-template.md        # M1/M2/M3 readiness format (v0.9.18+)
    ├── class-model-template.puml           # detailed static model (v0.9.19+)
    ├── cdr-report-template.md              # per-UC M3 readiness report (v0.9.19+)
    ├── edge-case-report-template.md        # per-UC edge-case enumeration (v0.9.20+)
    ├── test-matrix-template.md             # living REQ↔UC↔TC matrix (v0.9.20+)
    ├── feature-template.feature            # Gherkin BDD feature file scaffold (v0.9.48+)
    ├── change-impact-template.md
    ├── graphify-setup.md        # Graphify integration setup guide
    ├── intake-transcript-template.md   # stakeholder interview / meeting notes
    ├── intake-brd-template.md          # Business Requirements Document
    ├── intake-email-template.md        # email or written request
    ├── intake-feature-request-template.md  # feature request / ticket / user story
    ├── bug-report-template.md          # optional structured input for /iconix-bug
    ├── concurrent-touch-template.md    # M2-gate concurrent-touch report format (v0.9.6+)
    ├── phase9-cycle-template.md        # optional Phase 9 cycle log format (v0.9.8+)
    ├── metrics-snapshot-template.md    # markdown format for metrics snapshots (v0.9.7+)
    ├── metrics-schema.json             # JSON schema for snapshot output (v0.9.7+)
    ├── upgrade-report-template.md      # kit-version upgrade report format (v0.9.9+)
    ├── handoff-report-template.md      # migration handoff report format (v0.9.44+)
    └── git-integration/                # v0.9.5+ — provider-agnostic + provider-specific
        ├── README.md
        ├── branch-conventions.md       # branch naming reference (any provider)
        ├── commit-conventions.md       # commit message format (any provider)
        ├── generic/
        │   └── validate-traceability.sh   # core merge-gate validator
        ├── github/                     # workflows + PR templates (per phase)
        └── azure-devops/               # pipeline + PR templates (per phase)
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

### Multi-repo / microservices (v1.0.0+)

When each container lives in its own git repository (cloned locally), add `path:` per container:

```yaml
architecture:
  containers:
    - name: "OrderService"
      path: "../order-service"          # local clone path
      git_url: "https://github.com/org/order-service"  # for /iconix-pr
      src_dir: "src"                    # default; omit if your layout matches
      test_dir: "tests"                 # default; omit if your layout matches
      reviewers: ["@team-a"]            # optional PR reviewers
```

- Agents resolve source at `<path>/<src_dir>/` and tests at `<path>/<test_dir>/`
- Containers without `path:` fall back to `./src/<ContainerName>/` (single-repo behaviour unchanged)
- Cross-container system tests and BDD step definitions live in the meta-project under `meta.system_tests_dir` / `meta.acceptance_tests_dir`
- The migration agent in multi-repo mode walks each container's source root independently and produces a unified survey
- The git agent syncs all repos at Phase entry: shows a per-repo plan, waits for confirmation, then creates the same feature branch in every repo simultaneously. Set `base_branch:` on a container to override `git.default_branch` for that repo (e.g., `develop` in gitflow services).
- `/iconix-pr` opens one PR per unique `path:` at Implementation phase (plus one meta-project PR for traceability artifacts); M1/M2/M3 always use a single meta-project PR
- Mixed topology (multiple containers in one repo): use the same `path:` and different `src_dir:` subdirectories — the git agent treats them as one repo and creates one branch + one PR
- Developer and Tester agents resolve the correct source/test root per container (`<path>/<src_dir>/` and `<path>/<test_dir>/`); unit and integration tests go to the container repo, system and acceptance tests go to the meta-project
- The traceability CI script supports `ICONIX_CONFIG_PATH` for service repo pipelines — set it to the meta-project checkout so the script resolves artifact folders (use-cases/, robustness/, etc.) from the right location

## Project layout

After `iconix-init` the project gains two layers: **kit machinery** (agents, commands, templates installed once) and **artifact scaffolding** (empty directories the pipeline fills over time).

### Kit machinery — installed by `iconix-init`

```
.claude/
├── agents/                          ← 13 agent definitions
│   ├── iconix-orchestrator.md
│   ├── iconix-product-owner.md
│   ├── iconix-analyst.md
│   ├── iconix-architect.md
│   ├── iconix-developer.md
│   ├── iconix-tester.md
│   ├── iconix-traceability.md
│   ├── iconix-reviewer.md
│   ├── iconix-git.md
│   ├── iconix-metrics.md
│   ├── iconix-upgrade.md
│   ├── iconix-docs.md
│   └── iconix-migration.md
└── commands/                        ← 13 slash commands
    ├── iconix-next.md               /iconix-next
    ├── iconix-status.md             /iconix-status
    ├── iconix-impact.md             /iconix-impact
    ├── iconix-review.md             /iconix-review
    ├── iconix-bug.md                /iconix-bug
    ├── iconix-pr.md                 /iconix-pr
    ├── iconix-trace-check.md        /iconix-trace-check
    ├── iconix-concurrent.md         /iconix-concurrent
    ├── iconix-metrics.md            /iconix-metrics
    ├── iconix-upgrade.md            /iconix-upgrade
    ├── iconix-docs.md               /iconix-docs
    ├── iconix-migrate.md            /iconix-migrate
    ├── iconix-promote.md            /iconix-promote
    └── iconix-graphify.md           /iconix-graphify

docs/iconix/
├── metrics-glossary.md
└── templates/                       ← all kit templates (reference copies for agents)
    ├── req-template.md
    ├── use-case-template.md
    ├── use-case-diagram-template.puml
    ├── domain-model-initial-template.puml
    ├── robustness-template.puml
    ├── sequence-template.puml
    ├── class-model-template.puml
    ├── container-mapping-template.md
    ├── nfr-annotations-template.md
    ├── nfr-catalog-template.md
    ├── architecture-package-map-template.md
    ├── integration-surface-template.md
    ├── adr-template.md
    ├── milestone-report-template.md
    ├── cdr-report-template.md
    ├── test-case-template.md
    ├── test-matrix-template.md
    ├── test-plan-template.md
    ├── edge-case-report-template.md
    ├── feature-template.feature
    ├── change-impact-template.md
    ├── concurrent-touch-template.md
    ├── bug-report-template.md
    ├── phase9-cycle-template.md
    ├── metrics-snapshot-template.md
    ├── metrics-schema.json
    ├── system-architecture-template.md
    ├── upgrade-report-template.md
    ├── handoff-report-template.md
    ├── graphify-setup.md
    ├── intake-transcript-template.md
    ├── intake-brd-template.md
    ├── intake-email-template.md
    ├── intake-feature-request-template.md
    └── git-integration/
        ├── README.md
        ├── branch-conventions.md
        └── commit-conventions.md

.ci/
├── validate-traceability.sh         ← CI merge-gate validator (always installed)
└── scripts/                         ← only if git.provider = github | azure-devops
    ├── setup-branch-protection.sh   ← github only: enforce CI gates as required checks
    └── setup-branch-policies.sh     ← azure-devops only: enforce CI gates as branch policies

.github/                             ← only if git.provider = github
├── pull_request_template.md         ← default PR template
├── workflows/
│   └── iconix-validate.yml
└── PULL_REQUEST_TEMPLATE/
    ├── m1.md
    ├── m2.md
    ├── m3.md
    └── implementation.md

.azuredevops/                        ← only if git.provider = azure-devops
└── pull_request_templates/
    ├── default.md
    ├── m1.md / m2.md / m3.md / implementation.md

docs/architecture/
└── system-architecture.md           ← seeded from template; fill in before running Architect

iconix.config.yaml                   ← project config (root)
```

### Artifact directories

Directories marked **[install]** are created empty by `iconix-init`. Directories marked **[agent]** are created on demand the first time the relevant agent runs — they will not exist until that phase is reached.

```
Phase 1 — Requirements (M1)
  requirements/    [install]  REQ-XXX-<slug>.md
  use-cases/       [install]  <PREFIX>-UC-XXX-<slug>.md
  use-case-packages/ [install] <package-slug>.puml

Phase 2 — Analysis / Preliminary Design (M2)
  domain-model/    [install]  domain-model.puml
  robustness/      [install]  RB-XXX-<slug>.puml
  container-mapping/ [install] <PREFIX>-UC-XXX-containers.md
  nfr-annotations/ [install]  <PREFIX>-UC-XXX-nfr.md
  adrs/            [install]  <PREFIX>-ADR-XXX-<slug>.md
  docs/architecture/ [install] package-map.md, integration-surface.md

Phase 3 — Detailed Design (M3)
  sequence/        [install]  SD-XXX-<slug>.puml
  class-model/     [install]  class-model.puml
  test-cases/      [install]  TC-XXX-<slug>.md
  features/        [install]  UC-XXX.feature      ← BDD projects or acceptance-bdd TCs
  test-plan/       [agent]    test-plan-<date>.md
  edge-case-reports/ [agent]  <PREFIX>-UC-XXX-edge-cases.md
  test-matrix.md   [agent]    root level; single living document

Phase 9 — Implementation
  src/<container-name>/  [agent]  source files; one folder per container; language per Effective stack
                                  ‣ multi-repo: code goes to <path>/<src_dir>/ in each container's
                                    external repo; meta-project src/ is empty (no source in meta)
  tests/<container-name>.Tests/ [agent]  unit/integration tests; mirrors src/
                                  ‣ multi-repo: tests go to <path>/<test_dir>/ in each container's
                                    external repo
  tests/SystemTests/    [agent]  cross-container system tests (multi-repo; meta.system_tests_dir)
  tests/AcceptanceTests/ [agent] BDD acceptance step definitions (multi-repo; meta.acceptance_tests_dir)

Audit trail and tracking
  reviews/         [agent]    REVIEW-<date>-<scope>.md, review-checklist.md
  change-impact/   [agent]    CI-<date>.md (REQ change), CT-<date>.md (concurrent-touch)
  bug-reports/     [agent]    BUG-<date>-<slug>.md
  milestone-reports/ [install] M1-<date>.md, M2-<date>.md, M3-<date>.md
  phase9-cycles/   [install]  UC-XXX-cycle.md     ← optional Phase 9 audit log per UC
  metrics/         [install]  snapshot-<date>.md, snapshot-<date>.json, trend-<date>.md
  upgrades/        [install]  upgrade-<from>-to-<to>-<date>.md

Traceability (root level — accessible by all agents without path resolution)
  ids.registry.md  [agent]
  traceability-matrix.md [agent]
  orphan-report.md [agent]

Migration (legacy codebases only — produced by /iconix-migrate)
  migration/       [agent]    survey-<date>.md, coverage-gaps.md, handoff-<date>.md
```

## Usage

In Claude Code:

```text
/agents                 # confirm agents loaded
/iconix-next            # next pipeline step
/iconix-status          # milestone readiness
/iconix-impact REQ-042  # downstream impact of a change
```

Or invoke agents explicitly:

> "Use the iconix-product-owner agent to process this stakeholder transcript: [paste text]"
> "Use the iconix-product-owner agent to process this feature request: [paste ticket]"
> "Use the iconix-product-owner agent to draft use cases from the intake form in docs/iconix/templates/"
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
| `/iconix-bug <ref>` | Reviewer (bug-triage mode) | Classify a bug as Type 1 (code defect) or Type 2 (design defect); recommend next step |
| `/iconix-pr [draft\|ready] [--reviewers ...]` | Git | Open a phase-appropriate PR (M1/M2/M3/Impl) on the configured provider |
| `/iconix-trace-check [<base>]` | Git | Run the traceability validator locally (same checks as the CI merge-gate) |
| `/iconix-concurrent [<UC-ID>]` | Traceability (concurrent-touch mode) | Detect class- and container-level conflicts between in-flight UCs at M2 (or any time) |
| `/iconix-metrics [trend]` | Metrics | Produce snapshot (markdown + JSON) of throughput, cycle time, quality, process compliance; `trend` arg for delta vs. prior snapshot |
| `/iconix-upgrade [--dry-run]` | Upgrade | Migrate the project's installed kit version to current; auto-applies safe additive changes; produces detect-and-report for project artifacts |
| `/iconix-docs <type> [scope]` | Docs | Generate user / dev / API / release / ops docs |
| `/iconix-migrate [path]` | Migration | Reverse-engineer ICONIX artifacts from legacy code |
| `/iconix-promote [slug\|all]` | Migration | Promote reviewed DRAFTs to permanent IDs; runs after human review of migration output |
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
          ├─► Git Agent        — suggest feature/UC-XXX-<slug> branch name; STOP for user
          │                      confirmation; git checkout -b (once per UC, at M1 entry)
          │
          ├─► Product Owner    — intake checklist → draft REQs, initial domain model, UCs, glossary
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
          ├─► Implementation loop  — Phase 9: 9.1 kickoff → 9.2 pre-merge drift → 9.3 fix → 9.4 merge
          │       (capped at phase9.max_iterations_per_uc; escalates to Architect / PO if hit)
          │
          └─► (done — release)
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

Invoke the Reviewer against the affected UC or source file — either via the dedicated
`/iconix-bug <ref>` command (direct entry point) or via `/iconix-next` (Orchestrator
detects the bug input and dispatches the Reviewer in triage mode automatically).

`/iconix-bug` accepts three argument forms, in increasing order of how much work the
Reviewer has to do up front to find the affected artifacts:

| Input form | Example | What the Reviewer does first |
|---|---|---|
| **UC-ID** | `/iconix-bug UC-017 customer says PlaceBet allows negative balance` | Reads the UC, then greps for source files with `Traceability: ... UC-017 ...` |
| **Source path** | `/iconix-bug src/Bet/BetController.cs returns 200 on insufficient funds` | Reads the file's `Traceability:` comment to find UC-XXX and SD-XXX |
| **Free-text only** | `/iconix-bug PlaceBet allows negative balance` | Asks the user for a file path or UC-ID — does not guess |

For larger bugs (extended repro, stack traces, multiple affected files), fill in
`docs/iconix/templates/bug-report-template.md`, save it as
`bug-reports/BUG-<date>-<slug>.md`, and pass the saved path to `/iconix-bug`. The
template has a dedicated section for exception / stack-trace input — the Reviewer
uses the top application frame in the trace as a direct anchor against SD methods.

It classifies the bug in a `## Bug triage` section of its report:

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

### Upgrading an existing installation (v0.9.9+) — `iconix-upgrade` agent

When the kit evolves (new templates, new agents, new config sections), existing projects can pick up the new features without losing their state. `/iconix-upgrade` does the migration safely.

**What it auto-applies** (additive, can't break existing behaviour):

- **Folders** — `mkdir -p` for any missing structural folder (e.g., `metrics/`, `phase9-cycles/`, `upgrades/`)
- **Config sections** — adds missing sections to `iconix.config.yaml` with **conservative defaults** (every new boolean toggle defaults to `false`, even if the kit's seeded template has `true`). The principle: the upgrade itself must not change runtime behaviour. You opt in by editing the config after reading the report.
- **Reference templates** in `docs/iconix/templates/` — refreshes the team-reference docs (warns before overwriting any user-edited copy)
- **CI / git integration files** — copied from kit source based on `git.provider` (skip if not set)

**What it never touches** (your authored content):

- `requirements/`, `use-cases/`, `robustness/`, `sequence/`, `class-model/`, `test-cases/`, `bug-reports/` — your artifacts
- `src/`, `tests/` — your code
- Existing values in `iconix.config.yaml` — only ADDS missing sections

**What it detects-and-reports** (Layer D — for human review):

- UCs missing newer `## Traceability` blocks or M1 checklist references
- Source files missing or using older `Traceability:` comment format
- Type 2 bug reports missing the `## Closure` section (introduced v0.9.8)
- Bug-fix branches not following the v0.9.5 naming convention
- Milestone reports in older formats

**Version detection:**

- Reads `iconix.config.yaml` `kit_version: "X.Y.Z"` field if present
- Otherwise, heuristic detection by feature presence (e.g., `phase9-cycles/` → v0.9.8+; `metrics/` → v0.9.7+; `concurrent-touch-template.md` → v0.9.6+)
- Override with `/iconix-upgrade --from 0.9.5` if heuristics are ambiguous

**Usage:**

```bash
# Preview the upgrade — produces report, applies nothing
/iconix-upgrade --dry-run

# Apply (writes to upgrades/upgrade-<from>-to-<to>-<date>.md)
/iconix-upgrade

# Override version detection
/iconix-upgrade --from 0.9.5
```

**Supported range:** v0.9.0 → current. Pre-v0.9.0 installations should do a fresh `iconix-init` instead.

**Distinct from `iconix-migration`:** the migration agent retrofits ICONIX *onto legacy code* (reverse-engineers source). Upgrade migrates the *kit version itself*. Different problems, different agents.

### Phase 9 — the implementation loop (v0.9.8+)

After M3 / CDR passes, the implementation phase isn't a black box ("Developer + Tester iterate") — it's a 4-sub-state loop owned by the Orchestrator, with explicit handoffs and an iteration cap.

```
9.1 Kickoff    │  Developer codes from SD + implements unit test bodies (from
               │  unit TCs); Tester implements integration/system/acceptance
               │  TCs + verifies unit coverage. Both on feature/UC-XXX-<slug>.
               │  Commits: [UC-XXX] Impl: <summary>.
   ▼
9.2 Pre-merge  │  Reviewer drift check. Verdict: APPROVE | APPROVE WITH NOTES |
   drift       │  REQUEST CHANGES | BLOCK MERGE.
   ▼
[if APPROVE / WITH NOTES]            [if REQUEST CHANGES / BLOCK MERGE]
   │                                              ▼
   │                                  9.3 Drift fix loop
   │                                  Developer fixes the specific findings;
   │                                  Tester re-runs affected TCs + regression.
   │                                  Back to 9.2.
   │                                  Capped at phase9.max_iterations_per_uc
   │                                  (default 5); escalate to Architect (if
   │                                  architectural) or PO (if scope-shaped).
   ▼
9.4 Merge      │  STOP: Git agent prints PR details — user confirms before PR opens.
               │  Draft PR opened via /iconix-pr.
               │  STOP: user confirms CI is green + PR approved.
               │  Orchestrator prints merge command — user runs it manually.
               │  UC moves to "Done" in /iconix-metrics.
```

**Configuration** (`iconix.config.yaml`):

```yaml
phase9:
  enabled: true
  max_iterations_per_uc: 5         # cap on the 9.2↔9.3 loop per UC
  reviewer_required_for_merge: true   # pre-merge drift check is mandatory
```

**Three new Reviewer modes:**

- **Pre-merge drift mode** (9.2) — full code↔SD↔class-model drift check on the PR diff
- **Bug-fix verification mode** (post-Type 1) — verify the *specific* drift the original triage flagged is actually closed
- **Type 2 closure mode** (post-REQ-change-flow) — re-confirm the original bug report against the new SD; appends a `## Closure` section to the bug report. **This closes the loop that opens when a Type 2 bug is filed** — without it, a fix could merge without anyone re-checking that it actually addressed the reported problem.

**Optional cycle log:** teams that want audit-grade evidence of the loop history can maintain `phase9-cycles/UC-XXX-cycle.md` per UC (template at `templates/phase9-cycle-template.md`).

**Methodology:** operationalizes book Ch10 #10 (drive code from design), #9 (if coding reveals design wrong, change it AND review the process), #8 (regular code inspections), #5 (if code gets out of control, revisit the design), #4 (keep design and code in sync), #3 (focus on unit testing while implementing), #1 (implement alternate courses too) — all already ✅ in the matrix; v0.9.8 just makes the loop routing explicit.

### Metrics & audit evidence (v0.9.7+) — `iconix-metrics` agent

The kit's artifact discipline produces signals teams can measure: throughput, cycle time, gate-failure rates, drift findings, process compliance. v0.9.7 ships an agent that scans the project's current state + git history and produces audit-friendly snapshots — markdown for humans, JSON for dashboards.

**What gets measured** (full glossary at `docs/iconix/metrics-glossary.md`):

| Category | Examples |
|---|---|
| **Throughput** | UCs by phase; REQs added; bug volume; Type 2 / total ratio |
| **Cycle time** | Days from M1 entry to M1 pass; M2→M3; branch-to-merge — derived from `[<UC>] <phase>: ...` commits |
| **Quality** | M1/M2/M3 gate-failure rates; drift findings per Implementation PR; concurrent-touch outcomes (HIGH resolved/accepted/unresolved) |
| **Process compliance** | % of UCs through all 3 gates; trace-comment coverage; REQ/UC linkage; NFR/ADR linkage. **Target ≥95%** for ISO audits. |
| **Trends** | Deltas vs. the previous snapshot, with directional indicators |

**Output:**

```
metrics/
├── snapshot-2026-05-09.md     # human-readable, audit-friendly
├── snapshot-2026-05-09.json   # validates against metrics-schema.json (v1.0)
└── trend-2026-05-09.md         # only on /iconix-metrics trend
```

The JSON conforms to a versioned schema (`templates/metrics-schema.json`), so dashboards built against v1.0 stay stable. Provider-neutral: hook your own viz onto the JSON — Power BI, Grafana, Azure Workbooks, GitHub Insights, anything that can read JSON.

**Configuration** (`iconix.config.yaml`):

```yaml
metrics:
  enabled: true
  output_dir: "metrics"
  ci_snapshot: false             # generate on push to main (CI integration)
  retention: 12                  # keep N most recent snapshot pairs
  git_history_window: "12 months"
```

**For ISO 27001 / 9001 audits:** the markdown snapshots are themselves audit artifacts. Preserve them under your retention policy. The four process-compliance metrics (UCs through all gates, trace-comment coverage, REQ/UC linkage, NFR/ADR linkage) are the bridge between *"we follow ICONIX"* and *"here's the evidence."*

**Why this is a kit extension over the canonical text:** Rosenberg's process doesn't prescribe project-wide metrics. Closest book references: Ch11 #6 ("Use data gathered during the review to accumulate boilerplate checklists for future reviews") — per-review, not project-wide; and the Code-Inspection-vs-Code-Review sidebar in Ch11 acknowledging that formal code inspections gather metrics. v0.9.7 honestly extends these to project-wide aggregation.

### Multi-developer concurrency (v0.9.6+) — concurrent-touch detection at M2

Multiple developers running parallel UCs can quietly converge on the same domain class, controller, or database table — and the conflict only surfaces when their PRs collide at Implementation. The kit shifts that detection left to **M2 / PDR**, when the robustness diagrams already make class references explicit.

**What's checked**, for every pair of in-flight UCs:

| Touch type | Severity | Example |
|---|---|---|
| Both write the same domain entity (add operations or attributes) | **HIGH** | UC-017 adds `Bet.place()`; UC-019 adds `Bet.cancel()` |
| Same-named boundary controller across UCs | **HIGH** | both UCs reference a class named `BetController` |
| Both write the same DB container | **HIGH** | both UCs add columns to the same database container |
| One writes, one reads the same entity | **MEDIUM** | UC-019 reads `BetLedger.balance` while UC-017 changes its semantics |
| Both reference but neither modifies | **LOW** | informational only |

**How "in-flight" is detected** (in priority order):

1. Open `feature/UC-XXX-*` branches (requires v0.9.5 git integration)
2. Unpromoted DRAFT artifacts in `use-cases/`, `robustness/`, `sequence/`
3. UCs past M2 with no Implementation PR merged

**The flow:**

```
M2 entry
  └─► Traceability — concurrent-touch detection
        │  produces change-impact/CT-<date>.md
        │  classifies HIGH / MEDIUM / LOW
        ▼
   [HIGH conflicts present?]
        │ YES                                   │ NO
        ▼                                       ▼
   Architect — propose resolutions          M2 promotion proceeds
   (extract shared service, rename
    controllers, share migration, etc.)
        │
        ▼
   Resolved or accepted in M2 PR description
   (mark accepted ones as [CT-ACCEPT-XXX])
        │
        ▼
   Re-run M2 gate
```

**Configuration** (in `iconix.config.yaml`):

```yaml
concurrent_check:
  enabled: true
  block_on_high_conflict: false   # advisory by default; set true to fail M2 PR builds
  detect_boundaries: true
  detect_db_containers: true
```

**Default is advisory.** The check produces the report and surfaces it in the M2 PR; teams enable blocking after they trust the detector. Run it on demand with `/iconix-concurrent` mid-phase.

**Why this is a kit extension over the canonical text:** Rosenberg's process assumes a small co-located team sharing one whiteboard model. For multi-developer / multi-branch environments, the canonical text doesn't address cross-UC conflict detection. v0.9.6 fills that gap, justified by Ch11 #1 (Model Update at every gate) extended to the multi-dev reality.

### Git integration (v0.9.5+) — `iconix-git` agent

The kit ships provider-agnostic branch + commit conventions plus first-class adapters for **GitHub** and **Azure DevOps**. Other providers (GitLab, Bitbucket, plain Jenkins, etc.) are supported via a generic shell-script merge-gate; see `templates/git-integration/generic/README.md`.

**Configuration** — set in `iconix.config.yaml`:

```yaml
git:
  provider: "github"           # github | azure-devops | generic
  default_branch: "main"
  branch_strategy: "trunk"     # trunk | gitflow
  work_item_prefix: "AB#"      # "AB#" for Azure Boards, "#" for GitHub Issues, "" to disable
  pr_cli: "gh"                 # gh | az | none
```

**Branch & commit convention** (provider-neutral):

```
feature/UC-017-place-bet
arch/payment-provider-abstraction
bugfix/T1-bet-controller-status-code         # Type 1 — code only
bugfix/T2-UC-017-balance-validation          # Type 2 — rejoins REQ change flow

[UC-017] M2: robustness diagram + container mapping
[BUG-T1] Fix: BetController returns 400 on negative balance
```

Full reference at `templates/git-integration/branch-conventions.md` and `commit-conventions.md`.

**What the installer drops in:**

| Provider | Files | Where |
|---|---|---|
| Always | `validate-traceability.sh` | `.ci/` |
| Always | `branch-conventions.md`, `commit-conventions.md`, `README.md` | `docs/iconix/templates/git-integration/` |
| `github` | `iconix-validate.yml`, PR templates (default + M1/M2/M3/Impl), `setup-branch-protection.sh` | `.github/workflows/`, `.github/`, `.github/PULL_REQUEST_TEMPLATE/`, `.ci/scripts/` |
| `azure-devops` | `azure-pipelines-iconix-validate.yml`, PR templates, `setup-branch-policies.sh` | repo root, `.azuredevops/pull_request_templates/`, `.ci/scripts/` |
| `generic` | (script only — user wires the script into their CI manually) | `.ci/` |

**The merge-gate** — `.ci/validate-traceability.sh` runs in CI on every PR. It fails if any changed file under `src/` or `tests/` lacks a `Traceability:` comment, or if cited UC/RB/SD/REQ/TC/ADR IDs don't match an existing artifact. Run locally before pushing with `/iconix-trace-check`.

**Enforcing the gate (branch protection)** — The CI workflow alone is advisory; it runs but cannot block merges. To make the gate enforced, run the one-time setup script installed to `.ci/scripts/`:

```bash
# GitHub (requires gh CLI, run after first CI workflow run):
bash .ci/scripts/setup-branch-protection.sh

# Azure DevOps (requires az CLI + azure-devops extension):
bash .ci/scripts/setup-branch-policies.sh \
  --org https://dev.azure.com/myorg --project MyProject --repo MyRepo
```

After running, PRs that fail the ICONIX traceability check will be blocked from merging. See `agents/iconix-git.md` `## 7. Branch protection setup` for full options.

**Opening PRs** — `/iconix-pr` detects the current phase from the diff, opens a draft PR using the matching template (M1/M2/M3/Impl), and (with `pr_cli` set) calls the right CLI (`gh` for GitHub, `az` for Azure DevOps). With `pr_cli: none` it prints the suggested URL and lets you create the PR manually.

**Reviewer-as-PR-bot** — when `/iconix-review` runs against a branch with an open PR, the Git agent posts the review report as a structured PR comment. If the recommendation is `BLOCK MERGE` or `REQUEST CHANGES`, the PR is set to draft (when supported) so it can't be merged accidentally.

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
| NFR | Non-Functional Requirement | Quality attribute or constraint: **performance** (i.e. API response time < 200ms at p99), **availability** (i.e. 99.9% uptime SLA), **security** (i.e. All PII encrypted at rest (AES-256)], **scalability** (i.e.  Handle 10,000 concurrent sessions), **compliance** (i.e. GDPR data retention ≤ 90 days), **observability** (i.e. All errors logged with correlation IDs) |
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

## AI agent patterns

The kit applies four patterns from Anthropic's agent design taxonomy:

### Orchestrator → subagents

`iconix-orchestrator` inspects current artifact state and dispatches to whichever
specialist is needed. It never produces artifacts itself — it only routes and enforces
phase gates.

```
/iconix-next → Orchestrator → [detect phase] → Product Owner | Analyst | Architect | …
```

### Prompt chaining

Each agent's output is the next agent's input. The `## Traceability` block at the end
of every artifact is the explicit handoff contract — it carries upstream IDs forward
through the full chain:

```
REQ → UC → RB → SD → CLS → TC
```

### Parallelization

Two parallel lanes are built into the pipeline:

- **M1 → M2**: Analyst (robustness diagrams) ∥ Architect (containers, ADRs)
- **M2 → M3**: Developer (sequence diagrams, code) ∥ Tester (test cases, coverage matrix)

### Evaluator / gate

Traceability acts as an evaluator at every milestone gate — it validates the traceability
chain before downstream work is allowed to proceed. If validation fails it freezes the
pipeline. The Reviewer plays a secondary evaluator role (code ↔ design drift detection).

**What the kit does not use:** tool-use loops, self-reflection cycles, or
retrieval-augmented generation — those are deferred to the optional Graphify integration,
where the Migration agent queries a pre-built knowledge graph instead of walking source
code directly.

## Philosophy

Faithful to ICONIX's minimalism: ten agents, seven commands, one pipeline.
No ceremony beyond what drives the work from use case to code.
