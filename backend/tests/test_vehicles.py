import pytest


class TestVehicles:
    async def test_create_vehicle(self, async_client, auth_token):
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
        assert resp.status_code == 201
        data = resp.json()
        assert data["brand"] == "Yamaha"
        assert data["model"] == "R1"

    async def test_list_vehicles(self, async_client, auth_token):
        headers = {"Authorization": f"Bearer {auth_token}"}
        resp = await async_client.get("/vehicles", headers=headers)
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    async def test_get_vehicle(self, async_client, auth_token):
        headers = {"Authorization": f"Bearer {auth_token}"}
        create_resp = await async_client.post(
            "/vehicles",
            json={
                "vehicle_type": "auto",
                "brand": "Porsche",
                "model": "911 GT3",
                "year": 2022,
                "tires": "semi-slicks",
                "brakes": "racing",
                "noise_level_db": 108,
            },
            headers=headers,
        )
        vehicle_id = create_resp.json()["id"]
        resp = await async_client.get(f"/vehicles/{vehicle_id}", headers=headers)
        assert resp.status_code == 200
        assert resp.json()["brand"] == "Porsche"

    async def test_update_vehicle(self, async_client, auth_token):
        headers = {"Authorization": f"Bearer {auth_token}"}
        create_resp = await async_client.post(
            "/vehicles",
            json={
                "vehicle_type": "moto",
                "brand": "Kawasaki",
                "model": "ZX-10R",
                "year": 2023,
                "tires": "slicks",
                "brakes": "racing",
                "noise_level_db": 104,
            },
            headers=headers,
        )
        vehicle_id = create_resp.json()["id"]
        resp = await async_client.patch(
            f"/vehicles/{vehicle_id}",
            json={"noise_level_db": 106},
            headers=headers,
        )
        assert resp.status_code == 200
        assert resp.json()["noise_level_db"] == 106

    async def test_delete_vehicle(self, async_client, auth_token):
        headers = {"Authorization": f"Bearer {auth_token}"}
        create_resp = await async_client.post(
            "/vehicles",
            json={
                "vehicle_type": "moto",
                "brand": "Ducati",
                "model": "Panigale V4",
                "year": 2024,
                "tires": "slicks",
                "brakes": "racing",
                "noise_level_db": 108,
            },
            headers=headers,
        )
        vehicle_id = create_resp.json()["id"]
        resp = await async_client.delete(f"/vehicles/{vehicle_id}", headers=headers)
        assert resp.status_code == 204

    async def test_unauthorized(self, async_client):
        resp = await async_client.get("/vehicles")
        assert resp.status_code == 403
