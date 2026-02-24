from __future__ import annotations

import re
from pathlib import Path
import textwrap
import typer

app = typer.Typer(no_args_is_help=True)

def slugify(name: str) -> str:
    name = name.strip().lower().replace("-", "_").replace(" ", "_")
    name = re.sub(r"[^a-z0-9_]", "", name)
    name = re.sub(r"_+", "_", name).strip("_")
    if not name:
        raise typer.BadParameter("Project name produced an empty slug.")
    if name[0].isdigit():
        name = f"p_{name}"
    return name

@app.command()
def create(name: str):
    """Create a new Databricks-first project under projects/<name>."""
    repo_root = Path(__file__).resolve().parents[1]
    projects_dir = repo_root / "projects"
    projects_dir.mkdir(exist_ok=True)

    pkg = slugify(name)
    dist = pkg.replace("_", "-")
    proj_dir = projects_dir / pkg
    if proj_dir.exists():
        raise typer.BadParameter(f"{proj_dir} already exists")

    # Structure
    (proj_dir / "src" / pkg).mkdir(parents=True)
    (proj_dir / "tests" / "unit").mkdir(parents=True)
    (proj_dir / "tests" / "integration").mkdir(parents=True)
    (proj_dir / "notebooks").mkdir()
    (proj_dir / "conf").mkdir()
    (proj_dir / "resources").mkdir()

    # README
    (proj_dir / "README.md").write_text(textwrap.dedent(f"""\
        # {pkg}

        Databricks-first DS project.

        ## Local
        ```bash
        uv sync
        uv run --package {dist} {dist} --help
        ```

        ## Databricks bundle
        ```bash
        databricks bundle validate -t dev
        databricks bundle deploy -t dev
        databricks bundle run smoke -t dev
        ```
        """), encoding="utf-8")

    # Minimal package
    (proj_dir / "src" / pkg / "__init__.py").write_text("__all__ = []\n", encoding="utf-8")

    (proj_dir / "src" / pkg / "cli.py").write_text(textwrap.dedent(f"""\
        from __future__ import annotations

        import typer
        from {pkg}.pipelines import prep as prep_mod

        app = typer.Typer(no_args_is_help=True)

        @app.command()
        def smoke():
            """Fast smoke test."""
            typer.echo("{pkg}: ok")

        @app.command()
        def prep(config: str = "conf/dev.yml"):
            """Prep/features step (runs on Databricks in practice)."""
            prep_mod.run(config_path=config)

        if __name__ == "__main__":
            app()
        """), encoding="utf-8")

    # Config + pydantic validation
    (proj_dir / "src" / pkg / "config.py").write_text(textwrap.dedent(f"""\
        from __future__ import annotations

        from pathlib import Path
        import yaml
        from pydantic import BaseModel, Field

        class ProjectConfig(BaseModel):
            env: str = "dev"
            catalog: str = Field(..., description="Unity Catalog catalog")
            schema: str = Field(..., description="Unity Catalog schema")
            features_table: str = "features_{pkg}"

        def load_config(path: str | Path) -> ProjectConfig:
            data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {{}}
            return ProjectConfig.model_validate(data)
        """), encoding="utf-8")

    (proj_dir / "src" / pkg / "pipelines").mkdir()
    (proj_dir / "src" / pkg / "pipelines" / "__init__.py").write_text("__all__ = []\n", encoding="utf-8")
    (proj_dir / "src" / pkg / "pipelines" / "prep.py").write_text(textwrap.dedent(f"""\
        from __future__ import annotations

        from {pkg}.config import load_config
        from dbx_platform.runtime import get_spark

        def run(config_path: str = "conf/dev.yml") -> None:
            cfg = load_config(config_path)
            spark = get_spark()
            # Example placeholder: replace with real UC inputs.
            df = spark.range(0, 10).withColumnRenamed("id", "x")
            out = df.withColumn("x2", df.x * df.x)

            target = f"{{cfg.catalog}}.{{cfg.schema}}.{{cfg.features_table}}"
            (out.write
                .mode("overwrite")
                .format("delta")
                .saveAsTable(target))
            print(f"Wrote {{target}}")
        """), encoding="utf-8")

    # Tests
    (proj_dir / "tests" / "unit" / "test_import.py").write_text(textwrap.dedent(f"""\
        def test_import():
            import {pkg}  # noqa: F401
        """), encoding="utf-8")

    # conf
    (proj_dir / "conf" / "dev.yml").write_text(textwrap.dedent(f"""\
        env: dev
        catalog: main_dev
        schema: {pkg}_dev
        features_table: features_{pkg}
        """), encoding="utf-8")

    # project pyproject
    (proj_dir / "pyproject.toml").write_text(textwrap.dedent(f"""\
        [project]
        name = "{dist}"
        version = "0.1.0"
        # Keep compatible with common Databricks runtimes (often 3.11) while developing locally on 3.12
        requires-python = ">=3.11,<3.13"
        dependencies = [
          "typer>=0.12",
          "pyyaml>=6.0",
          "pydantic>=2.7",
          "dbx-platform",
          "shared-lib",
        ]

        [project.scripts]
        {dist} = "{pkg}.cli:app"

        [build-system]
        requires = ["hatchling"]
        build-backend = "hatchling.build"

        [tool.hatch.build.targets.wheel]
        packages = ["src/{pkg}"]
        """), encoding="utf-8")

    # DAB bundle config
    (proj_dir / "databricks.yml").write_text(textwrap.dedent(f"""\
        bundle:
          name: {pkg}

        include:
          - resources/*.yml

        variables:
          catalog:
            description: "Unity Catalog catalog for this environment"
          schema:
            description: "Unity Catalog schema for this environment"
          runtime_sp:
            description: "Service principal to run prod workloads as (application ID or name)"

        targets:
          dev:
            default: true
            mode: development
            workspace:
              host: ${{workspace.host}}
              root_path: /Workspace/Users/${{workspace.current_user.userName}}/.bundle/${{bundle.name}}/${{bundle.target}}
              file_path: /Workspace/Users/${{workspace.current_user.userName}}/.vscode/${{bundle.name}}/${{bundle.target}}
            run_as:
              user_name: ${{workspace.current_user.userName}}
            variables:
              catalog: main_dev
              schema: {pkg}_${{workspace.current_user.short_name}}

          prod:
            mode: production
            workspace:
              host: ${{workspace.host}}
              root_path: /Workspace/Shared/.bundle/${{bundle.name}}/${{bundle.target}}
              file_path: /Workspace/Shared/.bundle/${{bundle.name}}/${{bundle.target}}
            run_as:
              service_principal_name: ${{var.runtime_sp}}
            variables:
              catalog: main_prod
              schema: {pkg}
        """), encoding="utf-8")

    # resources: jobs + pipelines (optional) + permissions
    (proj_dir / "resources" / "jobs.yml").write_text(textwrap.dedent(f"""\
        resources:
          jobs:
            smoke:
              name: {pkg}_smoke
              tasks:
                - task_key: smoke
                  new_cluster:
                    spark_version: "13.3.x-scala2.12"
                    node_type_id: "i3.xlarge"
                    num_workers: 1
                  python_wheel_task:
                    package_name: {pkg}
                    entry_point: {dist}
                    parameters: ["smoke"]

            pipeline_job:
              name: {pkg}_pipeline
              tasks:
                - task_key: prep
                  depends_on: []
                  new_cluster:
                    spark_version: "13.3.x-scala2.12"
                    node_type_id: "i3.xlarge"
                    num_workers: 2
                  python_wheel_task:
                    package_name: {pkg}
                    entry_point: {dist}
                    parameters: ["prep", "--config", "conf/dev.yml"]
        """), encoding="utf-8")

    (proj_dir / "resources" / "pipelines.yml").write_text(textwrap.dedent(f"""\
        # Optional: Lakeflow Spark Declarative Pipeline.
        # Use this for ingestion / incremental feature tables; keep training as a Job.
        resources:
          pipelines:
            {pkg}_features:
              name: {pkg}_features
              development: true
              continuous: false
              channel: CURRENT
              edition: CORE
              clusters:
                - label: default
                  num_workers: 1
              catalog: ${{var.catalog}}
              target: ${{var.schema}}
              libraries:
                - notebook:
                    path: ./notebooks/20_lakeflow_features.py
        """), encoding="utf-8")

    (proj_dir / "resources" / "permissions.yml").write_text(textwrap.dedent("""            # Apply broad permissions at the top-level `permissions` if you want consistent behavior.
        # This file is a placeholder for org-specific group names.
        permissions:
          - level: CAN_VIEW
            group_name: ds_all
          - level: CAN_RUN
            group_name: ds_team
          - level: CAN_MANAGE
            group_name: ds_platform_admins
        """), encoding="utf-8")

    # Notebook stubs (Databricks source format)
    (proj_dir / "notebooks" / "00_eda.py").write_text(textwrap.dedent(f"""\
        # Databricks notebook source
        # MAGIC %md
        # MAGIC # {pkg} — EDA (thin notebook)
        # MAGIC This notebook should stay thin: call `src/{pkg}` functions.
        """), encoding="utf-8")

    (proj_dir / "notebooks" / "20_lakeflow_features.py").write_text(textwrap.dedent(f"""\
        # Databricks notebook source
        # MAGIC %md
        # MAGIC # Lakeflow features pipeline (optional)
        # MAGIC Replace the demo code with real UC inputs/outputs.
        """), encoding="utf-8")

    # databricks.env template (not committed as databricks.env)
    (proj_dir / "databricks.env.example").write_text(textwrap.dedent("""\
        # Copy to databricks.env (this file is gitignored) if you want local bundle vars
        # Example:
        # BUNDLE_VAR_runtime_sp=00000000-0000-0000-0000-000000000000
        """), encoding="utf-8")

    typer.echo(f"Created {proj_dir}")

if __name__ == "__main__":
    app()
