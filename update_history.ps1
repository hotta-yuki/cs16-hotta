# LLM History Update Script (update_history.ps1)
# Ref: https://qiita.com/rxg03350/items/9bd822a2be5549b17878

$pythonPath = "C:\Users\cs16\anaconda3\python.exe"
$scriptPath = "scripts\render_llm_history.py"

if (-not (Test-Path $pythonPath)) {
    Write-Host "Error: Python not found at $pythonPath" -ForegroundColor Red
    exit 1
}

Write-Host "--- Updating LLM Conversation History ---" -ForegroundColor Cyan

& $pythonPath $scriptPath

if ($LASTEXITCODE -eq 0) {
    Write-Host "--- Update Success! ---" -ForegroundColor Green
} else {
    Write-Host "--- Update Failed. ---" -ForegroundColor Red
}

Write-Host "Done."
