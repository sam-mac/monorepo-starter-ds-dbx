\
    Set-StrictMode -Version Latest
    $ErrorActionPreference = "Stop"

    Set-Location (Split-Path -Parent $MyInvocation.MyCommand.Path)
    Set-Location ../..

    if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
      Write-Host "uv not found. Install it first:"
      Write-Host "  irm https://astral.sh/uv/install.ps1 | iex"
      exit 1
    }

    Write-Host "Syncing workspace (.venv + deps)..."
    uv sync

    Write-Host "Installing pre-commit hooks..."
    uv run pre-commit install

    Write-Host "Done. Try: uv run ruff check . ; uv run pytest"
