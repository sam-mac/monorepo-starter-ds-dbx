# Team skills & conventions (human + any assistant)

This is the “human-readable contract” for how we build DS work that runs on Databricks.

## Golden path
- Notebooks are thin; real logic is in `src/`
- Projects ship as wheels; jobs run wheel entrypoints
- Config is declarative (YAML) but validated (Pydantic)
- Data lives in Unity Catalog tables (not in git)

## Where to put things
- Feature logic: `src/<project>/features/`
- Training/score orchestration: `src/<project>/pipelines/`
- Model wrappers: `src/<project>/models/`
- UC IO: `src/<project>/io/`
- Notebooks (EDA, reports): `notebooks/`

## Databricks guardrails
- No hard-coded catalog/schema; always use config / bundle variables
- No secrets in notebooks; use secret scopes or workspace identity
- Prefer writing structured outputs to Delta tables

## Testing
- Unit tests local (fast)
- Integration tests (optional) can run on Databricks against a dev schema

## AI usage guardrails
- Never accept large refactors for small requests
- Always demand tests for logic changes
