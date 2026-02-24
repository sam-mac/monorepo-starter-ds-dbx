# customer_churn

Databricks-first DS project example.

## Local quickstart
```bash
uv sync
uv run --package customer-churn customer-churn --help
uv run --package customer-churn customer-churn smoke
```

## Databricks bundle quickstart
From this folder:
```bash
databricks bundle validate -t dev
databricks bundle deploy -t dev
databricks bundle run smoke -t dev
```

## Where outputs go
- Prep writes a **Delta table** into Unity Catalog: `<catalog>.<schema>.features_customer_churn`
- Training (extend later) should log to MLflow and register models via UC model registry
