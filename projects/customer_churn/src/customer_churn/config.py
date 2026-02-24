from __future__ import annotations

from pathlib import Path
import yaml
from pydantic import Field
from shared_lib.config import StrictBaseModel

class ProjectConfig(StrictBaseModel):
    env: str = "dev"
    catalog: str = Field(..., description="Unity Catalog catalog")
    schema: str = Field(..., description="Unity Catalog schema")
    features_table: str = "features_customer_churn"

def load_config(path: str | Path) -> ProjectConfig:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    return ProjectConfig.model_validate(data)
