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
            "requirements","use-cases","robustness","domain-model",
            "class-model","sequence","container-mapping","nfr-annotations",
            "adrs","test-cases","features","test-matrices","milestone-reports",
            "docs\architecture","docs\iconix","docs\iconix\templates"
        )
        foreach ($f in $folders) { New-Item -ItemType Directory -Force -Path $f | Out-Null }
        Write-Host "  created ICONIX folder structure"

        Copy-Item (Join-Path $WorkDir "templates\use-case-template.md")     "docs\iconix\templates\" -Force -ErrorAction SilentlyContinue
        Copy-Item (Join-Path $WorkDir "templates\robustness-template.puml") "docs\iconix\templates\" -Force -ErrorAction SilentlyContinue
        Copy-Item (Join-Path $WorkDir "templates\graphify-setup.md")        "docs\iconix\templates\" -Force -ErrorAction SilentlyContinue
    }

    Write-Host ""
    Write-Host "[OK] ICONIX kit installed."
    Write-Host ""
    Write-Host "Next steps:"
    Write-Host "  1. Review and edit iconix.config.yaml"
    Write-Host "  2. Drop your architecture doc at docs\architecture\"
    Write-Host "  3. Open Claude Code in this directory"
    Write-Host "  4. Run /agents to confirm agents are loaded"
    Write-Host "  5. Run /iconix-next to start the pipeline"
}
finally {
    Remove-Item $WorkDir -Recurse -Force -ErrorAction SilentlyContinue
}
