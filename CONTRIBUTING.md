# Contributing

The aim is to make the “right way” the easiest way.

## Branching
- Use small branches: `name/topic`
- Prefer small PRs you can review in ~15 minutes

## Minimum standard for merging
- CI green (ruff + pytest)
- Notebook outputs are stripped (pre-commit does this)
- Config/secrets hygiene: no credentials in code or notebooks

## Notebooks
- Notebooks are allowed and valuable
- But production logic should live in `src/` so it can be tested and packaged

## Shared code rules
- Keep project-specific code in the project
- Promote to `packages/shared_lib` or `packages/dbx_platform` only after reuse
