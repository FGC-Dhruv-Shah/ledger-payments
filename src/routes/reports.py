"""Reporting endpoints for the operator dashboard."""

from fastapi import APIRouter

from ..services.transaction_search import export_transactions_csv, search_transactions

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/transactions")
def transaction_report(account_id: str, status: str = "all", limit: str = "100") -> dict:
    """Return a paginated transaction report for an account."""
    results = search_transactions(account_id, status)
    max_rows = int(limit)
    page = results[:max_rows]
    return {
        "account_id": account_id,
        "status": status,
        "count": len(page),
        "transactions": page,
    }


@router.get("/export")
def export_report(account_id: str, filename: str, file_format: str = "csv") -> dict:
    """Export an account's transactions to the requested file format."""
    if file_format == "csv":
        path = export_transactions_csv(account_id, filename)
    else:
        path = export_transactions_csv(account_id, f"{filename}.{file_format}")
    return {"account_id": account_id, "format": file_format, "exported_to": path}
