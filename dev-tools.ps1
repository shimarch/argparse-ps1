# uv-ps1-wrapper development scripts for PowerShell

function Show-Help {
    Write-Host "Available commands:" -ForegroundColor Green
    Write-Host "  Install-Package          Install package in development mode" -ForegroundColor Yellow
    Write-Host "  Install-DevDependencies  Install package with development dependencies" -ForegroundColor Yellow
    Write-Host "  Invoke-Tests             Run tests" -ForegroundColor Yellow
    Write-Host "  Invoke-TestsWithCoverage Run tests with coverage report" -ForegroundColor Yellow
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
    uv run pytest tests/ -v
}

function Invoke-TestsWithCoverage {
    Write-Host "Running tests with coverage..." -ForegroundColor Blue
    uv run pytest tests/ -v --cov=uv_ps1_wrapper --cov-report=term
}

function Invoke-Lint {
    Write-Host "Running ruff linter..." -ForegroundColor Blue
    uv run ruff check src/ tests/ examples/
}

function Invoke-Format {
    Write-Host "Running formatters..." -ForegroundColor Blue
    uv run black src/ tests/ examples/
    uv run ruff format src/ tests/ examples/
}

function Invoke-Check {
    Write-Host "Running all checks..." -ForegroundColor Blue
    uv run ruff check src/ tests/ examples/
    uv run black --check src/ tests/ examples/
    uv run ruff format --check src/ tests/ examples/
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
Export-ModuleMember -Function Show-Help, Install-Package, Install-DevDependencies, Invoke-Tests, Invoke-TestsWithCoverage, Invoke-Lint, Invoke-Format, Invoke-Check, Install-PreCommitHooks, Clear-BuildArtifacts

# Show help by default
Show-Help
