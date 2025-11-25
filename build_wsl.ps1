Param(
    [string]$Distro = "",
    [string]$OutputCopyPath = "",
    [string]$TargetPythonVersion = "3.11",
    [string]$TargetPlatform = "manylinux_2_28_aarch64"
)

# Ensure we are running from the repository root
$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

function Invoke-WslCommand($command) {
    if ([string]::IsNullOrWhiteSpace($Distro)) {
        wsl -e bash -lc "$command"
    } else {
        wsl -d $Distro -e bash -lc "$command"
    }
}

$wslRepo = (Invoke-WslCommand "wslpath -a '$RepoRoot'").Trim()

Write-Host "Installing build dependencies inside WSL (make, zip, rsync)..."
Invoke-WslCommand "sudo apt-get update && sudo apt-get install -y make zip rsync python3 python3-pip"

Write-Host "Building muxapp package via Makefile..."
Invoke-WslCommand "cd '$wslRepo' && TARGET_PYTHON_VERSION=$TargetPythonVersion TARGET_PLATFORM=$TargetPlatform make clean dist"

$distDir = Join-Path $RepoRoot "dist"
$latest = Get-ChildItem -Path $distDir -Filter *.muxapp -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $latest) {
    Write-Error "No .muxapp file was produced in $distDir"
    exit 1
}

$dest = if ([string]::IsNullOrWhiteSpace($OutputCopyPath)) { Join-Path $RepoRoot $latest.Name } else { (Resolve-Path $OutputCopyPath).Path }
Copy-Item $latest.FullName $dest -Force
Write-Host "Copied muxapp to $dest"
