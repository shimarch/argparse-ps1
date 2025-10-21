# uv-ps1-wrapper development scripts for PowerShell

function Show-Help {
    Write-Host "Available commands:" -ForegroundColor Green
    Write-Host "  Install-Package          Install package in development mode" -ForegroundColor Yellow
    Write-Host "  Install-DevDependencies  Install package with development dependencies" -ForegroundColor Yellow
    Write-Host "  Invoke-Tests             Run tests" -ForegroundColor Yellow
    Write-Host "  Invoke-Lint              Run ruff linter" -ForegroundColor Yellow
    Write-Host "  Invoke-Format            Run black formatter and ruff formatter" -ForegroundColor Yellow
    Write-Host "  Invoke-Check             Run all checks (lint + format check)" -ForegroundColor Yellow
    Write-Host "  Install-PreCommitHooks   Install pre-commit hooks" -ForegroundColor Yellow
    Write-Host "  Clear-BuildArtifacts     Clean build artifacts" -ForegroundColor Yellow
}

function Install-Package {
    Write-Host "Installing package in development mode..." -ForegroundColor Blue
    uv pip install -e .
}

function Install-DevDependencies {
    Write-Host "Installing package with development dependencies..." -ForegroundColor Blue
    uv pip install -e ".[dev]"
}

function Invoke-Tests {
    Write-Host "Running tests..." -ForegroundColor Blue
    python -m pytest tests/ -v
}

function Invoke-Lint {
    Write-Host "Running ruff linter..." -ForegroundColor Blue
    python -m ruff check src/ tests/ examples/
}

function Invoke-Format {
    Write-Host "Running formatters..." -ForegroundColor Blue
    python -m black src/ tests/ examples/
    python -m ruff format src/ tests/ examples/
}

function Invoke-Check {
    Write-Host "Running all checks..." -ForegroundColor Blue
    python -m ruff check src/ tests/ examples/
    python -m black --check src/ tests/ examples/
    python -m ruff format --check src/ tests/ examples/
}

function Install-PreCommitHooks {
    Write-Host "Installing pre-commit hooks..." -ForegroundColor Blue
    uv run pre-commit install
}

function Clear-BuildArtifacts {
    Write-Host "Cleaning build artifacts..." -ForegroundColor Blue
    if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
    if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
    Get-ChildItem -Recurse -Name "*.egg-info" | Remove-Item -Recurse -Force
    Get-ChildItem -Recurse -Name "__pycache__" | Remove-Item -Recurse -Force
    Get-ChildItem -Recurse -Name "*.pyc" | Remove-Item -Force
}

# Export functions
Export-ModuleMember -Function Show-Help, Install-Package, Install-DevDependencies, Invoke-Tests, Invoke-Lint, Invoke-Format, Invoke-Check, Install-PreCommitHooks, Clear-BuildArtifacts

# Show help by default
Show-Help
