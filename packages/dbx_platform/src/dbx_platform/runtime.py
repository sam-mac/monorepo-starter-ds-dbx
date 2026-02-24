from __future__ import annotations

from typing import Any

def in_databricks() -> bool:
    try:
        import builtins  # noqa: WPS433
        return hasattr(builtins, "dbutils")
    except Exception:
        return False

def get_spark() -> Any:
    """Return the active SparkSession (works in Databricks)."""
    try:
        from pyspark.sql import SparkSession  # type: ignore
    except Exception as e:
        raise RuntimeError(
            "pyspark is not available. This function is intended to run on Databricks compute."
        ) from e
    return SparkSession.getActiveSession() or SparkSession.builder.getOrCreate()
