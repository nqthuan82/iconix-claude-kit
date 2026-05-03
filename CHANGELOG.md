# Changelog

All notable changes to the ICONIX Claude Kit.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.4.1] — 2026-05-03

### Fixed
- **Migration idempotency guard**: `iconix-migration` now runs a `# Pre-run idempotency
  check` before any Phase 1 work in both modes, preventing silent overwrites on repeated
  `/iconix-migrate` runs:
  - Detects artifacts already promoted to permanent IDs (via `ids.registry.md`) and skips them
  - Detects DRAFT files modified by humans since the last run and skips them by default
  - Outputs a pre-run summary before proceeding so the user knows exactly what will be (re)generated
  - Aborts cleanly if everything is already promoted or human-edited
  - Two new rules added to `# What you never do` to reinforce the constraints

## [0.4.0] — 2026-05-03

### Added
- **Change mode for artifact-producing agents**: Product Owner, Analyst, and Tester
  each have a new `# Change mode` section. When given a `change-impact/CI-<date>.md`
  report, each agent self-scopes to the blast radius only:
  - Product Owner: updates only the affected UCs and re-runs M1 checklist scoped to those UCs
  - Analyst: updates only the affected RBs in place; updates domain model only if new entities appear
  - Tester: revises only the affected TCs and `test-matrix.md` rows; re-runs coverage gates scoped to changed UCs
- **REQ change flow in Orchestrator**: new `# REQ change flow` section drives the full
  scoped pipeline automatically via `/iconix-next` when a REQ change is detected —
  Traceability → Product Owner → M1 → Analyst → M2 → Developer+Tester (parallel) → M3

### Changed
- Orchestrator passes the CI report path in its dispatch plan so downstream agents
  can self-scope without manual instruction
- README: documented the REQ change flow, plan mode behaviour per agent,
  migration→pipeline handoff, and added a Notation & abbreviations glossary

## [0.3.0] — 2026-04-19

### Added
- **Graphify integration (Phase 1, migration agent only)**: `iconix-migration`
  now runs in graph-assisted mode when `iconix.config.yaml` enables Graphify.
  In graph-assisted mode:
  - Phase 1 (code survey) uses graph queries instead of code walking
  - Phases 2-3 (class model, sequence diagrams) seed from graph nodes/edges
  - Every artifact carries a `## Provenance` footer showing
    EXTRACTED / INFERRED / AMBIGUOUS edge counts
  - Stale graphs (>30 days) block migration; >7 days warns
- `knowledge_graph:` section in `iconix.config.yaml` template
  (disabled by default; portability preserved)
- `/iconix-graphify` slash command — bootstraps Graphify in a project
- `templates/graphify-setup.md` — full setup guide with confidence tuning,
  MCP server config, troubleshooting

### Changed
- `iconix-migration` agent now declares "operating mode" at start of every
  run (graph-assisted | code-walking)
- Orchestrator routing recognizes graph-assisted vs code-walking flow
- Installer copies Graphify setup guide into project templates

### Notes
- Other 9 agents (orchestrator, product-owner, analyst, architect,
  developer, tester, traceability, reviewer, docs) are **unchanged** in this
  release. Phase 2 will extend graph integration to architect/reviewer/
  traceability/docs once Phase 1 is validated in real use.
- This is an additive change. Existing projects on v0.2.0 continue to work
  identically without enabling `knowledge_graph`.

## [0.2.0] — 2026-04-19

### Added
- `iconix-reviewer` agent — detects drift between code and design artifacts
  (sequence diagram, class model, NFRs); produces review reports with
  BLOCK / CHANGES / APPROVE recommendations
- `iconix-docs` agent — generates user guides, developer onboarding, API
  reference, release notes, and SRE runbooks from ICONIX artifacts
- `iconix-migration` agent — reverse-engineers draft ICONIX artifacts from
  existing legacy codebases in a 7-phase workflow
- `/iconix-review`, `/iconix-docs`, `/iconix-migrate` slash commands
- PowerShell installer (`iconix-init.ps1`) for Windows users
- GitHub Actions validation workflow
- `CONTRIBUTING.md`, `LICENSE` (MIT), `CHANGELOG.md`

### Changed
- Orchestrator routing heuristics extended to cover review, docs, and
  migration flows
- Installer success message now lists all 10 agents and 6 commands

## [0.1.0] — 2026-04-19

### Added
- Initial kit with 7 agents: orchestrator, product-owner, analyst, architect,
  developer, tester, traceability
- 3 slash commands: `/iconix-next`, `/iconix-status`, `/iconix-impact`
- Bash installer (`iconix-init`) with project-scope and user-scope modes
- `iconix.config.yaml` template with prefix, stack, containers, NFRs
- Use case and robustness diagram templates
- README with install recipe and portability matrix
