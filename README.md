# Databricks-First DS Monorepo (uv + tests + bundles) — Starter

This starter is optimized for a data science team that:
- develops locally in **VS Code** (Databricks extension + Copilot) and keeps code in Git
- keeps **data and heavy processing in Databricks**
- deploys repeatably via **Databricks Asset Bundles (DAB)**
- uses **uv** for fast, reproducible Python environments

## What’s what (map of the repo)
- `projects/*` — independent DS projects (each is an installable Python package **and** a DAB bundle)
- `packages/shared_lib` — generic Python utilities (logging, config validation, small helpers)
- `packages/dbx_platform` — Databricks/Unity Catalog “glue” (naming, runtime helpers, safe defaults)
- `tools/` — onboarding scripts + scaffolding for new projects
- `.github/workflows/` — CI + deploy pipelines (uses GitHub secrets for Databricks auth)

---

## Why a shared monorepo (short + real)
- **One setup for everyone:** `uv sync` creates one predictable environment.
- **Consistent delivery to Databricks:** every project ships as a wheel and has a bundle config beside it.
- **Reuse without copy/paste:** common helpers graduate into `packages/*` when reused.
- **Lower risk:** pre-commit + CI catch issues early; main stays runnable.

---

## Quickstart (new starters / analysts / DS)

### 0) Install (once)
**Windows**
- Install “Git for Windows” (includes **Git Bash**)
- Install Python **3.12**
- Install VS Code

**macOS/Linux**
- Install git + Python **3.12**
- Install VS Code

Install uv:
- macOS/Linux:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- Windows PowerShell:
  ```powershell
  irm https://astral.sh/uv/install.ps1 | iex
  ```

### 1) Clone + bootstrap (recommended)
```bash
git clone <repo-url>
cd <repo>
./tools/scripts/bootstrap.sh
```

### 2) Daily local loop (fast)
```bash
uv run ruff format .
uv run ruff check .
uv run pytest
```

### 3) Run a project CLI locally
```bash
uv run --package customer-churn customer-churn --help
uv run --package customer-churn customer-churn prep --config conf/dev.yml
```

---

## Databricks-first development workflow (VS Code extension)
Recommended workflow per project:
1) Open the repo in VS Code
2) In the Databricks extension, choose **Local Folder** = `projects/<project>`
3) Select compute (personal compute or serverless) and start sync
4) Run:
   - Python files on cluster
   - notebooks as jobs
   - bundles (validate/deploy/run) from the extension UI

Important behavior:
- Sync is **one-way** (local → workspace); the remote copy is intended to be **transient**.

---

## “How do we keep local + Databricks consistent?”
You typically **pin the Databricks Runtime** (in bundle cluster specs) and keep project wheel deps *runtime-minimal*.
Local dev can include extra tooling via dependency groups/extras.

This repo assumes local Python is 3.12, but the project packages declare compatibility with 3.11–3.12
to reduce friction if your Databricks Runtime is on 3.11.

---

## Deploy & run (Databricks Asset Bundles)
Each project folder is a bundle root (contains `databricks.yml`).

From a project folder, e.g. `projects/customer_churn`:
```bash
databricks bundle validate -t dev
databricks bundle deploy  -t dev
databricks bundle run smoke -t dev
```

Variables are supplied via:
- `--var="key=value"` flags, or
- environment variables prefixed `BUNDLE_VAR_...` (ideal for CI).

---

## Repo ways of working (low-friction, high signal)

### Principle: keep notebooks thin
- Notebooks live in `projects/<project>/notebooks`
- Put logic in `src/` and call it from notebooks
**Value:** reproducible runs, testable logic, easier review.

### Principle: commit early, commit often
- Draft PRs are welcome
- The goal is **shared visibility**, not perfection
**Value:** reduces “lost work” and makes collaboration possible.

### Principle: separate platform glue from domain logic
- `dbx_platform` = Databricks/UC conventions
- project code = domain logic and modeling
**Value:** fewer circular dependencies and easier refactors.

---

## GitHub secrets (deployment identity) + runtime identity (run-as)
The GitHub deploy workflows assume secrets like:
- `DATABRICKS_HOST`
- `DATABRICKS_CLIENT_ID`
- `DATABRICKS_CLIENT_SECRET`

In prod, bundles are configured to **run as** a runtime service principal (least privilege on UC data).
UC grants (USE CATALOG/SCHEMA + table privileges) should be managed separately (recommended: Terraform).
See `infra/terraform/README.md`.

---

## Create a new project
```bash
uv run python tools/scaffold_project.py create my_new_project
```

---

## Commands cheat sheet
```bash
# Setup
uv sync

# Quality
uv run ruff format .
uv run ruff check .
uv run pytest

# Per-project CLI
uv run --package <dist-name> <console-script> --help

# Bundles
(cd projects/<project> && databricks bundle validate -t dev)
```
