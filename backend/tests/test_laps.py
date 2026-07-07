import pytest


class TestLaps:
    async def test_create_lap(self, async_client, auth_token):
        headers = {"Authorization": f"Bearer {auth_token}"}
        circuits = (await async_client.get("/circuits")).json()
        if not circuits:
            pytest.skip("No circuits available")
        resp = await async_client.post(
            "/laps",
            json={
                "circuit_id": circuits[0]["id"],
                "lap_time": "1:18.200",
                "total_laps_session": 10,
            },
            headers=headers,
        )
        assert resp.status_code == 201

    async def test_list_laps(self, async_client, auth_token):
        headers = {"Authorization": f"Bearer {auth_token}"}
        resp = await async_client.get("/laps", headers=headers)
        assert resp.status_code == 200

    async def test_create_lap_invalid_circuit(self, async_client, auth_token):
        headers = {"Authorization": f"Bearer {auth_token}"}
        resp = await async_client.post(
            "/laps",
            json={
                "circuit_id": "00000000-0000-0000-0000-000000000000",
                "lap_time": "1:20.000",
                "total_laps_session": 5,
            },
            headers=headers,
        )
        assert resp.status_code == 404
