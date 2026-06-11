import asyncio

import psycopg


class PostgresReadiness:
    """Checks Postgres readiness with a light `SELECT 1` under a short timeout."""

    def __init__(self, database_url: str, timeout_seconds: float) -> None:
        self._database_url = database_url
        self._timeout_seconds = timeout_seconds

    async def database_is_ready(self) -> bool:
        try:
            await asyncio.wait_for(self._run_readiness_query(), self._timeout_seconds)
        except (psycopg.Error, OSError, TimeoutError):
            return False
        return True

    async def _run_readiness_query(self) -> None:
        async with await psycopg.AsyncConnection.connect(self._database_url) as connection:
            await connection.execute("SELECT 1")
