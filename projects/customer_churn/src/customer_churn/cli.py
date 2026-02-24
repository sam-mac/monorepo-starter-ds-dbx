from __future__ import annotations

import typer
from shared_lib.logging import configure_logging
from customer_churn.pipelines.prep import run as prep_run

app = typer.Typer(no_args_is_help=True)

@app.command()
def smoke():
    """Fast smoke test (safe anywhere)."""
    configure_logging()
    typer.echo("customer_churn: ok")

@app.command()
def prep(config: str = "conf/dev.yml"):
    """Create/update feature table in Unity Catalog (intended to run on Databricks)."""
    configure_logging()
    prep_run(config_path=config)

if __name__ == "__main__":
    app()
