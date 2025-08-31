# src/utils/schema_validation.py
from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from jsonschema import Draft202012Validator

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = Path(__file__).resolve().parents[1]


def load_schema(rel_path: str | Path) -> dict[str, Any]:
    """
    Load a JSON schema from several candidate locations.

    Uses encoding='utf-8-sig' so files that accidentally include a UTF-8 BOM
    (common on Windows) are handled transparently.
    """
    p = Path(rel_path)
    candidates = [
        p,                       # absolute or working-dir relative
        PROJECT_ROOT / rel_path, # e.g., src/schemas/...
        SRC_ROOT / rel_path,     # e.g., schemas/...
    ]
    for cand in candidates:
        cand = Path(cand)
        if cand.exists():
            # utf-8-sig strips a BOM if present
            with open(cand, "r", encoding="utf-8-sig") as f:
                return json.load(f)
    raise FileNotFoundError(
        f"Schema not found. Tried: {', '.join(str(c) for c in candidates)}"
    )


def validate_payload(payload: dict[str, Any], schema: dict[str, Any]) -> None:
    """Validate payload against a Draft 2020-12 JSON Schema."""
    Draft202012Validator(schema).validate(payload)
