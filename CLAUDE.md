# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

**iconix-kit** is a portable Claude Code agent kit that applies the ICONIX software-development methodology (requirements → use cases → robustness → architecture → design → testing) to any software project. It ships 10 sub-agent definitions (`agents/`), 7 slash commands (`commands/`), installer scripts, and templates. There is no compiled code — agents and commands are Markdown files with YAML frontmatter consumed by Claude Code.

## Validation & Testing

There is no build step. Correctness is verified via CI:

```bash
# Run the full GitHub Actions validation locally via act, or inspect the steps manually:
cat .github/workflows/validate.yml
```

The workflow does three things:
1. **Frontmatter lint** — every `agents/*.md` must have `name` and `description`; every `commands/*.md` must have `description`
2. **Uniqueness check** — no duplicate agent `name` values
3. **Installer smoke test** — runs `iconix-init` against a scratch directory and asserts the expected files exist with the correct structure

To manually smoke-test the installer:
```bash
bash iconix-init --source . --prefix TEST --language typescript /tmp/smoke-test-project
# Verify: .claude/agents/ has ≥10 files, .claude/commands/ exists, iconix.config.yaml created
```

For Windows:
```powershell
.\iconix-init.ps1 -Source . -Prefix TEST -Language typescript -Target C:\Temp\smoke-test
```

## Architecture

### Agent Pipeline Order

Agents are not standalone — the Orchestrator enforces phase gates:

```
Product Owner → (M1 gate) → Analyst → Architect → (M2 gate) → Developer → Tester → (M3 gate)
                                                                      ↑
                                                          Traceability runs at every gate
```

`iconix-orchestrator.md` is the entry point for `/iconix-next`. It never produces artifacts itself — it routes work and enforces that upstream phases are complete before dispatching downstream agents.

### Methodology-in-Config Split

Agent system prompts encode **ICONIX rules** (e.g., the four robustness diagram connection constraints, two-column UC format, max 3 revisions per artifact). Stack-specific details (language, test framework, containers, NFR catalog) live in `iconix.config.yaml` per project. When modifying agent behavior, distinguish between changes to the ICONIX process (edit the agent `.md`) vs. changes to a project's tech context (edit `iconix.config.yaml`).

### Traceability ID Chain

Every artifact carries a `## Traceability` section. The enforced chain is:
```
REQ-XXX → UC-XXX → RB-XXX → SD-XXX → CLS-<Name> → TC-XXX
```
IDs use the format `<PREFIX>-<TYPE>-<NNN>` where PREFIX comes from `iconix.config.yaml`. IDs are **never reused** — the Traceability Agent validates this at each milestone gate and reports orphans.

### Graphify Integration (v0.3.0+)

The Migration agent has two modes controlled by `knowledge_graph.enabled` in `iconix.config.yaml`:
- **Disabled (default):** walks source code directly (7-phase workflow)
- **Enabled:** queries a pre-built Graphify knowledge graph (`graphify-out/graph.json`) for faster extraction, with provenance tracking (`EXTRACTED` / `INFERRED` / `AMBIGUOUS` edge labels)

The `/iconix-graphify` command bootstraps this integration. Other agents are not yet graph-aware (Phase 2 work planned for architect/reviewer/traceability/docs).

## Adding or Modifying Agents/Commands

Each agent file must have YAML frontmatter at the top:
```yaml
---
name: iconix-<role>
description: <one-line summary>
---
```

Each command file must have:
```yaml
---
description: <one-line summary>
---
```

Missing or malformed frontmatter will fail CI. Agent names must be globally unique across all files in `agents/`.

## Installing Into a Project

```bash
# Bash (Linux/macOS)
bash iconix-init --source /path/to/iconix-kit --prefix MYPRJ --language csharp

# PowerShell (Windows)
.\iconix-init.ps1 -Source . -Prefix MYPRJ -Language csharp

# Global install (all projects)
bash iconix-init --source . --global
```

After install: edit `.claude/iconix.config.yaml` to add containers and NFR catalog path, then open Claude Code and run `/iconix-next`.
