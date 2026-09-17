# LaTeX Build Automation Script (build_report.ps1)
# Usage: .\build_report.ps1 [fileName] (without extension)

param(
    [string]$fileName = ""
)

# Set encoding to UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# Dynamically find the tex directory to avoid encoding issues with Japanese characters
# We look for a directory named 'tex' that is a subdirectory of a directory containing reports
$foundDir = Get-ChildItem -Directory -Recurse -Filter "tex" | Select-Object -First 1
if ($foundDir) {
    $texDir = $foundDir.FullName
} else {
    # Fallback if discovery fails - using wildcards to be safe
    $texDir = (Get-Item "*report*\tex" -ErrorAction SilentlyContinue).FullName
    if (-not $texDir) {
        $texDir = "tex" # Last resort
    }
}

# If no fileName provided or file not found, try to find the newest .tex file in the directory
$targetFile = Join-Path $texDir "$fileName.tex"
if ([string]::IsNullOrWhiteSpace($fileName) -or -not (Test-Path $targetFile)) {
    if (-not [string]::IsNullOrWhiteSpace($fileName) -and $fileName -ne "build_report") {
        Write-Host "Warning: $fileName.tex not found." -ForegroundColor Yellow
    }
    
    if (Test-Path $texDir) {
        $latestFile = Get-ChildItem -Path $texDir -Filter "*.tex" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
        if ($latestFile) {
            $fileName = $latestFile.BaseName
            Write-Host "Using latest file: $($latestFile.Name)" -ForegroundColor Cyan
        } else {
            Write-Host "Error: No .tex files found in $texDir." -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "Error: Directory not found." -ForegroundColor Red
        exit 1
    }
}

Write-Host "--- Starting LaTeX Build: $fileName ---" -ForegroundColor Cyan

# Move to the directory where the .tex file is located
Push-Location $texDir

# Check if ptex2pdf is available
$ptex2pdf = Get-Command ptex2pdf -ErrorAction SilentlyContinue
if (-not $ptex2pdf) {
    # Try common TeX Live installation path
    $texLivePath = "C:\texlive\2026\bin\windows\ptex2pdf.exe"
    if (Test-Path $texLivePath) {
        $ptex2pdf = $texLivePath
    } else {
        Write-Host "Error: 'ptex2pdf' command not found." -ForegroundColor Red
        Write-Host "Please ensure TeX Live is installed and added to your PATH." -ForegroundColor Yellow
        Pop-Location
        exit 1
    }
} else {
    $ptex2pdf = "ptex2pdf"
}

# Run ptex2pdf twice to resolve references (for Japanese jarticle)
& $ptex2pdf -l -ot "-kanji=utf8 -synctex=1" "$fileName.tex"
& $ptex2pdf -l -ot "-kanji=utf8 -synctex=1" "$fileName.tex"

if ($LASTEXITCODE -eq 0) {
    Write-Host "--- Build Success! ---" -ForegroundColor Green
    
    # Clean up intermediate files
    Remove-Item "$fileName.aux", "$fileName.log", "$fileName.out", "$fileName.gz" -ErrorAction SilentlyContinue
    Write-Host "Intermediate files cleaned."
} else {
    Write-Host "--- Build Failed. Check the log above. ---" -ForegroundColor Red
    exit 1
}

Pop-Location
Write-Host "Done."
