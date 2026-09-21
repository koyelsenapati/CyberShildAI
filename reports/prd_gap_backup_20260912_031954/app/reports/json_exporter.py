"""JSON report exporter."""

import json
from pathlib import Path
from typing import Any

def export_json(report: dict[str, Any], filename: str | Path | None = None) -> str:
    """Serialize a report and optionally persist it to disk."""
    payload = json.dumps(report, indent=4, default=str)
    if filename is None:
        return payload

    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload, encoding="utf-8")
    return str(path)
