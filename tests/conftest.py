"""Shared test configuration.

Provide a throwaway secret so the app can boot under test. This is a test-only
placeholder, never a real credential, and never used outside the test suite.
"""

import os

os.environ.setdefault("MERIDIAN_SECRET_KEY", "test-only-placeholder")
os.environ.setdefault("MERIDIAN_ENVIRONMENT", "test")
