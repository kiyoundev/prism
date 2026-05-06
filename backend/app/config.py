import os
import sys


def require_env(name: str) -> str:
    """
    Get environment variable or exit with error message
    """
    value = os.getenv(name)
    if not value:
        sys.exit(f"Missing required environment variable: {name}")
    return value


DATABASE_URL = require_env("DATABASE_URL")
ANTHROPIC_API_KEY = require_env("ANTHROPIC_API_KEY")
INTERNAL_API_KEY = require_env("INTERNAL_API_KEY")
