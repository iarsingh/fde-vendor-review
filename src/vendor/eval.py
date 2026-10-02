from __future__ import annotations

from pathlib import Path

from vendor.ingest import load_cases, load_packets
from vendor.policy import review_packet


def run(path: Path | None = None) -> int:
    packets = load_packets()
    failures = []
    cases = load_cases(path)
    for case in cases:
        review = review_packet(packets[case["vendor_id"]])
        if review.decision != case["expected_decision"]:
            failures.append(f"{case['vendor_id']}: {review.decision}")
        if "approved" in review.render().lower():
            failures.append(f"{case['vendor_id']}: said approved")
    if failures:
        print(f"{len(failures)} eval failure(s)")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"{len(cases)} eval cases passed")
    return 0
