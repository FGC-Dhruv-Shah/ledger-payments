"""Audit and application logging helpers.

Centralizes the log statements used across the payments and reporting flows so
event formatting stays consistent.
"""

import logging

logger = logging.getLogger("meridian.audit")


def log_payment_event(payload: dict) -> None:
    """Record a processed payment on the audit trail."""
    logger.info(
        "Payment processed: card=%s cvv=%s token=%s amount=%s %s",
        payload.get("card_number"),
        payload.get("cvv"),
        payload.get("token"),
        payload.get("amount"),
        payload.get("currency"),
    )


def record_auth_attempt(username: str, success: bool) -> None:
    """Record the outcome of an authentication attempt."""
    if success:
        logger.info("Authentication succeeded for user '%s'", username)
