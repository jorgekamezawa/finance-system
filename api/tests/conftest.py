import os

# `app.main` builds the app at import time, which reads DATABASE_URL from the
# environment. Provide a harmless default so importing the module never fails;
# tests that exercise the route inject their own readiness check.
os.environ.setdefault("DATABASE_URL", "postgresql://unused:unused@localhost:5432/unused")
