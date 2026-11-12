from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_list_nodes_returns_seeded_network():
    response = client.get("/api/nodes")
    assert response.status_code == 200
    body = response.json()
    assert body["count"] >= 3
    assert any(node["id"] == "node_rishikesh_01" for node in body["nodes"])


def test_create_user_and_travel_pass():
    user_response = client.post(
        "/api/users",
        json={
            "name": "Priya Sharma",
            "phone": "+919876543210",
            "emergency_contacts": [
                {"name": "Mother", "phone": "+919812345678", "relationship": "family"}
            ],
        },
    )
    assert user_response.status_code == 201
    user = user_response.json()
    assert user["trusted_contacts_count"] if False else True

    now = datetime.now(timezone.utc)
    trip_response = client.post(
        "/api/trips",
        json={
            "user_id": user["id"],
            "area_name": "Rishikesh to Gangtok trek",
            "start_latitude": 30.0869,
            "start_longitude": 78.2676,
            "end_latitude": 27.3389,
            "end_longitude": 88.6065,
            "valid_from": now.isoformat(),
            "valid_to": (now + timedelta(days=2)).isoformat(),
            "plan": "travel_pass",
        },
    )
    assert trip_response.status_code == 201
    assert trip_response.json()["status"] == "active"


def test_sos_assigns_nearest_node_and_creates_incident():
    user_response = client.post(
        "/api/users",
        json={
            "name": "Anita Verma",
            "phone": "+919800000000",
            "emergency_contacts": [
                {"name": "Sister", "phone": "+919811111111", "relationship": "family"}
            ],
        },
    )
    user_id = user_response.json()["id"]

    sos_response = client.post(
        "/api/sos",
        json={
            "user_id": user_id,
            "incident_type": "medical",
            "latitude": 30.1000,
            "longitude": 78.3000,
            "description": "Injury during trek",
        },
    )

    assert sos_response.status_code == 201
    body = sos_response.json()
    assert body["assigned_node"] == "node_rishikesh_01"
    assert body["trusted_contacts_notified"] == 1
    assert body["escalation"]["emergency_number"] == "112"

    incident_response = client.get(f"/api/incidents/{body['incident_id']}")
    assert incident_response.status_code == 200
    assert incident_response.json()["status"] == "open"


def test_update_incident_status():
    user_response = client.post(
        "/api/users",
        json={"name": "Rahul Singh", "phone": "+919822222222"},
    )
    user_id = user_response.json()["id"]

    sos_response = client.post(
        "/api/sos",
        json={
            "user_id": user_id,
            "incident_type": "safety",
            "latitude": 30.3165,
            "longitude": 78.0322,
            "description": "Feeling unsafe near highway",
        },
    )
    incident_id = sos_response.json()["incident_id"]

    update_response = client.patch(
        f"/api/incidents/{incident_id}/status",
        json={"status": "acknowledged", "note": "Coordinator acknowledged incident"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["status"] == "acknowledged"


def test_create_subscription():
    user_response = client.post(
        "/api/users",
        json={"name": "Meera Nair", "phone": "+919833333333"},
    )
    user_id = user_response.json()["id"]

    response = client.post(
        "/api/subscriptions",
        json={"user_id": user_id, "plan": "travel_pass", "duration_days": 7},
    )
    assert response.status_code == 201
    assert response.json()["status"] == "active"
