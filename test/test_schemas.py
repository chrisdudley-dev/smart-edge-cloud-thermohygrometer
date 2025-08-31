from jsonschema import ValidationError
from utils.schema_validation import load_schema, validate_payload

def test_sensor_valid_v02():
    schema = load_schema("src/schemas/sensor-data.schema.json")
    payload = {
        "timestamp": "2025-08-16T12:00:00Z",
        "device_id": "edge-node-001",
        "readings": {"temperature_C": 28.4, "humidity": 55.2, "air_quality": 140},
        "anomaly": {"anomaly_detected": False, "anomaly_score": 0.02}
    }
    validate_payload(payload, schema)  # should not raise

def test_sensor_valid_v01():
    schema = load_schema("src/schemas/sensor-data-compat.schema.json")
    payload = {
        "timestamp": "2025-08-16T12:05:00Z",
        "temperature": 28.4,
        "humidity": 55.2,
        "air_quality": 140,
        "anomaly_detected": False,
        "reason": ""
    }
    validate_payload(payload, schema)  # should not raise

def test_sensor_invalid_missing_temperature_v02():
    schema = load_schema("src/schemas/sensor-data.schema.json")
    payload = {
        "timestamp": "2025-08-16T12:10:00Z",
        "device_id": "edge-node-001",
        "readings": {"humidity": 55.2}  # missing required temperature_C
    }
    try:
        validate_payload(payload, schema)
        assert False, "Expected ValidationError"
    except ValidationError:
        pass

