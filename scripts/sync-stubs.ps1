#!/usr/bin/env pwsh
# Sync stub reference files from canonical source (ceh-python-backend) to host plugins.
# Always one-way: source is truth.

$repoRoot = $PSScriptRoot | Split-Path -Parent
$source   = Join-Path $repoRoot "ceh-python-backend\skills\python-backend\references"

$stubs = @(
    @{ file = "database.md";     dest = "ceh-architecture-design\skills\python-backend\references" },
    @{ file = "observability.md"; dest = "ceh-release-ops\skills\python-backend\references" },
    @{ file = "security.md";     dest = "ceh-release-ops\skills\python-backend\references" }
)

$changed = 0
$errors  = 0

foreach ($stub in $stubs) {
    $src  = Join-Path $source $stub.file
    $destDir = Join-Path $repoRoot $stub.dest
    $dst  = Join-Path $destDir $stub.file

    if (-not (Test-Path $src)) {
        Write-Error "Source missing: $src"
        $errors++
        continue
    }

    $null = New-Item -ItemType Directory -Force $destDir

    $srcHash = (Get-FileHash $src  -Algorithm MD5).Hash
    $dstHash = if (Test-Path $dst) { (Get-FileHash $dst -Algorithm MD5).Hash } else { "" }

    if ($srcHash -ne $dstHash) {
        Copy-Item -Path $src -Destination $dst -Force
        Write-Host "synced  $($stub.dest)\$($stub.file)"
        $changed++
    } else {
        Write-Host "ok      $($stub.dest)\$($stub.file)"
    }
}

Write-Host ""
if ($errors -gt 0) {
    Write-Error "$errors error(s). $changed file(s) updated."
    exit 1
}
Write-Host "$changed file(s) updated, $(($stubs.Count - $changed)) already in sync."
