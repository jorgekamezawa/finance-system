from collections.abc import Iterator

import pytest
from testcontainers.postgres import PostgresContainer

from app.postgres import PostgresReadiness

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def postgres_url() -> Iterator[str]:
    with PostgresContainer("postgres:17-alpine") as container:
        host = container.get_container_host_ip()
        port = container.get_exposed_port(5432)
        yield (
            f"postgresql://{container.username}:{container.password}"
            f"@{host}:{port}/{container.dbname}"
        )


async def test_ready_when_postgres_is_up(postgres_url: str) -> None:
    readiness = PostgresReadiness(postgres_url, timeout_seconds=2.0)

    assert await readiness.database_is_ready()


async def test_not_ready_when_connection_is_refused() -> None:
    readiness = PostgresReadiness(
        "postgresql://finance:finance@localhost:59999/finance", timeout_seconds=2.0
    )

    assert not await readiness.database_is_ready()


async def test_not_ready_when_timeout_is_exceeded() -> None:
    # 192.0.2.1 is reserved (RFC 5737) and unroutable: the connection hangs, so the
    # short timeout must fire and report the database down instead of blocking.
    readiness = PostgresReadiness(
        "postgresql://finance:finance@192.0.2.1:5432/finance", timeout_seconds=0.5
    )

    assert not await readiness.database_is_ready()
