# ICONIX Git Integration Templates

Provider-agnostic and provider-specific templates for wiring ICONIX into a git workflow. The kit installer (`iconix-init`) reads `git.provider` from `iconix.config.yaml` and copies the matching subtree into the project.

## Layout

```
git-integration/
├── README.md                    (this file)
├── branch-conventions.md        (branch naming — works on any provider)
├── commit-conventions.md        (commit message format — works on any provider)
├── generic/
│   ├── README.md                how to wire into any CI provider
│   └── validate-traceability.sh the core merge-gate validator
├── github/
│   ├── workflows/
│   │   └── iconix-validate.yml      → .github/workflows/iconix-validate.yml
│   ├── pull_request_template.md     → .github/pull_request_template.md
│   └── PULL_REQUEST_TEMPLATE/
│       ├── m1.md                    → .github/PULL_REQUEST_TEMPLATE/m1.md
│       ├── m2.md
│       ├── m3.md
│       └── implementation.md
└── azure-devops/
    ├── azure-pipelines-iconix-validate.yml → repo root
    └── pull_request_templates/
        ├── default.md            → .azuredevops/pull_request_templates/default.md
        ├── m1.md
        ├── m2.md
        ├── m3.md
        └── implementation.md
```

## What the installer does

When `iconix.config.yaml` has `git.provider: github`:
- Copies `github/workflows/iconix-validate.yml` to `.github/workflows/`
- Copies `github/pull_request_template.md` to `.github/`
- Copies `github/PULL_REQUEST_TEMPLATE/*.md` to `.github/PULL_REQUEST_TEMPLATE/`
- Copies `generic/validate-traceability.sh` to `.ci/`

When `git.provider: azure-devops`:
- Copies `azure-devops/azure-pipelines-iconix-validate.yml` to project root
- Copies `azure-devops/pull_request_templates/*.md` to `.azuredevops/pull_request_templates/`
- Copies `generic/validate-traceability.sh` to `.ci/`

When `git.provider: generic` (or unrecognised):
- Copies `generic/validate-traceability.sh` to `.ci/`
- Copies `generic/README.md` to `.ci/`
- User wires the script into their CI manually (see `generic/README.md`)

## Adding support for another provider

The script in `generic/` is the only thing that runs the actual checks. To add (e.g.) GitLab:

1. Create `gitlab/.gitlab-ci.yml.iconix` that invokes `.ci/validate-traceability.sh`.
2. Create `gitlab/merge_request_templates/*.md` mirroring the GitHub set.
3. Add a case for `gitlab` in `iconix-init` and `iconix-init.ps1`.
4. Add a smoke-test assertion in `.github/workflows/validate.yml`.

The four steps above are kept small on purpose so the kit can grow provider coverage without inflating the core.

## Branch + commit conventions

See `branch-conventions.md` and `commit-conventions.md` — these are provider-neutral and apply regardless of which CI runs the validator.

## See also

- `agents/iconix-git.md` — the agent that drives branch creation, PR opening, and commit hygiene
- `commands/iconix-pr.md` — open a phase-appropriate PR
- `agents/iconix-traceability.md` — the methodology spec the validator enforces
