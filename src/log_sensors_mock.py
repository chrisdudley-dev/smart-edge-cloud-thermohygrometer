#!/usr/bin/env python3
"""
Basic mock sensor logger for the Smart Edge–Cloud Monitor project.

Generates plausible temperature/humidity readings (as if from a DHT22)
without requiring any hardware. Outputs JSON Lines (one object per line)
with the following shape:

{
  "timestamp": "2025-08-06T22:11:03Z",
  "temperature_C": 24.6,
  "humidity": 52.4,
  "device_id": "edge-node-001"
}

Usage (examples):
    python log_sensors_mock.py --count 60 --interval 2 \
        --device-id edge-node-001 --output data/sensor_log.jsonl

Notes:
- Designed to be drop-in compatible with the Day 15 payload structure.
- Keep this file hardware-agnostic; real sensor integrations should live
  in dedicated modules (e.g., src/sensors/dht22.py) later.
- Future: optionally validate against your JSON Schemas (v0.1 / v0.2).

Runtime baseline: Python 3.9+
"""
from __future__ import annotations

import argparse
import json
import logging
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
import random
import time
from typing import Optional
from tempfile import TemporaryDirectory


# ----------------------------
# Data model
# ----------------------------
@dataclass
class SensorReading:
    timestamp: str
    temperature_C: float
    humidity: float
    device_id: str


# ----------------------------
# Time helpers
# ----------------------------
ISO_FMT = "%Y-%m-%dT%H:%M:%SZ"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime(ISO_FMT)


# ----------------------------
# Mock sensor
# ----------------------------
class MockDHT22:
    """Simple, reproducible-ish mock for temperature and humidity.

    Produces values that gently drift within realistic indoor ranges.
    """

    def __init__(
            self,
            seed: Optional[int] = None,
            temp_start: float = 23.5,
            hum_start: float = 50.0,
            temp_bounds: tuple[float, float] = (18.0, 30.0),
            hum_bounds: tuple[float, float] = (30.0, 70.0),
            temp_step_sigma: float = 0.15,
            hum_step_sigma: float = 0.4,
    ) -> None:
        self._rng = random.Random(seed)
        self._t = temp_start
        self._h = hum_start
        self._t_bounds = temp_bounds
        self._h_bounds = hum_bounds
        self._t_sigma = temp_step_sigma
        self._h_sigma = hum_step_sigma

    def read(self) -> tuple[float, float]:
        # random walk with reflecting bounds
        self._t += self._rng.gauss(0, self._t_sigma)
        self._h += self._rng.gauss(0, self._h_sigma)

        t_min, t_max = self._t_bounds
        h_min, h_max = self._h_bounds

        # reflect if out of bounds
        if self._t < t_min or self._t > t_max:
            self._t = max(min(self._t, t_max), t_min)
            self._t += self._rng.gauss(0, self._t_sigma) * (-1)
        if self._h < h_min or self._h > h_max:
            self._h = max(min(self._h, h_max), h_min)
            self._h += self._rng.gauss(0, self._h_sigma) * (-1)

        # round to tenths for temperature, tenths for humidity
        return round(self._t, 1), round(self._h, 1)


# ----------------------------
# Core logger
# ----------------------------
class JSONLWriter:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, obj: dict) -> None:
        line = json.dumps(obj, ensure_ascii=False)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(line + "\n")


def emit_reading(device_id: str, sensor: MockDHT22) -> SensorReading:
    temp_c, h_pct = sensor.read()
    return SensorReading(
        timestamp=utc_now_iso(),
        temperature_C=float(temp_c),
        humidity=float(h_pct),
        device_id=device_id,
    )


# ----------------------------
# CLI
# ----------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Generate mock temperature/humidity readings and log them as JSON Lines.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--device-id", default="edge-node-001", help="Logical device identifier")
    p.add_argument("--interval", type=float, default=2.0, help="Seconds between readings")
    p.add_argument("--count", type=int, default=30, help="Number of readings to generate (0 = infinite)")
    p.add_argument("--output", type=Path, default=Path("data/sensor_log.jsonl"), help="Path to JSONL output file")
    p.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    p.add_argument(
        "--no-stdout",
        action="store_true",
        help="Do not also echo readings to stdout while logging to file",
    )
    p.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logger verbosity",
    )
    p.add_argument(
        "--self-test",
        action="store_true",
        help="Run built-in smoke tests and exit.",
    )
    return p.parse_args()


def setup_logging(level: str) -> None:
    # noinspection SpellCheckingInspection
    logging.basicConfig(
        level=getattr(logging, level),
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def run(
        device_id: str,
        interval: float,
        count: int,
        output: Path,
        seed: Optional[int],
        echo_stdout: bool,
) -> None:
    writer = JSONLWriter(output)
    sensor = MockDHT22(seed=seed)

    n = 0
    try:
        while True:
            reading = emit_reading(device_id, sensor)
            obj = asdict(reading)

            writer.append(obj)
            if echo_stdout:
                print(json.dumps(obj, ensure_ascii=False), flush=True)

            n += 1
            if 0 < count <= n:
                break
            time.sleep(max(0.0, interval))
    except KeyboardInterrupt:
        logging.info("Interrupted by user; exiting.")


# ----------------------------
# Self-tests (lightweight, no external deps)
# ----------------------------

def _self_tests() -> None:
    """Run a few invariants to sanity-check behavior.

    These tests are *in-module* so you can run them via:
        python src/log_sensors_mock.py --self-test
    """
    from json import loads

    with TemporaryDirectory() as td:
        path = Path(td) / "out.jsonl"
        # Generate a few readings quickly
        run(
            device_id="self-test-node",
            interval=0.0,
            count=5,
            output=path,
            seed=123,
            echo_stdout=False,
        )
        lines = path.read_text(encoding="utf-8").splitlines()
        assert len(lines) == 5, f"expected 5 lines, got {len(lines)}"
        for i, line in enumerate(lines):
            obj = loads(line)
            for key in ("timestamp", "temperature_C", "humidity", "device_id"):
                assert key in obj, f"missing key {key} in line {i}: {obj}"
            # Type checks
            assert isinstance(obj["timestamp"], str)
            assert isinstance(obj["temperature_C"], (int, float))
            assert isinstance(obj["humidity"], (int, float))
            assert isinstance(obj["device_id"], str)
            # Range checks (loose bounds)
            assert 10.0 <= obj["temperature_C"] <= 40.0
            assert 0.0 <= obj["humidity"] <= 100.0

        # Determinism with same seed
        path_a = Path(td) / "a.jsonl"
        path_b = Path(td) / "b.jsonl"
        args = dict(device_id="seeded", interval=0.0, count=3, seed=42, echo_stdout=False)
        run(output=path_a, **args)
        run(output=path_b, **args)
        lines_a = path_a.read_text(encoding="utf-8").splitlines()
        lines_b = path_b.read_text(encoding="utf-8").splitlines()
        assert lines_a == lines_b, "same seed should produce identical sequence"


# ----------------------------
# Entry point
# ----------------------------
if __name__ == "__main__":
    args = parse_args()
    setup_logging(args.log_level)

    if args.self_test:
        _self_tests()
        logging.info("Self-tests passed.")
        raise SystemExit(0)

    run(
        device_id=args.device_id,
        interval=args.interval,
        count=args.count,
        output=args.output,
        seed=args.seed,
        echo_stdout=not args.no_stdout,
    )
