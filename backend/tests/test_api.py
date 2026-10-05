def test_create_road(client):
    response = client.post(
        "/api/v1/roads/",
        json={
            "road_id": "R001",
            "road_name": "Main St",
            "district": "Downtown",
            "latitude": 10.0,
            "longitude": 20.0
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["road_id"] == "R001"
    assert data["road_name"] == "Main St"
    assert "id" in data

def test_get_roads(client):
    response = client.get("/api/v1/roads/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert len(data["items"]) >= 1

def test_create_traffic_record(client):
    response = client.post(
        "/api/v1/traffic/",
        json={
            "road_id": "R001",
            "timestamp": "2023-10-01T12:00:00Z",
            "vehicle_count": 150,
            "avg_speed": 45.5,
            "source": "sensor_1"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["vehicle_count"] == 150
    assert data["road_id"] == "R001"
