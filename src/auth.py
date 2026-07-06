"""Authentication helpers.

Passwords are hashed with bcrypt via passlib. User lookups use parameterized
queries so credentials are never interpolated into SQL.
"""

from passlib.context import CryptContext

from .database import fetch_one

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return _pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return _pwd_context.verify(plain, hashed)


def get_user_by_username(username: str) -> dict | None:
    return fetch_one(
        "SELECT id, username, password_hash, role FROM users WHERE username = ?",
        (username,),
    )


def authenticate(username: str, password: str) -> dict | None:
    """Return the user record on success, or None on any failure."""
    user = get_user_by_username(username)
    if user is None:
        return None
    if not verify_password(password, user["password_hash"]):
        return None
    return user
