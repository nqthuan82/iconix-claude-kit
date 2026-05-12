<#
.SYNOPSIS
  Install the ICONIX Claude Code agent kit into a project.

.DESCRIPTION
  Mirrors iconix-init (bash) for Windows / PowerShell users.
  Copies agents, commands, and templates into .claude/ and seeds
  iconix.config.yaml plus the ICONIX folder structure.

.EXAMPLE
  .\iconix-init.ps1 -Prefix RGS -Language csharp
  .\iconix-init.ps1 -Global
  .\iconix-init.ps1 -Source C:\kits\iconix-kit -Force
  .\iconix-init.ps1 -Source https://github.com/your-org/iconix-claude-kit.git
#>

[CmdletBinding()]
param(
    [switch]$Global,
    [string]$Prefix = "",
    [string]$Language = "",
    [switch]$Force,
    [string]$Source = ""
)

$ErrorActionPreference = "Stop"
$DefaultSourceUrl = "https://github.com/your-org/iconix-claude-kit.git"

# Determine target
if ($Global) {
    $TargetBase = Join-Path $HOME ".claude"
    Write-Host "-> Installing globally at $TargetBase"
} else {
    $TargetBase = Join-Path (Get-Location) ".claude"
    Write-Host "-> Installing into current project at $TargetBase"
}

$AgentsDir   = Join-Path $TargetBase "agents"
$CommandsDir = Join-Path $TargetBase "commands"
New-Item -ItemType Directory -Force -Path $AgentsDir, $CommandsDir | Out-Null

# Resolve source
$WorkDir = New-Item -ItemType Directory -Path (Join-Path $env:TEMP ("iconix-" + [guid]::NewGuid()))
try {
    if ([string]::IsNullOrEmpty($Source)) { $Source = $DefaultSourceUrl }

    if (Test-Path $Source -PathType Container) {
        Write-Host "-> Copying from local path: $Source"
        Copy-Item -Path (Join-Path $Source '*') -Destination $WorkDir -Recurse -Force
    }
    elseif ($Source -match '^https?://' -or $Source.EndsWith('.git')) {
        Write-Host "-> Cloning from: $Source"
        & git clone --depth=1 $Source (Join-Path $WorkDir "kit") 2>&1 | Out-Null
        Copy-Item -Path (Join-Path $WorkDir "kit\*") -Destination $WorkDir -Recurse -Force
    }
    else {
        throw "Source must be an existing directory or a git URL. Got: $Source"
    }

    # Copy agents
    Get-ChildItem (Join-Path $WorkDir "agents") -Filter "*.md" | ForEach-Object {
        $dest = Join-Path $AgentsDir $_.Name
        if ((Test-Path $dest) -and (-not $Force)) {
            Write-Host "  skip $($_.Name) (exists, use -Force to overwrite)"
        } else {
            Copy-Item $_.FullName $dest -Force
            Write-Host "  installed agent: $($_.Name)"
        }
    }

    # Copy commands
    Get-ChildItem (Join-Path $WorkDir "commands") -Filter "*.md" | ForEach-Object {
        $dest = Join-Path $CommandsDir $_.Name
        if ((Test-Path $dest) -and (-not $Force)) {
            Write-Host "  skip command $($_.Name)"
        } else {
            Copy-Item $_.FullName $dest -Force
            Write-Host "  installed command: $($_.Name)"
        }
    }

    # Project-scope seeding
    if (-not $Global) {
        $ConfigFile = Join-Path (Get-Location) "iconix.config.yaml"
        if ((-not (Test-Path $ConfigFile)) -or $Force) {
            Copy-Item (Join-Path $WorkDir "templates\iconix.config.yaml") $ConfigFile -Force
            if ($Prefix)   { (Get-Content $ConfigFile) -replace 'prefix: "PRJ"', "prefix: `"$Prefix`"" | Set-Content $ConfigFile }
            if ($Language) { (Get-Content $ConfigFile) -replace 'language: "csharp"', "language: `"$Language`"" | Set-Content $ConfigFile }
            Write-Host "  created iconix.config.yaml"
        } else {
            Write-Host "  iconix.config.yaml already exists (use -Force to overwrite)"
        }

        $folders = @(
            "requirements","use-cases","use-case-packages","robustness","domain-model",
            "class-model","sequence","container-mapping","nfr-annotations",
            "adrs","test-cases","features","milestone-reports",
            "metrics","phase9-cycles","upgrades",
            "docs\architecture","docs\iconix","docs\iconix\templates"
        )
        foreach ($f in $folders) { New-Item -ItemType Directory -Force -Path $f | Out-Null }
        Write-Host "  created ICONIX folder structure"

        Copy-Item (Join-Path $WorkDir "templates\req-template.md")            "docs\iconix\templates\" -Force -ErrorAction SilentlyContinue
        Copy-Item (Join-Path $WorkDir "templates\adr-template.md")           "docs\iconix\templates\" -Force -ErrorAction SilentlyContinue
        Copy-Item (Join-Path $WorkDir "templates\container-mapping-template.md")            "docs\iconix\templates\" -Force -ErrorAction SilentlyContinue
        Copy-Item (Join-Path $WorkDir "templates\nfr-annotations-template.md")              "docs\iconix\templates\" -Force -ErrorAction SilentlyContinue
        Copy-Item (Join-Path $WorkDir "templates\nfr-catalog-template.md")                  "docs\iconix\templates\" -Force -ErrorAction SilentlyContinue
        Copy-Item (Join-Path $WorkDir "templates\architecture-package-map-template.md")     "docs\iconix\templates\" -Force -ErrorAction SilentlyContinue
        Copy-Item (Join-Path $WorkDir "templates\integration-surface-template.md")          "docs\iconix\templates\" -Force -ErrorAction SilentlyContinue
        Copy-Item (Join-Path $WorkDir "templates\milestone-report-template.md")             "docs\iconix\templates\" -Force -ErrorAction SilentlyContinue
        Copy-Item (Join-Path $WorkDir "templates\class-model-template.puml")                "docs\iconix\templates\" -Force -ErrorAction SilentlyContinue
        Copy-Item (Join-Path $WorkDir "templates\cdr-report-template.md")                   "docs\iconix\templates\" -Force -ErrorAction SilentlyContinue
        Copy-Item (Join-Path $WorkDir "templates\edge-case-report-template.md")             "docs\iconix\templates\" -Force -ErrorAction SilentlyContinue
        Copy-Item (Join-Path $WorkDir "templates\test-matrix-template.md")                  "docs\iconix\templates\" -Force -ErrorAction SilentlyContinue
        Copy-Item (Join-Path $WorkDir "templates\use-case-template.md")        "docs\iconix\templates\" -Force -ErrorAction SilentlyContinue
        Copy-Item (Join-Path $WorkDir "templates\use-case-diagram-template.puml") "docs\iconix\templates\" -Force -ErrorAction SilentlyContinue
        Copy-Item (Join-Path $WorkDir "templates\domain-model-initial-template.puml") "docs\iconix\templates\" -Force -ErrorAction SilentlyContinue
        Copy-Item (Join-Path $WorkDir "templates\robustness-template.puml")    "docs\iconix\templates\" -Force -ErrorAction SilentlyContinue
        Copy-Item (Join-Path $WorkDir "templates\sequence-template.puml")    "docs\iconix\templates\" -Force -ErrorAction SilentlyContinue
        Copy-Item (Join-Path $WorkDir "templates\test-case-template.md")     "docs\iconix\templates\" -Force -ErrorAction SilentlyContinue
        Copy-Item (Join-Path $WorkDir "templates\test-plan-template.md")     "docs\iconix\templates\" -Force -ErrorAction SilentlyContinue
        Copy-Item (Join-Path $WorkDir "templates\change-impact-template.md") "docs\iconix\templates\" -Force -ErrorAction SilentlyContinue
        Copy-Item (Join-Path $WorkDir "templates\graphify-setup.md")         "docs\iconix\templates\" -Force -ErrorAction SilentlyContinue
        Copy-Item (Join-Path $WorkDir "templates\intake-transcript-template.md")      "docs\iconix\templates\" -Force -ErrorAction SilentlyContinue
        Copy-Item (Join-Path $WorkDir "templates\intake-brd-template.md")             "docs\iconix\templates\" -Force -ErrorAction SilentlyContinue
        Copy-Item (Join-Path $WorkDir "templates\intake-email-template.md")           "docs\iconix\templates\" -Force -ErrorAction SilentlyContinue
        Copy-Item (Join-Path $WorkDir "templates\intake-feature-request-template.md") "docs\iconix\templates\" -Force -ErrorAction SilentlyContinue
        Copy-Item (Join-Path $WorkDir "templates\bug-report-template.md")              "docs\iconix\templates\" -Force -ErrorAction SilentlyContinue
        Copy-Item (Join-Path $WorkDir "templates\concurrent-touch-template.md")        "docs\iconix\templates\" -Force -ErrorAction SilentlyContinue
        Copy-Item (Join-Path $WorkDir "templates\phase9-cycle-template.md")            "docs\iconix\templates\" -Force -ErrorAction SilentlyContinue
        Copy-Item (Join-Path $WorkDir "templates\upgrade-report-template.md")          "docs\iconix\templates\" -Force -ErrorAction SilentlyContinue
        Copy-Item (Join-Path $WorkDir "templates\handoff-report-template.md")          "docs\iconix\templates\" -Force -ErrorAction SilentlyContinue
        Copy-Item (Join-Path $WorkDir "templates\metrics-snapshot-template.md")        "docs\iconix\templates\" -Force -ErrorAction SilentlyContinue
        Copy-Item (Join-Path $WorkDir "templates\system-architecture-template.md")       "docs\iconix\templates\" -Force -ErrorAction SilentlyContinue
        Copy-Item (Join-Path $WorkDir "templates\metrics-schema.json")                 "docs\iconix\templates\" -Force -ErrorAction SilentlyContinue
        Copy-Item (Join-Path $WorkDir "docs\iconix\metrics-glossary.md")               "docs\iconix\" -Force -ErrorAction SilentlyContinue

        # Seed canonical architecture doc if not present
        $archDoc = "docs\architecture\system-architecture.md"
        if (-not (Test-Path $archDoc)) {
            Copy-Item (Join-Path $WorkDir "templates\system-architecture-template.md") $archDoc -Force -ErrorAction SilentlyContinue
            Write-Host "  seeded docs\architecture\system-architecture.md (fill in before running the Architect agent)"
        }

        # Git integration — branch + commit conventions (always)
        New-Item -ItemType Directory -Force -Path "docs\iconix\templates\git-integration" | Out-Null
        Copy-Item (Join-Path $WorkDir "templates\git-integration\branch-conventions.md") "docs\iconix\templates\git-integration\" -Force -ErrorAction SilentlyContinue
        Copy-Item (Join-Path $WorkDir "templates\git-integration\commit-conventions.md") "docs\iconix\templates\git-integration\" -Force -ErrorAction SilentlyContinue
        Copy-Item (Join-Path $WorkDir "templates\git-integration\README.md")             "docs\iconix\templates\git-integration\" -Force -ErrorAction SilentlyContinue

        # Always seed the generic validator script
        New-Item -ItemType Directory -Force -Path ".ci" | Out-Null
        Copy-Item (Join-Path $WorkDir "templates\git-integration\generic\validate-traceability.sh") ".ci\" -Force -ErrorAction SilentlyContinue

        # Provider-specific files based on git.provider in iconix.config.yaml
        $gitProvider = "generic"
        if (Test-Path $ConfigFile) {
            $providerLine = (Get-Content $ConfigFile | Select-String -Pattern '^\s*provider:\s*"?([^"]*)"?' | Select-Object -First 1)
            if ($providerLine -and $providerLine.Matches.Count -gt 0) {
                $gitProvider = $providerLine.Matches[0].Groups[1].Value
            }
        }
        switch ($gitProvider) {
            "github" {
                New-Item -ItemType Directory -Force -Path ".github\workflows", ".github\PULL_REQUEST_TEMPLATE", ".ci\scripts" | Out-Null
                Copy-Item (Join-Path $WorkDir "templates\git-integration\github\workflows\iconix-validate.yml") ".github\workflows\" -Force -ErrorAction SilentlyContinue
                Copy-Item (Join-Path $WorkDir "templates\git-integration\github\pull_request_template.md")      ".github\" -Force -ErrorAction SilentlyContinue
                Copy-Item (Join-Path $WorkDir "templates\git-integration\github\PULL_REQUEST_TEMPLATE\m1.md")             ".github\PULL_REQUEST_TEMPLATE\" -Force -ErrorAction SilentlyContinue
                Copy-Item (Join-Path $WorkDir "templates\git-integration\github\PULL_REQUEST_TEMPLATE\m2.md")             ".github\PULL_REQUEST_TEMPLATE\" -Force -ErrorAction SilentlyContinue
                Copy-Item (Join-Path $WorkDir "templates\git-integration\github\PULL_REQUEST_TEMPLATE\m3.md")             ".github\PULL_REQUEST_TEMPLATE\" -Force -ErrorAction SilentlyContinue
                Copy-Item (Join-Path $WorkDir "templates\git-integration\github\PULL_REQUEST_TEMPLATE\implementation.md") ".github\PULL_REQUEST_TEMPLATE\" -Force -ErrorAction SilentlyContinue
                Copy-Item (Join-Path $WorkDir "templates\git-integration\github\scripts\setup-branch-protection.sh")      ".ci\scripts\" -Force -ErrorAction SilentlyContinue
                Write-Host "  installed git integration: github"
                Write-Host "  -> run 'bash .ci/scripts/setup-branch-protection.sh' once to enforce CI gates on merge"
            }
            "azure-devops" {
                New-Item -ItemType Directory -Force -Path ".azuredevops\pull_request_templates", ".ci\scripts" | Out-Null
                Copy-Item (Join-Path $WorkDir "templates\git-integration\azure-devops\azure-pipelines-iconix-validate.yml") ".\" -Force -ErrorAction SilentlyContinue
                Copy-Item (Join-Path $WorkDir "templates\git-integration\azure-devops\pull_request_templates\default.md")        ".azuredevops\pull_request_templates\" -Force -ErrorAction SilentlyContinue
                Copy-Item (Join-Path $WorkDir "templates\git-integration\azure-devops\pull_request_templates\m1.md")             ".azuredevops\pull_request_templates\" -Force -ErrorAction SilentlyContinue
                Copy-Item (Join-Path $WorkDir "templates\git-integration\azure-devops\pull_request_templates\m2.md")             ".azuredevops\pull_request_templates\" -Force -ErrorAction SilentlyContinue
                Copy-Item (Join-Path $WorkDir "templates\git-integration\azure-devops\pull_request_templates\m3.md")             ".azuredevops\pull_request_templates\" -Force -ErrorAction SilentlyContinue
                Copy-Item (Join-Path $WorkDir "templates\git-integration\azure-devops\pull_request_templates\implementation.md") ".azuredevops\pull_request_templates\" -Force -ErrorAction SilentlyContinue
                Copy-Item (Join-Path $WorkDir "templates\git-integration\azure-devops\scripts\setup-branch-policies.sh")         ".ci\scripts\" -Force -ErrorAction SilentlyContinue
                Write-Host "  installed git integration: azure-devops"
                Write-Host "  -> run 'bash .ci/scripts/setup-branch-policies.sh --help' to enforce CI gates on merge"
            }
            default {
                Copy-Item (Join-Path $WorkDir "templates\git-integration\generic\README.md") ".ci\" -Force -ErrorAction SilentlyContinue
                Write-Host "  installed git integration: generic (CI wiring left to the user)"
            }
        }
    }

    Write-Host ""
    Write-Host "[OK] ICONIX kit installed."
    Write-Host ""
    Write-Host "Next steps:"
    Write-Host "  1. Review and edit iconix.config.yaml (project prefix, stack, containers, git provider, concurrent_check, metrics)"
    Write-Host "  2. Fill in docs\architecture\system-architecture.md (seeded from template)"
    Write-Host "  3. Open Claude Code in this directory"
    Write-Host "  4. Run /agents to confirm agents are loaded"
    Write-Host "  5. Run /iconix-next to start the pipeline"
    Write-Host ""
    Write-Host "Agents installed:"
    Write-Host "  - iconix-orchestrator    (routing + phase enforcement)"
    Write-Host "  - iconix-product-owner   (requirements, use cases, glossary, initial domain model)"
    Write-Host "  - iconix-analyst         (robustness diagrams, refined domain model)"
    Write-Host "  - iconix-architect       (packages, NFRs, ADRs)"
    Write-Host "  - iconix-developer       (sequence diagrams, code, unit tests)"
    Write-Host "  - iconix-tester          (test cases, Gherkin, regression matrix)"
    Write-Host "  - iconix-traceability    (ID ledger, milestone gates, change impact)"
    Write-Host "  - iconix-reviewer        (code vs design drift detection, bug triage)"
    Write-Host "  - iconix-git             (branch/PR/commit hygiene; provider-agnostic)"
    Write-Host "  - iconix-metrics         (project metrics + audit-friendly snapshots)"
    Write-Host "  - iconix-upgrade         (kit-version migration; never modifies project artifacts)"
    Write-Host "  - iconix-docs            (user / dev / API docs generation)"
    Write-Host "  - iconix-migration       (reverse-engineer ICONIX onto legacy code)"
    Write-Host ""
    Write-Host "Commands installed:"
    Write-Host "  /iconix-next        run next pipeline step"
    Write-Host "  /iconix-status      milestone readiness report"
    Write-Host "  /iconix-impact      change impact analysis"
    Write-Host "  /iconix-review      ICONIX-style code review"
    Write-Host "  /iconix-bug         triage a bug as Type 1 (code) or Type 2 (design)"
    Write-Host "  /iconix-pr          open a phase-appropriate PR (GitHub / Azure DevOps)"
    Write-Host "  /iconix-trace-check run the traceability validator locally"
    Write-Host "  /iconix-concurrent  detect class-level conflicts between in-flight UCs (M2)"
    Write-Host "  /iconix-metrics     produce ICONIX metrics snapshot (markdown + JSON)"
    Write-Host "  /iconix-upgrade     migrate kit installation to current version"
    Write-Host "  /iconix-docs        generate user/dev/api docs"
    Write-Host "  /iconix-migrate     reverse-engineer from existing code"
    Write-Host "  /iconix-promote     promote reviewed DRAFTs to permanent IDs"
    Write-Host "  /iconix-graphify    bootstrap Graphify integration (optional, for migration)"
}
finally {
    Remove-Item $WorkDir -Recurse -Force -ErrorAction SilentlyContinue
}
