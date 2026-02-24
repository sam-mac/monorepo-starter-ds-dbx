# GitHub Copilot instructions

You are assisting in a Databricks-first DS monorepo.

- Keep notebooks thin; move logic into `src/` modules.
- Do not hard-code Unity Catalog catalog/schema names; use config objects.
- Do not print or log secrets.
- Make minimal diffs; no refactors unless requested.
- Add/adjust tests under `tests/` for logic changes.
- Prefer Spark for large-scale transforms (code runs in Databricks).
- Prefer wheel tasks for production jobs.
