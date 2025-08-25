# src/utils/schema_validation.py
import json
from pathlib import Path
from jsonschema import Draft202012Validator

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = Path(__file__).resolve().parents[1]

def load_schema(rel_path: str):
    p = Path(rel_path)
    candidates = [
        p,                              # absolute or working-dir relative
        PROJECT_ROOT / rel_path,        # e.g., src/schemas/...
        SRC_ROOT / rel_path,            # e.g., schemas/...
    ]
    for cand in candidates:
        if cand.exists():
            with open(cand, "r", encoding="utf-8") as f:
                return json.load(f)
    raise FileNotFoundError(f"Schema not found. Tried: {', '.join(str(c) for c in candidates)}")

def validate_payload(payload: dict, schema: dict) -> None:
    Draft202012Validator(schema).validate(payload)
