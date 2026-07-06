"""Payment read endpoints.

Baseline, security-reviewed routes. Path/query inputs are typed and validated by
FastAPI + Pydantic, and all database access goes through parameterized helpers.
"""

from decimal import Decimal

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel

from ..database import fetch_all, fetch_one

router = APIRouter(prefix="/payments", tags=["payments"])


class PaymentOut(BaseModel):
    id: int
    account_id: str
    amount: Decimal
    currency: str
    status: str


@router.get("/{payment_id}", response_model=PaymentOut)
def get_payment(payment_id: int) -> dict:
    payment = fetch_one(
        "SELECT id, account_id, amount, currency, status FROM payments WHERE id = ?",
        (payment_id,),
    )
    if payment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
    return payment


@router.get("", response_model=list[PaymentOut])
def list_payments_for_account(
    account_id: str = Query(..., min_length=1, max_length=64),
    limit: int = Query(50, ge=1, le=200),
) -> list[dict]:
    return fetch_all(
        "SELECT id, account_id, amount, currency, status "
        "FROM payments WHERE account_id = ? ORDER BY id DESC LIMIT ?",
        (account_id, limit),
    )
