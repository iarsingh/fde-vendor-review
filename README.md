# Northline vendor review

Simulated forward deployed engagement for Northline Procurement. New vendor packets were sitting in a shared inbox. Analysts were one missed insurance date away from paying a vendor, and a bank-detail change had been accepted by the same person who entered it. Legal will not let software mark a packet approved.

## What the analyst gets

Clock for this sample: 2 October 2026.

| Vendor | Decision | Why |
| --- | --- | --- |
| V-1 | ready_for_human | Complete. A person still accepts it |
| V-2 | manual_review | Bank details changed |
| V-3 | blocked_incomplete | W-9 missing |
| V-4 | blocked_incomplete | Insurance expired 1 January 2025 |
| V-5 | blocked_sanctions | Flag is yes. No override |
| V-6 | blocked_incomplete | Missing W-9 is fixed before the bank review starts |

The rendered line says the tool does not approve the packet. The word approved is rejected by the code.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=src
pytest
python -m vendor eval
python -m vendor V-2
```

## Docs

- [Discovery](docs/01-discovery.md)
- [Security](docs/02-security.md)
- [Readout](docs/03-readout.md)

The pilot does not claim fraud found. It claims a bank-detail change cannot leave this tool as an acceptance.
