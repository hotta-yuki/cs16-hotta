# Register (or re-register) the task that resumes the surrogate sweep after a reboot.
#
# Run from an ELEVATED PowerShell ("Run as administrator"):
#   powershell -ExecutionPolicy Bypass -File C:\Users\cs16\cs16-hotta\lab\vscode\surrogate\register_resume_task.ps1
#
#   Unregister-ScheduledTask -TaskName SurrogateSweepResume      # to remove it
#
# Mode (2026-11-07): runs whether the user is logged on or not.
#   - LogonType S4U: runs as cs16 without storing the password, in a
#     non-interactive session. Only local files are reachable (fine: the repo,
#     the conda env and the GPU are all local).
#   - Triggers: at startup and at logon, each delayed 2 minutes. After a BSOD the
#     PC reboots to the sign-in screen; the startup trigger resumes the sweep
#     without anyone logging on. resume_sweep.ps1 holds a Global mutex and also
#     checks for a running run_design.py, so the two triggers never start it twice.
#
# Before switching, this script checks that CuPy can use the GPU from an S4U
# task (session 0). If it cannot, the existing logon-only task is left as is.
# Registering S4U / startup tasks needs administrator rights.
#
# The task removes itself once every condition in design.csv has been computed.

$ErrorActionPreference = "Stop"
$TaskName = "SurrogateSweepResume"
$Here     = Split-Path -Parent $MyInvocation.MyCommand.Path
$Script   = Join-Path $Here "resume_sweep.ps1"
$Python   = "C:\Users\cs16\anaconda3\envs\venv\python.exe"
$User     = "$env:USERDOMAIN\$env:USERNAME"

$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole(
    [Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "Run this from an elevated PowerShell (Run as administrator)." -ForegroundColor Red
    exit 1
}

# ---- 1. GPU check from an S4U task -------------------------------------------
$checkPy  = Join-Path $env:TEMP "surrogate_gpu_check.py"
$checkOut = Join-Path $Here "tmp_output\gpu_check_s4u.txt"
@"
import datetime
with open(r'$checkOut', 'w') as f:
    f.write(f'{datetime.datetime.now()}\n')
    try:
        import cupy as cp
        s = float(cp.arange(10**6, dtype=cp.float64).sum())
        name = cp.cuda.runtime.getDeviceProperties(0)['name'].decode()
        f.write(f'OK sum={s} device={name}\n')
    except Exception as e:
        f.write(f'FAIL {type(e).__name__}: {e}\n')
"@ | Set-Content -Encoding ASCII $checkPy
Remove-Item $checkOut -ErrorAction SilentlyContinue

$tmpName = "SurrogateGpuCheckS4U"
Register-ScheduledTask -TaskName $tmpName -Force `
    -Action (New-ScheduledTaskAction -Execute $Python -Argument "`"$checkPy`"") `
    -Principal (New-ScheduledTaskPrincipal -UserId $User -LogonType S4U -RunLevel Limited) | Out-Null
Start-ScheduledTask -TaskName $tmpName
for ($i = 0; $i -lt 60 -and -not (Test-Path $checkOut); $i++) { Start-Sleep 2 }
Start-Sleep 3
Unregister-ScheduledTask -TaskName $tmpName -Confirm:$false
Remove-Item $checkPy -ErrorAction SilentlyContinue

$result = if (Test-Path $checkOut) { Get-Content $checkOut -Raw } else { "FAIL no output (task did not run)" }
Write-Host "GPU check from a not-logged-on (S4U) task:"
Write-Host $result
if ($result -notmatch "OK sum=") {
    Write-Host "CuPy did not work without logon. Keeping the existing logon-only task." -ForegroundColor Yellow
    exit 1
}

# ---- 2. Register the resume task ---------------------------------------------
$action    = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$Script`""
$atStartup = New-ScheduledTaskTrigger -AtStartup
$atStartup.Delay = "PT2M"
$atLogon   = New-ScheduledTaskTrigger -AtLogOn -User $User
$atLogon.Delay = "PT2M"
$settings  = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
    -ExecutionTimeLimit ([TimeSpan]::Zero) -MultipleInstances IgnoreNew -StartWhenAvailable
$principal = New-ScheduledTaskPrincipal -UserId $User -LogonType S4U -RunLevel Limited

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger @($atStartup, $atLogon) `
    -Settings $settings -Principal $principal -Force | Out-Null

$t = Get-ScheduledTask -TaskName $TaskName
Write-Host ""
Write-Host "Registered $TaskName  state=$($t.State)  logon type=$($t.Principal.LogonType)" -ForegroundColor Green
$t.Triggers | ForEach-Object { Write-Host ("  trigger: {0}  delay {1}" -f $_.CimClass.CimClassName, $_.Delay) }
