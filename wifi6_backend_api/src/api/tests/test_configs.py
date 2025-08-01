def test_list_configs_requires_auth(client):
    resp = client.get("/configs/")
    assert resp.status_code == 401

def test_config_crud(client, auth_headers):
    # List configs (should have dummy configs)
    resp = client.get("/configs/", headers=auth_headers)
    assert resp.status_code == 200

    # Create new config
    new_cfg = {
        "device_id": 1,
        "ssid": "SuperNet",
        "password": "supersecret",
        "channel": 64,
        "wpa3_enabled": True
    }
    resp2 = client.post("/configs/", json=new_cfg, headers=auth_headers)
    assert resp2.status_code == 201
    created = resp2.json()
    assert created["ssid"] == "SuperNet"
    cfg_id = created["id"]

    # Get config by id
    resp3 = client.get(f"/configs/{cfg_id}", headers=auth_headers)
    assert resp3.status_code == 200
    assert resp3.json()["id"] == cfg_id

    # Update config
    update_data = {
        "device_id": 1,
        "ssid": "UpdatedSSID",
        "password": "UPDpwA123",
        "channel": 100,
        "wpa3_enabled": False
    }
    resp4 = client.put(f"/configs/{cfg_id}", json=update_data, headers=auth_headers)
    assert resp4.status_code == 200
    assert resp4.json()["ssid"] == "UpdatedSSID"

    # Delete config
    resp5 = client.delete(f"/configs/{cfg_id}", headers=auth_headers)
    assert resp5.status_code == 204

    # Confirm deleted
    resp6 = client.get(f"/configs/{cfg_id}", headers=auth_headers)
    assert resp6.status_code == 404

def test_get_config_not_found(client, auth_headers):
    resp = client.get("/configs/9999", headers=auth_headers)
    assert resp.status_code == 404

def test_update_config_not_found(client, auth_headers):
    payload = {
        "device_id": 2,
        "ssid": "Missing",
        "password": "pw",
        "channel": 10,
        "wpa3_enabled": True
    }
    resp = client.put("/configs/9999", json=payload, headers=auth_headers)
    assert resp.status_code == 404

def test_delete_config_not_found(client, auth_headers):
    resp = client.delete("/configs/9999", headers=auth_headers)
    assert resp.status_code == 404

def test_list_device_configs(client, auth_headers):
    # Assumes dummy_configs in code with at least device_id=1 and device_id=2
    resp = client.get("/configs/device/1", headers=auth_headers)
    assert resp.status_code == 200
    cfgs = resp.json()
    # All configs here should have device_id=1
    assert all(cfg["device_id"] == 1 for cfg in cfgs)
