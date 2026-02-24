from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class UCRef:
    catalog: str
    schema: str
    name: str

    def fqn(self) -> str:
        return f"{self.catalog}.{self.schema}.{self.name}"
