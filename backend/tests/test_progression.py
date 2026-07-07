import pytest


class TestProgression:
    async def test_progression_stats(self, async_client, auth_token):
        headers = {"Authorization": f"Bearer {auth_token}"}
        circuits = (await async_client.get("/circuits")).json()
        if not circuits:
            pytest.skip("No circuits")

        await async_client.post(
            "/laps",
            json={
                "circuit_id": circuits[0]["id"],
                "lap_time": "1:18.200",
                "total_laps_session": 10,
            },
            headers=headers,
        )

        resp = await async_client.get("/laps/stats/progression", headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)

    async def test_csv_export(self, async_client, auth_token):
        headers = {"Authorization": f"Bearer {auth_token}"}
        resp = await async_client.get("/laps/export/csv", headers=headers)
        assert resp.status_code == 200
        assert resp.headers["content-type"] == "text/csv"

    async def test_vehicle_stats(self, async_client, auth_token):
        headers = {"Authorization": f"Bearer {auth_token}"}
        resp = await async_client.get("/laps/stats/vehicle", headers=headers)
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)
