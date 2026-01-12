Param(
    [switch]$DryRun = $false,
    [int]$Limit = 200
)

$ProjectDir = "C:\Users\germa\OneDrive\Documentos\Programas\inventario"
Set-Location $ProjectDir

$LogDir = Join-Path $ProjectDir "logs"
if (!(Test-Path $LogDir)) { New-Item -ItemType Directory -Force -Path $LogDir | Out-Null }
$LogFile = Join-Path $LogDir "o11ce_reorder.log"

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$python = "python"
$manage = Join-Path $ProjectDir "manage.py"
$arguments = @($manage, "run_reorder_engine")
if ($DryRun) { $arguments += "--dry-run" } else { $arguments += "--apply" }
$arguments += @("--limit", "$Limit")

("$timestamp Executing: " + "$python $($arguments -join ' ')") | Out-File -Append $LogFile
try {
    $output = & $python $arguments 2>&1
    $output | Out-File -Append $LogFile
} catch {
    ("$timestamp ERROR: " + $_.Exception.Message) | Out-File -Append $LogFile
}

# Simple log retention: remove logs older than 14 days (any rotated files)
Get-ChildItem $LogDir -Filter "o11ce_reorder*.log" -ErrorAction SilentlyContinue | Where-Object {
    $_.LastWriteTime -lt (Get-Date).AddDays(-14)
} | Remove-Item -Force -ErrorAction SilentlyContinue
