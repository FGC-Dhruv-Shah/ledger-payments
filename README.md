<div align="center">

# Meridian Pay — Ledger & Payments API

**Core payments and transaction ledger service powering the Meridian Pay platform.**

[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

</div>

---

## Overview

`ledger-payments-api` is the transactional backbone of Meridian Pay. It exposes a
small, well-audited HTTP surface for recording and querying payments against
customer accounts, backed by an append-only ledger.

The service is built for correctness and auditability first: strict input typing,
parameterized data access, and structured logging are enforced conventions rather
than aspirations.

## Architecture

```
                +-------------------+
   Client  ───▶ |   FastAPI app     |   src/main.py
                |  (routing + docs) |
                +---------+---------+
                          │
             +------------▼-------------+
             |   Route handlers         |   src/routes/
             | (typed request models)   |
             +------------+-------------+
                          │
             +------------▼-------------+
             |   Data-access layer      |   src/database.py
             | (parameterized queries)  |
             +------------+-------------+
                          │
                    +-----▼-----+
                    |  SQLite   |   ledger.db  (Postgres in production)
                    +-----------+
```

**Design principles**

- **Parameterized everything** — the data layer only accepts bound parameters; SQL is never string-built from input.
- **Typed boundaries** — every request field is validated by Pydantic before it reaches business logic.
- **No secrets in source** — configuration and credentials come exclusively from the environment.
- **Auditable by default** — security-relevant events are logged with structured, non-sensitive context.

## Tech stack

| Concern        | Choice                        |
| -------------- | ----------------------------- |
| Language       | Python 3.11+                  |
| Web framework  | FastAPI                       |
| Validation     | Pydantic v2                   |
| Auth hashing   | passlib (bcrypt)              |
| Datastore      | SQLite (dev) / PostgreSQL (prod) |
| Tooling        | ruff, pytest                  |

## Getting started

```bash
# 1. Install (editable, with dev tooling)
python -m pip install -e ".[dev]"

# 2. Configure
cp .env.example .env
#   then set MERIDIAN_SECRET_KEY to a strong random value

# 3. Initialize the schema
sqlite3 ledger.db < migrations/001_initial_schema.sql

# 4. Run
uvicorn src.main:app --reload
```

Interactive API docs are then available at `http://localhost:8000/docs`.

## Project structure

```
ledger-payments-api/
├─ src/
│  ├─ main.py            # FastAPI application entrypoint
│  ├─ config.py          # environment-driven settings
│  ├─ database.py        # parameterized data-access helpers
│  ├─ auth.py            # bcrypt password hashing + user lookup
│  └─ routes/
│     └─ payments.py     # payment read endpoints
├─ migrations/
│  └─ 001_initial_schema.sql
└─ tests/
```

## Security

Security is a first-class concern for a payments service. Every pull request is
analyzed by **CodeSherlock**, which surfaces findings mapped to **CWE**
identifiers and the **OWASP Top 10** before code can be merged.

Vulnerability disclosures: `security@meridianpay.io`.

## Testing

```bash
pytest -q          # run the test suite
ruff check .       # lint
```

## License

Released under the [MIT License](LICENSE).
