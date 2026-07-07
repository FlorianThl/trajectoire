import uuid

import pytest


class TestMaintenance:
    async def _create_vehicle(self, async_client, auth_token):
        headers = {"Authorization": f"Bearer {auth_token}"}
        resp = await async_client.post(
            "/vehicles",
            json={
                "vehicle_type": "moto",
                "brand": "Yamaha",
                "model": "R1",
                "year": 2023,
                "tires": "slicks",
                "brakes": "racing",
                "noise_level_db": 102,
            },
            headers=headers,
        )
        return resp.json()["id"], headers

    async def test_create_log(self, async_client, auth_token):
        vid, headers = await self._create_vehicle(async_client, auth_token)
        resp = await async_client.post(
            f"/vehicles/{vid}/maintenance",
            json={"consumable": "plaquettes", "max_laps": 100},
            headers=headers,
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["consumable"] == "plaquettes"
        assert data["max_laps"] == 100
        assert data["current_laps"] == 0

    async def test_list_logs(self, async_client, auth_token):
        vid, headers = await self._create_vehicle(async_client, auth_token)
        resp = await async_client.get(f"/vehicles/{vid}/maintenance", headers=headers)
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    async def test_update_log(self, async_client, auth_token):
        vid, headers = await self._create_vehicle(async_client, auth_token)
        create_resp = await async_client.post(
            f"/vehicles/{vid}/maintenance",
            json={"consumable": "disques", "max_laps": 200},
            headers=headers,
        )
        log_id = create_resp.json()["id"]
        resp = await async_client.patch(
            f"/vehicles/{vid}/maintenance/{log_id}",
            json={"current_laps": 50},
            headers=headers,
        )
        assert resp.status_code == 200
        assert resp.json()["current_laps"] == 50

    async def test_delete_log(self, async_client, auth_token):
        vid, headers = await self._create_vehicle(async_client, auth_token)
        create_resp = await async_client.post(
            f"/vehicles/{vid}/maintenance",
            json={"consumable": "huile", "max_laps": 50},
            headers=headers,
        )
        log_id = create_resp.json()["id"]
        resp = await async_client.delete(
            f"/vehicles/{vid}/maintenance/{log_id}", headers=headers
        )
        assert resp.status_code == 204

    async def test_unauthorized(self, async_client):
        resp = await async_client.get(
            f"/vehicles/{uuid.uuid4()}/maintenance"
        )
        assert resp.status_code == 403

    async def test_vehicle_not_found(self, async_client, auth_token):
        headers = {"Authorization": f"Bearer {auth_token}"}
        resp = await async_client.get(
            f"/vehicles/{uuid.uuid4()}/maintenance", headers=headers
        )
        assert resp.status_code == 404

    async def test_lap_auto_increments_maintenance(self, async_client, auth_token):
        vid, headers = await self._create_vehicle(async_client, auth_token)
        await async_client.post(
            f"/vehicles/{vid}/maintenance",
            json={"consumable": "plaquettes", "max_laps": 100},
            headers=headers,
        )
        circuits = (await async_client.get("/circuits")).json()
        if not circuits:
            pytest.skip("No circuits")
        await async_client.post(
            "/laps",
            json={
                "circuit_id": circuits[0]["id"],
                "vehicle_id": vid,
                "lap_time": "1:20.000",
                "total_laps_session": 15,
            },
            headers=headers,
        )
        logs = (await async_client.get(f"/vehicles/{vid}/maintenance", headers=headers)).json()
        assert len(logs) > 0
        assert logs[0]["current_laps"] >= 15
