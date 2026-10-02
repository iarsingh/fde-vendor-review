from __future__ import annotations

from dataclasses import dataclass
from datetime import date


AS_OF = date(2026, 10, 2)


@dataclass(frozen=True)
class Packet:
    vendor_id: str
    w9: str
    insurance_expiry: str
    bank_change: str
    sanctions_flag: str


@dataclass(frozen=True)
class Review:
    vendor_id: str
    decision: str
    reason: str

    def render(self) -> str:
        text = (
            f"Vendor {self.vendor_id}: {self.decision}.\n"
            f"{self.reason}\n"
            "A person still has to accept this packet. The tool does not approve it.\n"
        )
        if "approved" in text.lower():
            raise RuntimeError("vendor review must not say approved")
        return text


def review_packet(packet: Packet, as_of: date = AS_OF) -> Review:
    if packet.sanctions_flag.strip().lower() == "yes":
        return Review(packet.vendor_id, "blocked_sanctions", "Sanctions flag is yes. No override in this tool.")
    incomplete = []
    if packet.w9.strip().lower() != "yes":
        incomplete.append("W-9 is missing")
    try:
        expiry = date.fromisoformat(packet.insurance_expiry)
    except ValueError:
        expiry = None
    if expiry is None or expiry < as_of:
        incomplete.append("insurance is expired or missing")
    if incomplete:
        return Review(packet.vendor_id, "blocked_incomplete", "; ".join(incomplete) + ".")
    if packet.bank_change.strip().lower() == "yes":
        return Review(
            packet.vendor_id,
            "manual_review",
            "Bank details changed. A second person reviews this before any payment setup.",
        )
    return Review(packet.vendor_id, "ready_for_human", "Packet is complete. It still waits for a person.")
