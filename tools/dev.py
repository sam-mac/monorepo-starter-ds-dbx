from __future__ import annotations

import subprocess
import typer

app = typer.Typer(no_args_is_help=True)

def run(cmd: list[str]) -> None:
    rc = subprocess.call(cmd)
    if rc != 0:
        raise typer.Exit(rc)

@app.command()
def fmt():
    """Format code (ruff)."""
    run(["uv", "run", "ruff", "format", "."])

@app.command()
def lint():
    """Lint code (ruff)."""
    run(["uv", "run", "ruff", "check", "."])

@app.command()
def test():
    """Run unit tests."""
    run(["uv", "run", "pytest"])

@app.command()
def check():
    """Format, lint, test."""
    fmt()
    lint()
    test()

if __name__ == "__main__":
    app()
