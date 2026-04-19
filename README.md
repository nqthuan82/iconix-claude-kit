# ICONIX Claude Code Kit

A reusable set of Claude Code sub-agents and commands that apply the ICONIX
software-development process (Rosenberg & Stephens) to any project.

## What's inside

```
iconix-kit/
├── iconix-init              # installer CLI (bash)
├── iconix-init.ps1          # installer CLI (PowerShell)
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
│   └── iconix-migration.md    # retrofit ICONIX onto legacy code
├── commands/                # Claude Code slash commands
│   ├── iconix-next.md
│   ├── iconix-status.md
│   ├── iconix-impact.md
│   ├── iconix-review.md
│   ├── iconix-docs.md
│   └── iconix-migrate.md
└── templates/               # per-project templates
    ├── iconix.config.yaml
    ├── use-case-template.md
    └── robustness-template.puml
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

## Philosophy

Faithful to ICONIX's minimalism: six primary agents, three commands,
one pipeline. No ceremony beyond what drives the work from use case to code.
