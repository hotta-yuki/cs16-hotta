# Register (or re-register) the logon task that resumes the surrogate sweep.
#
#   powershell -ExecutionPolicy Bypass -File vscode\surrogate\register_resume_task.ps1
#   Unregister-ScheduledTask -TaskName SurrogateSweepResume      # to remove it
#
# Runs as the current user only while logged on (CuPy needs the user's session),
# 2 minutes after logon so Google Drive and the GPU driver are up first.
# The task removes itself once every condition in design.csv has been computed.

$TaskName = "SurrogateSweepResume"
$Script   = Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Path) "resume_sweep.ps1"
$User     = "$env:USERDOMAIN\$env:USERNAME"

$action   = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$Script`""
$trigger  = New-ScheduledTaskTrigger -AtLogOn -User $User
$trigger.Delay = "PT2M"
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
    -ExecutionTimeLimit ([TimeSpan]::Zero) -MultipleInstances IgnoreNew -StartWhenAvailable
$principal = New-ScheduledTaskPrincipal -UserId $User -LogonType Interactive -RunLevel Limited

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger `
    -Settings $settings -Principal $principal -Force | Out-Null
Get-ScheduledTask -TaskName $TaskName | Select-Object TaskName, State
