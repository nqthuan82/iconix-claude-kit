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
Product Owner → (M1 gate) → Analyst → Architect → (M2 gate) → Developer → Tester → (M3 gate) → Implementation
                                                                      ↑
                                                          Traceability runs at every gate
```

Implementation is phase 9 in `iconix-orchestrator.md` — Developer + Tester iterate after M3 to build to the approved design and fix drift surfaced by the Reviewer.

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

## ICONIX Theory References

When reviewing ICONIX artifacts (use cases, robustness diagrams, sequence diagrams, domain models, test cases) or auditing the kit itself for methodology compliance, treat these as the authoritative sources:

- **`docs/iconix/iconix-process-reference.md`** (committed) — coverage matrix mapping every Top 10 list and key rule from Rosenberg & Stephens to the agent/template/command that enforces it, with a ✅/⚠️/❌ status per rule. **Look here first** to find which agent owns a given ICONIX rule and whether it's currently enforced. Use it to detect mismatches between an artifact and the rule it's supposed to satisfy.
- **`Use Case Driven Object Modeling with UML.pdf`** — Doug Rosenberg & Matt Stephens (Apress, 2007), the canonical ICONIX text. **Gitignored** (copyrighted), so only available on machines where the user has placed it locally. When present, use it as the source of truth for resolving ambiguities the matrix doesn't settle (e.g., subtle robustness-diagram connection rules, exact GRASP application). The file is large — always read with the `pages` parameter for a specific chapter range, never the whole file. If the PDF is not present locally, fall back to the reference matrix and say so explicitly.

When flagging a possible methodology violation (e.g., a robustness diagram with boundary→entity links, a UC missing alternate courses, a sequence diagram with controllers calling boundaries directly), cite the specific rule from the matrix — and quote the relevant passage from the book when available — rather than asserting it from memory.

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

## Auditing kit changes against ICONIX Theory

Whenever a change in this conversation touches the kit's **methodology surface** — anything that encodes an ICONIX rule, gate, or process step — audit it against the references in `## ICONIX Theory References` (above) before treating the change as complete. This is what keeps the kit faithful to the source methodology over time and prevents drift from accumulating one well-intentioned edit at a time.

Treat the following as methodology-surface changes:
- Agent system prompts (`agents/*.md`) — rules listed under headings like `# ICONIX rules`, `# Domain model rules`, milestone checklists, phase order, artifact responsibilities
- Templates (`templates/*`) — section structure, mandatory fields, traceability blocks
- Milestone gate criteria (M1 / M2 / M3) wherever defined
- Pipeline order in `iconix-orchestrator.md` and `iconix-state-machine.puml`
- The process reference matrix itself (`docs/iconix/iconix-process-reference.md`)
- Commands that introduce methodology semantics (e.g., `/iconix-impact`, `/iconix-bug`)

Tooling-only changes (installer scripts, CI workflow, version bumps, typo fixes, methodology-neutral bug fixes, formatting) do **not** require a theory audit.

For each methodology-surface change, before treating it complete:

1. **Cite the matrix row.** Find the rule in `docs/iconix/iconix-process-reference.md` that the change implements, modifies, or contradicts. Quote the chapter and rule number in the response (e.g., "Ch2 #3 — Draw the domain model before writing use cases").
2. **Verify against the book** when the matrix does not fully resolve the question. Read `Use Case Driven Object Modeling with UML.pdf` with the `pages` parameter for the relevant chapter range — never the whole file. Quote the relevant passage. If the PDF is not present locally, say so explicitly and proceed using the matrix alone.
3. **Update the matrix in the same change** if the kit's coverage status for any rule has shifted (✅ ⚠️ ❌ 🚫). Bump the "Last reviewed" version line. Re-check the chapter's ✅/⚠️/❌/🚫 counts in the Summary Coverage Matrix.
4. **Surface contradictions.** If the proposed change conflicts with the book or matrix, do not silently introduce it. Flag the conflict and let the user decide whether to revise the change or revise the matrix row (with a justification).

In the response, mention which rules were audited, what was cited, and whether the matrix was updated. If a change initially appeared methodology-relevant but turned out not to be, say so explicitly so the user knows the audit was considered and consciously skipped.

Same applicability as the sync rule below: this fires while Claude is actively making or reviewing changes in Claude Code; it does not fire for edits made outside Claude Code.

## Keeping README and state machine in sync

Whenever a change in this conversation touches the kit's user-facing surface — files under `agents/`, `commands/`, `templates/`, the installers (`iconix-init`, `iconix-init.ps1`), `templates/iconix.config.yaml`, the directory layout, or the agent pipeline / milestone gates — review both of these before treating the change as complete:

1. **`README.md`** — confirm it still accurately states the agent count, the command list, installer flags, the directory layout it advertises, and any examples that reference renamed or removed items.
2. **`iconix-state-machine.puml`** (root) — confirm states, transitions, M1/M2/M3 gates, and agent labels still match the pipeline. If a new agent, gate, or transition was introduced or one was renamed/removed, update the diagram in the same change.

If a mismatch is found, fix it in the same change rather than deferring. Mention in the response which files were updated and why.

This is a CLAUDE.md instruction, so it applies while Claude is actively making or reviewing changes; it does not fire for edits made outside Claude Code. For harness-enforced automation on every file save, a PostToolUse hook in `.claude/settings.json` would be needed.

## Commit workflow

Before committing any changes to this repo:
1. Update `CHANGELOG.md` with a new version entry describing what changed and why.
2. Show the user the planned commit message and wait for explicit acceptance.
3. Only then run `git commit`.

Never commit without completing both steps first.
