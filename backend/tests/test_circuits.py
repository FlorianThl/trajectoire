import pytest


class TestCircuits:
    async def test_search_circuits(self, async_client):
        resp = await async_client.get("/circuits")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) > 0

    async def test_circuit_not_found(self, async_client):
        resp = await async_client.get(
            "/circuits/00000000-0000-0000-0000-000000000000"
        )
        assert resp.status_code == 404
