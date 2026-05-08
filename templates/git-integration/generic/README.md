# Generic CI Wiring — `validate-traceability.sh`

`validate-traceability.sh` is the provider-agnostic core of the ICONIX merge-gate. The provider-specific files (`github/`, `azure-devops/`) are thin wrappers that just invoke this script.

If your CI provider isn't shipped as a first-class adapter, copy this folder into your repo and wire the script into your pipeline manually. The script:

- Compares `${ICONIX_BASE_REF}` against `${ICONIX_HEAD_REF}` (defaults: `origin/main` and `HEAD`)
- Fails if any changed file under `src/` or `tests/` lacks a `Traceability:` comment
- Fails if any cited UC/RB/SD/REQ/TC/ADR ID points to an artifact that doesn't exist
- Exits 0 on pass, 1 on violations, 2 on setup error

## Drop-in for any CI

```bash
# Make the script executable and stage it
chmod +x .ci/validate-traceability.sh

# In your pipeline (Jenkinsfile, .circleci/config.yml, etc.):
git fetch --no-tags --prune --depth=50 origin main
.ci/validate-traceability.sh origin/main HEAD
```

The script needs:
- `bash` 4+
- `git` 2.20+
- POSIX `grep`, `find`, `sed`, `head`, `cut`, `sort`

No other dependencies. It's self-contained on purpose so it runs identically in CI containers and on developer laptops.

## Running locally before pushing

```bash
.ci/validate-traceability.sh origin/main
```

Or use the `/iconix-trace-check` slash command, which calls this script with the right base ref for the current branch.

## Tuning

- **ID prefix:** auto-resolved from `iconix.config.yaml` (`project.prefix`). Override by exporting `ICONIX_PREFIX` if needed.
- **Skip on docs-only PRs:** add a guard in the wrapping pipeline; the script itself does not differentiate.
- **Custom artifact folders:** the script's folder mapping is hard-coded to the kit defaults (`requirements/`, `use-cases/`, etc.). Edit the `case "$type" in ...` block if your project uses a non-standard layout.
