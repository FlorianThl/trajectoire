import pytest


class TestAuth:
    async def test_register_success(self, async_client):
        resp = await async_client.post(
            "/auth/register",
            json={
                "email": "new@test.com",
                "password": "testpass123",
                "first_name": "John",
                "last_name": "Doe",
            },
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["email"] == "new@test.com"
        assert data["first_name"] == "John"

    async def test_register_duplicate(self, async_client):
        await async_client.post(
            "/auth/register",
            json={
                "email": "dup@test.com",
                "password": "testpass123",
                "first_name": "A",
                "last_name": "B",
            },
        )
        resp = await async_client.post(
            "/auth/register",
            json={
                "email": "dup@test.com",
                "password": "testpass123",
                "first_name": "A",
                "last_name": "B",
            },
        )
        assert resp.status_code == 409

    async def test_login_success(self, async_client):
        email = "login@test.com"
        await async_client.post(
            "/auth/register",
            json={
                "email": email,
                "password": "testpass123",
                "first_name": "A",
                "last_name": "B",
            },
        )
        resp = await async_client.post(
            "/auth/login",
            json={"email": email, "password": "testpass123"},
        )
        assert resp.status_code == 200
        assert "access_token" in resp.json()

    async def test_login_invalid_password(self, async_client):
        email = "badpw@test.com"
        await async_client.post(
            "/auth/register",
            json={
                "email": email,
                "password": "testpass123",
                "first_name": "A",
                "last_name": "B",
            },
        )
        resp = await async_client.post(
            "/auth/login",
            json={"email": email, "password": "wrongpass"},
        )
        assert resp.status_code == 401

    async def test_login_nonexistent(self, async_client):
        resp = await async_client.post(
            "/auth/login",
            json={"email": "nobody@test.com", "password": "testpass123"},
        )
        assert resp.status_code == 401
