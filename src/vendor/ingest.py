from __future__ import annotations

import csv
import json
from pathlib import Path

from vendor.policy import Packet

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
EVALS_PATH = ROOT / "evals" / "questions.jsonl"


def load_packets() -> dict[str, Packet]:
    packets = {}
    with (DATA_DIR / "packets.csv").open(newline="") as handle:
        for row in csv.DictReader(handle):
            packet = Packet(
                vendor_id=row["vendor_id"],
                w9=row["w9"],
                insurance_expiry=row["insurance_expiry"],
                bank_change=row["bank_change"],
                sanctions_flag=row["sanctions_flag"],
            )
            packets[packet.vendor_id] = packet
    return packets


def load_cases(path: Path | None = None) -> list[dict]:
    return [json.loads(line) for line in (path or EVALS_PATH).read_text().splitlines() if line.strip()]
