from __future__ import annotations

import sys

from vendor.eval import run
from vendor.ingest import load_packets
from vendor.policy import review_packet


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "eval":
        return run()
    vendor_id = sys.argv[1] if len(sys.argv) > 1 else "V-2"
    packet = load_packets().get(vendor_id)
    if packet is None:
        print(f"Unknown vendor {vendor_id}", file=sys.stderr)
        return 1
    print(review_packet(packet).render())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
