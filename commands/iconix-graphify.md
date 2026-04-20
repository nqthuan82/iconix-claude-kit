---
description: "Bootstrap Graphify integration for the migration agent. Checks install, builds the graph, enables it in iconix.config.yaml."
---

Help the user enable Graphify-assisted mode for the iconix-migration agent.

Steps:

1. Check whether Graphify is installed:
   ```
   graphify --version
   ```
   If not installed, point them to the setup guide at
   `docs/iconix/templates/graphify-setup.md` and stop. Do not install
   global packages without explicit consent.

2. Check whether `graphify-out/graph.json` already exists:
   - If yes, report when it was last modified and ask whether to refresh
     (`graphify update .`)
   - If no, ask before running `graphify .` (the initial build can take
     several minutes on a large repo)

3. After the graph is built, read `graphify-out/GRAPH_REPORT.md` and
   summarize:
   - Total nodes / edges
   - Breakdown of EXTRACTED / INFERRED / AMBIGUOUS
   - Notable findings the report calls out

4. Update `iconix.config.yaml`:
   - Set `knowledge_graph.enabled: true`
   - Verify all paths in the `knowledge_graph` section match what
     `graphify .` actually produced

5. Suggest (do not require) configuring the Graphify MCP server in
   Claude Code for live queries — point to the snippet in
   `docs/iconix/templates/graphify-setup.md`.

6. Confirm by suggesting the user run `/iconix-migrate <small-module>`
   to verify graph-assisted mode works.

Do not run `pipx install graphifyy` or any other install command without
explicit user confirmation. Do not commit anything.
