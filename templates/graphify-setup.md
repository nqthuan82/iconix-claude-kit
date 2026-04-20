# Graphify Integration Setup Guide

This guide walks you through enabling Graphify-assisted mode for the
`iconix-migration` agent. Graphify integration is **optional** — the kit
works without it, but migration is significantly faster and more accurate
when the graph is available.

## What Graphify gives the migration agent

Without Graphify, `iconix-migration` walks your code with grep/AST tools to
infer entry points, classes, and call paths. With Graphify, the same
information is already in a structured queryable graph with provenance tags
(`EXTRACTED`, `INFERRED`, `AMBIGUOUS`), so the agent reads structure
instead of inferring it.

Concretely:
- Phase 1 (code survey) drops from minutes to seconds
- Phase 3 (sequence diagram extraction) uses graph `shortest_path` queries
  instead of guessing call chains
- Every artifact carries provenance — reviewers know what was found vs
  inferred

## Prerequisites

- Python 3.10+
- Claude Code (or another supported AI assistant)
- A repository you want to retrofit ICONIX onto

## Installation (one-time, per machine)

```bash
# Recommended: pipx keeps Graphify isolated from your project envs
pipx install graphifyy
graphify install
```

Note: the PyPI package name is `graphifyy` (double-y). The CLI is `graphify`.
This matches the official upstream guidance from
https://github.com/safishamsi/graphify.

## Per-project setup

From your project root:

```bash
# 1. Build the initial graph
graphify .

# This produces:
#   graphify-out/graph.json         <- the queryable graph
#   graphify-out/GRAPH_REPORT.md    <- human-readable summary
#   graphify-out/graph.html         <- interactive viewer
```

Verify the graph looks reasonable:

```bash
# Open the interactive viewer
open graphify-out/graph.html        # macOS
xdg-open graphify-out/graph.html    # Linux
start graphify-out/graph.html       # Windows
```

## Enable in iconix.config.yaml

Edit the `knowledge_graph` section:

```yaml
knowledge_graph:
  enabled: true                          # was false
  tool: "graphify"
  graph_path: "graphify-out/graph.json"
  report_path: "graphify-out/GRAPH_REPORT.md"
  mcp_server: true
  min_confidence: 0.7
  max_age_warn_days: 7
  max_age_fail_days: 30
```

## Optional: enable the MCP server for live queries

If you set `mcp_server: true`, configure the Graphify MCP server in your
Claude Code config so the migration agent can run live graph queries
(`get_neighbors`, `shortest_path`, etc.) instead of only reading the
static `graph.json`:

```json
{
  "mcpServers": {
    "graphify": {
      "type": "stdio",
      "command": ".venv/bin/python3",
      "args": ["-m", "graphify.serve", "graphify-out/graph.json"]
    }
  }
}
```

Adjust the Python path to your environment. If you used `pipx`, find the
correct interpreter with `pipx list` and substitute.

## Keeping the graph fresh

The migration agent will warn if the graph is older than 7 days and
refuse to run if older than 30. Refresh options:

```bash
# Manual refresh (full rebuild incrementally)
graphify update .

# Continuous refresh (watch mode, useful during active migration)
graphify watch .

# Or use a git pre-commit hook (see Graphify docs)
```

## Recommended .gitignore additions

```
# Graphify outputs (regenerable, can be heavy)
graphify-out/cache/
graphify-out/graph.html

# But keep these for team consistency:
# graphify-out/graph.json
# graphify-out/GRAPH_REPORT.md
```

The Graphify project recommends committing `graph.json` and
`GRAPH_REPORT.md` so teammates share the same baseline. The cache
directory and HTML viewer are regenerable and should be ignored.

## Verifying the integration works

Run a small migration test:

```bash
# In Claude Code:
/iconix-migrate <path-to-small-module>
```

The migration agent should:
1. Open by stating "Operating in **graph-assisted mode**"
2. Report graph stats from GRAPH_REPORT.md
3. Produce artifacts with `## Provenance` footers showing
   EXTRACTED / INFERRED / AMBIGUOUS edge counts

If it reports "Operating in code-walking mode" instead, check:
- `iconix.config.yaml` has `knowledge_graph.enabled: true`
- `graphify-out/graph.json` exists at the configured path

## When NOT to enable Graphify integration

- You're starting greenfield (no legacy code to migrate)
- Your codebase changes faster than you can keep the graph fresh
- You don't have time to set up MCP server config

The kit's other 9 agents (orchestrator, product-owner, analyst, architect,
developer, tester, traceability, reviewer, docs) work identically with or
without Graphify in v0.3.0. Future versions may extend graph integration
to architect/reviewer/traceability/docs after Phase 1 is validated.

## Confidence thresholds — how to set min_confidence

- **0.9+**: Conservative. Only highly confident inferences accepted.
  Use when migration outputs feed compliance-sensitive artifacts.
- **0.7** (default): Balanced. Most useful inferences accepted with
  manageable noise.
- **0.5**: Aggressive. More inferences accepted, more `[VERIFY]` markers
  required. Use only for exploratory first-pass migrations.

Adjust based on the AMBIGUOUS / INFERRED count in your `GRAPH_REPORT.md`.
If you see many AMBIGUOUS edges, raise the threshold.

## Troubleshooting

**"Graph file not found at graphify-out/graph.json"**
Run `graphify .` from the project root.

**"Graph is 45 days old; refusing to proceed"**
Run `graphify update .` to refresh. Adjust `max_age_fail_days` in config
only if you have a strong reason — stale graphs produce wrong artifacts.

**"GRAPH_REPORT.md shows 60% INFERRED edges"**
Your codebase may use patterns Graphify cannot fully resolve via AST alone
(heavy reflection, dynamic dispatch, generated code). Consider raising
`min_confidence` to 0.8+ and accepting more `[VERIFY]` markers.

**Migration agent says "graph-assisted mode" but produces no provenance footers**
The agent is misbehaving. Check that you're on kit v0.3.0+
(`grep version iconix-init` or check CHANGELOG.md).
