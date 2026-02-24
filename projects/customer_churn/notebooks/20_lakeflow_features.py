# Databricks notebook source
# MAGIC %md
# MAGIC # Lakeflow (Declarative Pipelines) — optional
# MAGIC Use Lakeflow declarative pipelines for incremental ingestion / transformations.
# MAGIC Keep model training as a Job (wheel task).

# COMMAND ----------
df = spark.range(0, 100).withColumnRenamed("id", "x")
df.createOrReplaceTempView("source")
