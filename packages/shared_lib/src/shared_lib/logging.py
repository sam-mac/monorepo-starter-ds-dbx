from __future__ import annotations

import logging
from rich.logging import RichHandler

def configure_logging(level: int = logging.INFO) -> None:
    """Team-friendly logging (pretty + readable)."""
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)],
    )
