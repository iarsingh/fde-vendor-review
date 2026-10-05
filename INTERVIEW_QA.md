# fde-vendor-review — interview questions and answers

[README](README.md) · [Project architecture](PROJECT_ARCHITECTURE.md)

Answers below use this repository’s files and implementation. They distinguish existing behavior from suggested extensions; source links let you verify each walkthrough.

## 1. What problem does fde-vendor-review address, and what can you demonstrate?

Simulated forward deployed engagement for Northline Procurement. New vendor packets were sitting in a shared inbox. Analysts were one missed insurance date away from paying a vendor, and a bank-detail change had been accepted by the same person who entered it. Legal will not let software mark a packet approved.

I would demonstrate the linked implementation or examples and distinguish that evidence from any planned production features. Start with [`README.md`](README.md).

## 2. How is this repository organized?

- [`src/vendor/policy.py`](src/vendor/policy.py): Implementation or supporting configuration.
- [`src/vendor/eval.py`](src/vendor/eval.py): Implementation or supporting configuration.
- [`src/vendor/ingest.py`](src/vendor/ingest.py): Implementation or supporting configuration.
- [`requirements.txt`](requirements.txt): Implementation or supporting configuration.
- [`src/vendor/__init__.py`](src/vendor/__init__.py): Implementation or supporting configuration.
- [`src/vendor/__main__.py`](src/vendor/__main__.py): Implementation or supporting configuration.
- [`Dockerfile`](Dockerfile): Container build/service configuration.
- [`tests/test_policy.py`](tests/test_policy.py): Executable checks and regression examples.

[PROJECT_ARCHITECTURE.md](PROJECT_ARCHITECTURE.md) contains the component diagram and the implementation walkthrough.

## 3. Can you walk through `review_packet` and explain the decision it makes?

The main walkthrough here is `review_packet(packet: Packet, as_of: date=AS_OF)` in [`src/vendor/policy.py`](src/vendor/policy.py#L36).

```python
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
```

This is an excerpt; follow the source link for the rest of the branches.

The implementation calls `'; '.join`, `Review`, `date.fromisoformat`, `incomplete.append`, `packet.bank_change.strip`, `packet.bank_change.strip().lower`, `packet.sanctions_flag.strip`, `packet.sanctions_flag.strip().lower`, `packet.w9.strip`. In an interview, trace those calls in execution order using a fixture input.

## 4. What responsibility does `run` have?

`run(path: Path | None=None)` is defined in [`src/vendor/eval.py`](src/vendor/eval.py#L9).

Its return expressions include:

- `0`
- `1`

It uses `failures.append`, `len`, `load_cases`, `load_packets`, `print`, `review.render`, `review.render().lower`, `review_packet`. This is the code path I would compare against the caller to explain responsibility boundaries.

## 5. What input validation and failure behavior are implemented?

Explicit failure paths include:

- `SystemExit(main())` in [`src/vendor/__main__.py`](src/vendor/__main__.py#L23).
- `RuntimeError('vendor review must not say approved')` in [`src/vendor/policy.py`](src/vendor/policy.py#L32).

I would test both the condition that reaches each exception and the caller that translates it. An explicit raise does not mean every malformed input or dependency failure is handled.

## 6. Which test would you use to demonstrate correctness?

[`tests/test_policy.py`](tests/test_policy.py#L6) contains `test_eval_file_passes`:

```python
def test_eval_file_passes():
    assert run(EVALS_PATH) == 0
```

This is a concrete regression example from the repository. Its assertions establish that case; they do not establish behavior for every input or under production load.

## 7. How do you separate the current design from a future production design?

The current design is the source/component map in [PROJECT_ARCHITECTURE.md](PROJECT_ARCHITECTURE.md). A future deployment needs explicit input contracts, persistence decisions, authentication, monitoring, and rollback. I would present these as proposed work until the corresponding implementation and verification exist.

## 8. How would you investigate data ownership and persistence?

Trace the data/configuration files and the code that reads or writes them in the component table. Identify which files are examples, which records are mutable, and which external store is actually configured. I would document those facts before discussing retention, backup, or tenant isolation.

## 9. How would another engineer reproduce your walkthrough?

Start from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

These commands follow repository manifests; environment setup and command results still need to be checked on the target machine.

## 10. What does automation verify, and what does it not prove?

Inspect [`.github/workflows/ci.yml`](.github/workflows/ci.yml) for triggers, permissions, and job commands. I would name the checks that those definitions run and show the latest run separately. A workflow definition alone does not establish a successful deployment, security review, or production SLO.

## 11. How would you present this project in a Forward Deployed Engineer interview?

Start with the user and operational problem described in [`README.md`](README.md). Explain one constraint that changes the implementation, show the linked code or example, and walk through a success case and a failure case. Agree on a measurable acceptance criterion before expanding the solution, and leave a handoff with data boundaries and rollback ownership. Any proposed production or business metric should be identified as a target until measured.

## 12. What is the input-to-output contract of `review_packet`?

In [`src/vendor/policy.py`](src/vendor/policy.py#L36), `review_packet(packet: Packet, as_of: date=AS_OF)` receives the inputs. The function computes these intermediate values:

- `incomplete = []`

Its result is defined by:

- `Review(packet.vendor_id, 'ready_for_human', 'Packet is complete. It still waits for a person.')`
- `Review(packet.vendor_id, 'blocked_sanctions', 'Sanctions flag is yes. No override in this tool.')`
- `Review(packet.vendor_id, 'blocked_incomplete', '; '.join(incomplete) + '.')`

## 13. Which decision rules or boundary conditions should an interviewer challenge?

The implementation in [`src/vendor/policy.py`](src/vendor/policy.py#L36) branches on:

- `packet.sanctions_flag.strip().lower() == 'yes'`
- `packet.w9.strip().lower() != 'yes'`
- `expiry is None or expiry < as_of`
- `incomplete`
- `packet.bank_change.strip().lower() == 'yes'`

A useful extension is a table-driven test that covers each condition just below, at, and above its boundary where applicable. These expressions are the current rules; changing them changes behavior and should be justified by the project’s acceptance criteria.
