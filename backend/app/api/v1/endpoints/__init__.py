# This file makes the endpoints directory a Python package

from . import auth, jobs

__all__ = ["auth", "jobs"]
