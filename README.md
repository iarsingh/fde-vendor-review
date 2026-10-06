# Northline vendor review

<!-- project-guide:start -->
## Project guide

[Project architecture](PROJECT_ARCHITECTURE.md) · [Interview questions and answers](INTERVIEW_QA.md)

Use the architecture document for the component diagram, implementation boundaries, and verification entry points. The interview guide includes source-backed answers and project walkthroughs.

### Implementation map

| Component | Responsibility |
| --- | --- |
| [`src/vendor/policy.py`](src/vendor/policy.py) | Functions: `review_packet`, `render` |
| [`src/vendor/eval.py`](src/vendor/eval.py) | Functions: `run` |
| [`src/vendor/ingest.py`](src/vendor/ingest.py) | Functions: `load_packets`, `load_cases` |
| [`requirements.txt`](requirements.txt) | Implementation or supporting configuration |
| [`src/vendor/__init__.py`](src/vendor/__init__.py) | Implementation or supporting configuration |
| [`src/vendor/__main__.py`](src/vendor/__main__.py) | Functions: `main` |
| [`Dockerfile`](Dockerfile) | Container build/service configuration |
| [`tests/test_policy.py`](tests/test_policy.py) | Executable checks and regression examples |
| [`.github/workflows/ci.yml`](.github/workflows/ci.yml) | GitHub Actions job definitions |
| [`README.md`](README.md) | Project explanations or operating notes |
| [`docs/01-discovery.md`](docs/01-discovery.md) | Project explanations or operating notes |
| [`docs/02-security.md`](docs/02-security.md) | Project explanations or operating notes |

### Local setup and verification

From the repository root (the commands follow the checked-in manifests):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

<!-- project-guide:end -->

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

## Documentation checks

Project architecture, interview guides, and local source links are checked automatically on pushes and pull requests. Run the same check locally:

```bash
python3 .github/scripts/validate_project_docs.py
```
