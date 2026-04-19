# Contributing to the ICONIX Claude Kit

Thanks for considering a contribution. This kit follows ICONIX's minimalism
philosophy: changes should make the agents more reliable or more portable,
not add ceremony.

## Ground rules

1. **One agent = one artifact owner.** Do not propose agents that blur
   responsibilities (e.g., a "full-stack" agent that does both use cases
   and code). The clean separation is the value.

2. **Agents should encode methodology, not project specifics.** If a
   proposed change mentions a specific stack (ASP.NET, Spring, Django)
   in an agent's system prompt, it belongs in `iconix.config.yaml`
   instead.

3. **Narrow is better than broad.** A sub-agent that does one check
   reliably beats one that does five things ambiguously.

4. **Anti-analysis-paralysis guardrails stay.** The `max_revisions_per_artifact`
   setting and the orchestrator's "stop after two revisions" rule are load-bearing.

## How to propose a change

1. Open an issue describing the problem (not just the solution)
2. Reference the specific ICONIX step or role affected
3. If proposing a new agent, justify why it isn't a sub-agent of an existing one
4. Submit a PR with updates to agents, commands, README, and CHANGELOG

## Agent file checklist

Every agent markdown file must have:
- YAML frontmatter with `name`, `description`, `tools`
- A `# Role` section
- A clear statement of what the agent does NOT do
- Input artifact list
- Output artifact list
- Handoff / traceability contract

## Versioning

This kit uses semantic versioning:
- **Patch** (0.0.X) — bug fixes to existing agents, documentation fixes
- **Minor** (0.X.0) — new agents, new commands, new templates
- **Major** (X.0.0) — breaking changes to the ID schema, artifact formats,
  or orchestrator routing

Tag releases as `v0.2.0`, etc. Keep a `CHANGELOG.md` with human-readable
entries.

## Testing

Before submitting:

```bash
# 1. Lint YAML frontmatter
for f in agents/*.md commands/*.md; do
  head -20 "$f" | grep -q '^---' || echo "Missing frontmatter: $f"
done

# 2. Smoke-test the installer
mkdir -p /tmp/iconix-test && cd /tmp/iconix-test
/path/to/iconix-kit/iconix-init --source /path/to/iconix-kit --prefix TEST
ls .claude/agents/ .claude/commands/ iconix.config.yaml

# 3. Run the CI validation locally (see .github/workflows/validate.yml)
```

## Code of conduct

Be direct, be specific, cite sources (including the ICONIX book when
discussing methodology points). Disagreements about methodology should
reference Rosenberg & Stephens' *Use Case Driven Object Modeling with UML*
or *Agile Development with ICONIX Process*.
