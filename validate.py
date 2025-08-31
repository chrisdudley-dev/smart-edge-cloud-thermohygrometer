#!/usr/bin/env python3
from pathlib import Path
import sys, json, argparse

# add ./src to the import path so "utils" resolves when running from project root
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from utils.schema_validation import load_schema, validate_payload

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--schema", required=True)   # e.g. src/schemas/sensor-data.schema.json
    ap.add_argument("json_file")                 # e.g. test_payload_v02.json
    args = ap.parse_args()

    schema = load_schema(args.schema)
    with open(args.json_file, "r", encoding="utf-8") as f:
        payload = json.load(f)
    validate_payload(payload, schema)
    print("OK")

if __name__ == "__main__":
    main()

