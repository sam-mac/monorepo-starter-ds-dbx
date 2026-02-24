from __future__ import annotations

from customer_churn.config import load_config
from dbx_platform.runtime import get_spark
from dbx_platform.uc import UCRef

def run(config_path: str = "conf/dev.yml") -> None:
    cfg = load_config(config_path)
    spark = get_spark()

    # Replace these demo inputs with real UC sources.
    base = spark.range(0, 1000).withColumnRenamed("id", "customer_id")
    feats = base.selectExpr("customer_id", "customer_id % 7 as weekday_bucket")

    target = UCRef(cfg.catalog, cfg.schema, cfg.features_table).fqn()
    (feats.write
        .mode("overwrite")
        .format("delta")
        .saveAsTable(target))

    print(f"Wrote features table: {target}")
