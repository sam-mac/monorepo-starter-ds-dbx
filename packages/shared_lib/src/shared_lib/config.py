from __future__ import annotations

from pathlib import Path
import yaml
from pydantic import BaseModel
from dotenv import load_dotenv

def load_env() -> None:
    """Load .env (local dev convenience only)."""
    load_dotenv(override=False)

def load_yaml(path: str | Path) -> dict:
    p = Path(path)
    if not p.exists():
        return {}
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}

class StrictBaseModel(BaseModel):
    """Base for validated configs."""
    model_config = {"extra": "forbid"}
