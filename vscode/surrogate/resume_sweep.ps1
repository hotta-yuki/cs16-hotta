# Resume the surrogate design sweep (run_design.py) after a reboot.
#
# Registered as a logon task by register_resume_task.ps1. run_design.py skips
# conditions whose CSV already exists, so running this again after a crash
# continues from where it stopped and loses at most the condition in progress.
#
# - Does nothing if run_design.py is already running (no double start on the GPU)
# - When nothing is left to compute, unregisters its own logon task, so a later
#   change to design.csv does not start a 20+ hour sweep by surprise.
#
# Comments are ASCII on purpose: Windows PowerShell 5.1 reads BOM-less files as ANSI.

$ErrorActionPreference = "Stop"
$TaskName = "SurrogateSweepResume"
$Here     = Split-Path -Parent $MyInvocation.MyCommand.Path
$Python   = "C:\Users\cs16\anaconda3\envs\venv\python.exe"
$LogDir   = Join-Path $Here "tmp_output"
$Log      = Join-Path $LogDir ("run_log_resume_{0}.txt" -f (Get-Date -Format "yyyyMMdd"))

# Phases to finish before the normal phase order. 2026-11-05: the user asked to
# get the remaining 120 train points (learning curve 100 / 180) ahead of the
# specimen and test phases. 2026-11-24: phase 4 is done, back to plain order.
$PriorityPhases = @()

# Design sets to compute (run_design.py --set). @() means run_design.py's default
# order (smooth isorms specimen train test). 2026-11-24: the default sets are all
# done and the sweep in progress is test_spec, which is not in the default order;
# without this the dry run finds nothing left and the task removes itself.
$Sets = @("test_spec")
$SetArgs = if ($Sets.Count) { @("--set") + $Sets } else { @() }
$SetArg  = $SetArgs -join " "

# The task has both a startup and a logon trigger, and they can fire within
# seconds of each other in different sessions. A Global mutex makes the second
# one exit even before the first has launched python. Held until this script ends.
$mutex = New-Object System.Threading.Mutex($false, "Global\SurrogateSweepResume")
if (-not $mutex.WaitOne(0)) {
    exit 0
}

$running = Get-CimInstance Win32_Process -Filter "name='python.exe'" |
    Where-Object { $_.CommandLine -match "run_design\.py" -and $_.CommandLine -notmatch "--dry-run" }
if ($running) {
    exit 0
}

Set-Location $Here
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

# Anything left? The dry run prints "RUN ->" for each condition still to compute.
$todo = & $Python -u run_design.py --dry-run @SetArgs 2>&1 | Select-String -SimpleMatch "RUN ->"
if (-not $todo) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
    exit 0
}

# cmd redirection keeps the log in the same encoding as the earlier logs
# (PowerShell 5.1 ">>" would write UTF-16).
$stamp = Get-Date -Format "yyyy-MM-dd HH:mm"
cmd.exe /c "echo === auto resume $stamp ($($todo.Count) left, priority phases: $($PriorityPhases -join ',')) ===>> `"$Log`""
foreach ($ph in $PriorityPhases) {
    cmd.exe /c "`"$Python`" -u run_design.py --phase $ph >> `"$Log`" 2>&1"
}
cmd.exe /c "`"$Python`" -u run_design.py $SetArg >> `"$Log`" 2>&1"

$left = & $Python -u run_design.py --dry-run @SetArgs 2>&1 | Select-String -SimpleMatch "RUN ->"
if (-not $left) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
}
