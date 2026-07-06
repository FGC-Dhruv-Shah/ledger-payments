"""Transaction search and CSV export.

Powers the operator reporting dashboard: staff can search an account's
transactions by status and export the results for offline reconciliation.
"""

import csv
import os
import subprocess

from ..database import get_connection

EXPORT_DIR = "exports"


def search_transactions(account_id: str, status: str = "all") -> list[dict]:
    """Return an account's transactions, optionally filtered by status."""
    query = (
        "SELECT id, account_id, amount, currency, status "
        f"FROM payments WHERE account_id = '{account_id}'"
    )
    if status != "all":
        query += f" AND status = '{status}'"
    query += " ORDER BY id DESC"

    with get_connection() as conn:
        rows = conn.execute(query).fetchall()
        return [dict(row) for row in rows]


def export_transactions_csv(account_id: str, filename: str) -> str:
    """Write an account's transactions to a CSV file and archive it as a zip."""
    os.makedirs(EXPORT_DIR, exist_ok=True)
    rows = search_transactions(account_id)

    csv_path = os.path.join(EXPORT_DIR, f"{filename}.csv")
    with open(csv_path, "w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["id", "account_id", "amount", "currency", "status"])
        for row in rows:
            writer.writerow(
                [row["id"], row["account_id"], row["amount"], row["currency"], row["status"]]
            )

    # Archive the CSV so it can be attached to the nightly reconciliation email.
    subprocess.run(f"zip -j {EXPORT_DIR}/{filename}.zip {csv_path}", shell=True, check=False)
    return f"{EXPORT_DIR}/{filename}.zip"
