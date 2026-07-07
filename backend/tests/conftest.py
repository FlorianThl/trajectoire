import uuid

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config import settings
from app.database import Base, get_db
from app.main import app

TEST_DB_NAME = f"test_trajectoire_{uuid.uuid4().hex[:8]}"


@pytest.fixture(scope="session")
def test_db_url():
    return f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/{TEST_DB_NAME}"


@pytest_asyncio.fixture(scope="session")
async def engine(test_db_url):
    import asyncpg

    conn = await asyncpg.connect(
        user=settings.postgres_user,
        password=settings.postgres_password,
        host=settings.postgres_host,
        port=settings.postgres_port,
        database="trajectoire",
    )
    await conn.execute(f'CREATE DATABASE "{TEST_DB_NAME}" OWNER "{settings.postgres_user}"')
    await conn.close()

    e = create_async_engine(test_db_url, echo=False)

    # Enable PostGIS and create schemas
    async with e.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
        await conn.run_sync(Base.metadata.create_all)

    from geoalchemy2 import WKTElement
    from app.models.circuit import Circuit

    async with async_sessionmaker(e, expire_on_commit=False)() as session:
        existing = await session.execute(text("SELECT COUNT(*) FROM circuits"))
        if existing.scalar() == 0:
            circuits = [
                Circuit(
                    id=uuid.uuid4(),
                    name="Circuit Paul Ricard",
                    location="Le Castellet",
                    location_geo=WKTElement("POINT(5.7659 43.2523)", srid=4326),
                    length_km=5.842,
                    layout="Grand Prix",
                    runoff_type="asphalt",
                    max_noise_level_db=105,
                    has_electricity=True,
                    has_compressor=True,
                    has_sp98=True,
                ),
                Circuit(
                    id=uuid.uuid4(),
                    name="Pôle Mécanique Alès",
                    location="Alès",
                    location_geo=WKTElement("POINT(4.0833 44.1167)", srid=4326),
                    length_km=3.5,
                    layout="Trackday",
                    runoff_type="grass",
                    max_noise_level_db=102,
                    has_electricity=True,
                    has_compressor=False,
                    has_sp98=True,
                ),
            ]
            for c in circuits:
                session.add(c)
            await session.commit()

    yield e

    await e.dispose()

    conn = await asyncpg.connect(
        user=settings.postgres_user,
        password=settings.postgres_password,
        host=settings.postgres_host,
        port=settings.postgres_port,
        database="trajectoire",
    )
    await conn.execute(f'DROP DATABASE IF EXISTS "{TEST_DB_NAME}" WITH (FORCE)')
    await conn.close()


@pytest_asyncio.fixture
async def async_client(engine):
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async def override_get_db():
        async with async_session() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def auth_token(async_client):
    email = f"test_{uuid.uuid4().hex[:8]}@test.com"
    await async_client.post(
        "/auth/register",
        json={
            "email": email,
            "password": "testpass123",
            "first_name": "Test",
            "last_name": "User",
        },
    )
    resp = await async_client.post(
        "/auth/login",
        json={"email": email, "password": "testpass123"},
    )
    return resp.json()["access_token"]
