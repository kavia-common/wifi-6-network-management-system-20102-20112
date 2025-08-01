def test_list_devices_requires_auth(client):
    resp = client.get("/devices/")
    assert resp.status_code == 401

def test_device_crud(client, auth_headers):
    # List all devices (should return pre-seeded dummy devices)
    resp = client.get("/devices/", headers=auth_headers)
    assert resp.status_code == 200

    # Add device
    new_device = {
        "name": "TestDevice123",
        "mac": "00:AA:BB:CC:DD:FF",
        "ip": "10.0.2.2"
    }
    resp2 = client.post("/devices/", json=new_device, headers=auth_headers)
    assert resp2.status_code == 201
    created = resp2.json()
    assert created["name"] == new_device["name"]
    assert created["mac"] == new_device["mac"]
    assert created["ip"] == new_device["ip"]
    assert created["device_status"] == "online"
    new_id = created["id"]

    # Get device by id
    resp3 = client.get(f"/devices/{new_id}", headers=auth_headers)
    assert resp3.status_code == 200
    dev = resp3.json()
    assert dev["id"] == new_id

    # Update device
    updated_info = {
        "name": "UpdatedDevice",
        "mac": "00:AA:BB:CC:DD:FF",
        "ip": "10.0.2.99"
    }
    resp4 = client.put(f"/devices/{new_id}", json=updated_info, headers=auth_headers)
    assert resp4.status_code == 200
    assert resp4.json()["name"] == "UpdatedDevice"

    # Delete device
    resp5 = client.delete(f"/devices/{new_id}", headers=auth_headers)
    assert resp5.status_code == 204

    # Confirm deleted
    resp6 = client.get(f"/devices/{new_id}", headers=auth_headers)
    assert resp6.status_code == 404

def test_get_device_not_found(client, auth_headers):
    resp = client.get("/devices/9999", headers=auth_headers)
    assert resp.status_code == 404

def test_update_device_not_found(client, auth_headers):
    payload = {
        "name": "NoDevice",
        "mac": "00:00:00:00:00:01",
        "ip": "1.2.3.4"
    }
    resp = client.put("/devices/9999", json=payload, headers=auth_headers)
    assert resp.status_code == 404

def test_delete_device_not_found(client, auth_headers):
    resp = client.delete("/devices/9999", headers=auth_headers)
    assert resp.status_code == 404
