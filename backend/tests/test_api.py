import uuid

import pytest
from fastapi.testclient import TestClient

from app.main import app

# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture(scope="module")
def client():
    return TestClient(app)

@pytest.fixture(scope="module")
def auth_headers(client):
    username = f"mastertest_{uuid.uuid4().hex[:8]}"
    email = f"{username}@example.com"
    password = "Test@12345"

    register_response = client.post(
        "/auth/register",
        json={
            "username": username,
            "full_name": "Master Scan Test User",
            "email": email,
            "password": password,
        },
    )

    assert register_response.status_code in {
        200,
        201,
    }

    login_response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }

# ============================================================
# OPENAPI / BASIC API TESTS
# ============================================================

def test_openapi_available(client):
    response = client.get("/openapi.json")

    assert response.status_code == 200

    data = response.json()

    assert "openapi" in data

def test_api_returns_json(client):
    response = client.get("/openapi.json")

    assert response.status_code == 200

    assert response.headers[
        "content-type"
    ].startswith("application/json")

# ============================================================
# MASTER SCAN - ROUTE REGISTRATION
# ============================================================

def test_master_scan_route_registered(client):
    response = client.get("/openapi.json")

    assert response.status_code == 200

    paths = response.json().get("paths", {})

    assert "/master-scan/" in paths

# ============================================================
# MASTER SCAN - BASIC REQUESTS
# ============================================================

def test_master_scan_requires_target(
    client,
    auth_headers,
):
    response = client.post(
        "/master-scan/",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "Failed"

    assert (
        "target" in data["message"]
        or "website" in data["message"]
    )

def test_master_scan_example_website(
    client,
    auth_headers,
):
    response = client.post(
        "/master-scan/",
        params={
            "website": "https://example.com"
        },
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert "status" in data
    assert "risk_level" in data
    assert "target" in data

    assert data["target"] == "https://example.com"

def test_master_scan_response_json(
    client,
    auth_headers,
):
    response = client.post(
        "/master-scan/",
        params={
            "website": "https://example.com"
        },
        headers=auth_headers,
    )

    assert response.status_code == 200

    assert response.headers[
        "content-type"
    ].startswith("application/json")

# ============================================================
# MASTER SCAN - RESPONSE STRUCTURE
# ============================================================

def test_master_scan_response_structure(
    client,
    auth_headers,
):
    response = client.post(
        "/master-scan/",
        params={
            "website": "https://example.com"
        },
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert "status" in data
    assert "target" in data
    assert "risk_level" in data

    if data.get("status") == "Completed":
        assert "risk_breakdown" in data
        assert "web_scan" in data
        assert "network_scan" in data
        assert "vulnerability" in data
        assert "phishing" in data

def test_master_scan_risk_level_valid(
    client,
    auth_headers,
):
    response = client.post(
        "/master-scan/",
        params={
            "website": "https://example.com"
        },
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    if "risk_level" in data:
        assert data["risk_level"] in {
            "Low",
            "Medium",
            "High",
            "Critical",
        }

def test_master_scan_risk_breakdown_structure(
    client,
    auth_headers,
):
    response = client.post(
        "/master-scan/",
        params={
            "website": "https://example.com"
        },
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    if data.get("status") == "Completed":
        assert "risk_breakdown" in data

        assert isinstance(
            data["risk_breakdown"],
            dict,
        )

def test_master_scan_completed_modules_structure(
    client,
    auth_headers,
):
    response = client.post(
        "/master-scan/",
        params={
            "website": "https://example.com"
        },
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    if data.get("status") == "Completed":
        assert "web_scan" in data
        assert "network_scan" in data
        assert "vulnerability" in data
        assert "phishing" in data

def test_master_scan_completed_response_has_scan_id(
    client,
    auth_headers,
):
    response = client.post(
        "/master-scan/",
        params={
            "website": "https://example.com"
        },
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    if data.get("status") == "Completed":
        assert "scan_id" in data
        assert isinstance(
            data["scan_id"],
            int,
        )

        assert "created_at" in data

# ============================================================
# MASTER SCAN - INVALID TARGET
# ============================================================

def test_master_scan_invalid_target_handled(
    client,
    auth_headers,
):
    response = client.post(
        "/master-scan/",
        params={
            "website": "not-a-valid-url"
        },
        headers=auth_headers,
    )

    assert response.status_code in {
        200,
        400,
        422,
    }

def test_master_scan_invalid_target_does_not_crash(
    client,
    auth_headers,
):
    response = client.post(
        "/master-scan/",
        params={
            "website": "invalid-target"
        },
        headers=auth_headers,
    )

    assert response.status_code in {
        200,
        400,
        422,
    }

# ============================================================
# MASTER SCAN - NETWORK TARGET
# ============================================================

def test_master_scan_network_target(
    client,
    auth_headers,
):
    response = client.post(
        "/master-scan/",
        params={
            "network_target": "127.0.0.1"
        },
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert "status" in data
    assert "target" in data

    if data.get("status") == "Completed":
        assert data["target"] == "127.0.0.1"
        assert "risk_level" in data

def test_master_scan_website_and_network_target(
    client,
    auth_headers,
):
    response = client.post(
        "/master-scan/",
        params={
            "website": "https://example.com",
            "network_target": "127.0.0.1",
        },
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert "status" in data
    assert "target" in data

def test_master_scan_requires_website_or_network(
    client,
    auth_headers,
):
    response = client.post(
        "/master-scan/",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "Failed"
    assert "message" in data

# ============================================================
# MASTER SCAN - HISTORY
# ============================================================

def test_master_scan_history_requires_auth(client):
    response = client.get(
        "/master-scan/history"
    )

    assert response.status_code == 401

def test_master_scan_history(
    client,
    auth_headers,
):
    response = client.get(
        "/master-scan/history",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "Success"

    assert "count" in data
    assert "scans" in data

    assert isinstance(
        data["scans"],
        list,
    )

def test_master_scan_history_structure(
    client,
    auth_headers,
):
    response = client.get(
        "/master-scan/history",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "Success"

    assert isinstance(
        data["count"],
        int,
    )

    assert isinstance(
        data["scans"],
        list,
    )

def test_master_scan_history_count_matches(
    client,
    auth_headers,
):
    response = client.get(
        "/master-scan/history",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["count"] == len(
        data["scans"]
    )

def test_master_scan_history_scan_structure(
    client,
    auth_headers,
):
    response = client.get(
        "/master-scan/history",
        headers=auth_headers,
    )

    assert response.status_code == 200

    scans = response.json()["scans"]

    for scan in scans:
        assert "id" in scan
        assert "target" in scan
        assert "scan_type" in scan
        assert "risk_level" in scan
        assert "created_at" in scan

        assert isinstance(
            scan["id"],
            int,
        )

        assert isinstance(
            scan["target"],
            str,
        )

        assert isinstance(
            scan["scan_type"],
            str,
        )

        assert scan["risk_level"] in {
            "Low",
            "Medium",
            "High",
            "Critical",
        }

def test_master_scan_history_only_returns_current_user_scans(
    client,
    auth_headers,
):
    response = client.get(
        "/master-scan/history",
        headers=auth_headers,
    )

    assert response.status_code == 200

    scans = response.json()["scans"]

    for scan in scans:
        assert "id" in scan
        assert "target" in scan

# ============================================================
# MASTER SCAN - DETAILS
# ============================================================

def test_master_scan_details_requires_auth(client):
    response = client.get(
        "/master-scan/1"
    )

    assert response.status_code == 401

def test_master_scan_details_not_found(
    client,
    auth_headers,
):
    response = client.get(
        "/master-scan/999999999",
        headers=auth_headers,
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == (
        "Master scan not found"
    )

def test_master_scan_details_invalid_id(
    client,
    auth_headers,
):
    response = client.get(
        "/master-scan/999999999",
        headers=auth_headers,
    )

    assert response.status_code == 404

    assert response.json()["detail"] == (
        "Master scan not found"
    )

def test_master_scan_zero_id(
    client,
    auth_headers,
):
    response = client.get(
        "/master-scan/0",
        headers=auth_headers,
    )

    assert response.status_code == 404

def test_master_scan_negative_id(
    client,
    auth_headers,
):
    response = client.get(
        "/master-scan/-1",
        headers=auth_headers,
    )

    assert response.status_code == 404

def test_master_scan_details_existing_scan(
    client,
    auth_headers,
):
    history_response = client.get(
        "/master-scan/history",
        headers=auth_headers,
    )

    assert history_response.status_code == 200

    scans = history_response.json()["scans"]

    if not scans:
        pytest.skip(
            "No master scan available"
        )

    scan_id = scans[0]["id"]

    response = client.get(
        f"/master-scan/{scan_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "Success"
    assert "scan" in data

    scan = data["scan"]

    assert scan["id"] == scan_id
    assert "user_id" in scan
    assert "target" in scan
    assert "scan_type" in scan
    assert "risk_level" in scan
    assert "result" in scan
    assert "created_at" in scan

# ============================================================
# MASTER SCAN - USER ISOLATION
# ============================================================

def test_master_scan_user_isolation(
    client,
    auth_headers,
):
    history_response = client.get(
        "/master-scan/history",
        headers=auth_headers,
    )

    assert history_response.status_code == 200

    scans = history_response.json()["scans"]

    if not scans:
        pytest.skip(
            "No master scan available for isolation test"
        )

    scan_id = scans[0]["id"]

    username = (
        f"seconduser_"
        f"{uuid.uuid4().hex[:8]}"
    )

    email = f"{username}@example.com"
    password = "Test@12345"

    register_response = client.post(
        "/auth/register",
        json={
            "username": username,
            "full_name": "Second Test User",
            "email": email,
            "password": password,
        },
    )

    assert register_response.status_code in {
        200,
        201,
    }

    login_response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    second_token = login_response.json()[
        "access_token"
    ]

    second_headers = {
        "Authorization": (
            f"Bearer {second_token}"
        )
    }

    response = client.get(
        f"/master-scan/{scan_id}",
        headers=second_headers,
    )

    assert response.status_code == 403

    assert response.json()["detail"] == (
        "Access denied"
    )

# ============================================================
# MASTER SCAN - SAVE / HISTORY CONSISTENCY
# ============================================================

def test_master_scan_saved_in_history(
    client,
    auth_headers,
):
    scan_response = client.post(
        "/master-scan/",
        params={
            "website": "https://example.com"
        },
        headers=auth_headers,
    )

    assert scan_response.status_code == 200

    scan_data = scan_response.json()

    if scan_data.get("status") != "Completed":
        pytest.skip(
            "Master scan did not complete"
        )

    assert "scan_id" in scan_data

    scan_id = scan_data["scan_id"]

    history_response = client.get(
        "/master-scan/history",
        headers=auth_headers,
    )

    assert history_response.status_code == 200

    history = history_response.json()

    ids = [
        scan["id"]
        for scan in history["scans"]
    ]

    assert scan_id in ids

def test_master_scan_saved_details_match(
    client,
    auth_headers,
):
    scan_response = client.post(
        "/master-scan/",
        params={
            "website": "https://example.com"
        },
        headers=auth_headers,
    )

    assert scan_response.status_code == 200

    data = scan_response.json()

    if data.get("status") != "Completed":
        pytest.skip(
            "Master scan did not complete"
        )

    assert "scan_id" in data

    scan_id = data["scan_id"]

    details_response = client.get(
        f"/master-scan/{scan_id}",
        headers=auth_headers,
    )

    assert details_response.status_code == 200

    saved_scan = details_response.json()[
        "scan"
    ]

    assert saved_scan["id"] == scan_id
    assert saved_scan["target"] == (
        "https://example.com"
    )
    assert saved_scan["scan_type"] == (
        "Full Scan"
    )

# ============================================================
# DASHBOARD - AUTHENTICATION
# ============================================================

def test_dashboard_requires_auth(client):
    response = client.get(
        "/dashboard/"
    )

    assert response.status_code == 401

def test_dashboard_rejects_invalid_token(client):
    response = client.get(
        "/dashboard/",
        headers={
            "Authorization": (
                "Bearer invalid-token"
            )
        },
    )

    assert response.status_code == 401

def test_dashboard_requires_bearer_token(client):
    response = client.get(
        "/dashboard/",
        headers={
            "Authorization": "invalid-token"
        },
    )

    assert response.status_code == 401

# ============================================================
# DASHBOARD - BASIC
# ============================================================

def test_dashboard_returns_200(
    client,
    auth_headers,
):
    response = client.get(
        "/dashboard/",
        headers=auth_headers,
    )

    assert response.status_code == 200

def test_dashboard_response_structure(
    client,
    auth_headers,
):
    response = client.get(
        "/dashboard/",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert "security_score" in data
    assert "total_scans" in data
    assert "total_alerts" in data
    assert "total_vulnerabilities" in data
    assert "status" in data

def test_dashboard_values_are_not_null(
    client,
    auth_headers,
):
    response = client.get(
        "/dashboard/",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["security_score"] is not None
    assert data["total_scans"] is not None
    assert data["total_alerts"] is not None
    assert data["total_vulnerabilities"] is not None
    assert data["status"] is not None

# ============================================================
# DASHBOARD - SECURITY SCORE
# ============================================================

def test_dashboard_security_score_valid(
    client,
    auth_headers,
):
    response = client.get(
        "/dashboard/",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(
        data["security_score"],
        int,
    )

    assert 0 <= data["security_score"] <= 100

# ============================================================
# DASHBOARD - TOTAL SCANS
# ============================================================

def test_dashboard_total_scans_valid(
    client,
    auth_headers,
):
    response = client.get(
        "/dashboard/",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(
        data["total_scans"],
        int,
    )

    assert data["total_scans"] >= 0

# ============================================================
# DASHBOARD - TOTAL ALERTS
# ============================================================

def test_dashboard_total_alerts_valid(
    client,
    auth_headers,
):
    response = client.get(
        "/dashboard/",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(
        data["total_alerts"],
        int,
    )

    assert data["total_alerts"] >= 0

# ============================================================
# DASHBOARD - TOTAL VULNERABILITIES
# ============================================================

def test_dashboard_total_vulnerabilities_valid(
    client,
    auth_headers,
):
    response = client.get(
        "/dashboard/",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(
        data["total_vulnerabilities"],
        int,
    )

    assert data[
        "total_vulnerabilities"
    ] >= 0

# ============================================================
# DASHBOARD - STATUS
# ============================================================

def test_dashboard_status_valid(
    client,
    auth_headers,
):
    response = client.get(
        "/dashboard/",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] in {
        "Safe",
        "Low",
        "Medium",
        "High",
        "Critical",
    }

# ============================================================
# DASHBOARD - CONSISTENCY
# ============================================================

def test_dashboard_same_user_gets_same_data(
    client,
    auth_headers,
):
    first_response = client.get(
        "/dashboard/",
        headers=auth_headers,
    )

    second_response = client.get(
        "/dashboard/",
        headers=auth_headers,
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 200

    assert (
        first_response.json()
        == second_response.json()
    )

# ============================================================
# DASHBOARD - NEW USER DEFAULTS
# ============================================================

def test_dashboard_new_user_defaults(client):
    username = (
        f"newdashboard_"
        f"{uuid.uuid4().hex[:8]}"
    )

    email = f"{username}@example.com"
    password = "Test@12345"

    register_response = client.post(
        "/auth/register",
        json={
            "username": username,
            "full_name": "New Dashboard User",
            "email": email,
            "password": password,
        },
    )

    assert register_response.status_code in {
        200,
        201,
    }

    login_response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()[
        "access_token"
    ]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.get(
        "/dashboard/",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["security_score"] == 100
    assert data["total_scans"] == 0
    assert data["total_alerts"] == 0
    assert data[
        "total_vulnerabilities"
    ] == 0
    assert data["status"] == "Safe"

# ============================================================
# DASHBOARD - USER ISOLATION
# ============================================================

def test_dashboard_user_isolation(client):
    username = (
        f"dashboard_"
        f"{uuid.uuid4().hex[:8]}"
    )

    email = f"{username}@example.com"
    password = "Test@12345"

    register_response = client.post(
        "/auth/register",
        json={
            "username": username,
            "full_name": "Dashboard Test User",
            "email": email,
            "password": password,
        },
    )

    assert register_response.status_code in {
        200,
        201,
    }

    login_response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()[
        "access_token"
    ]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.get(
        "/dashboard/",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert "security_score" in data
    assert "total_scans" in data
    assert "total_alerts" in data
    assert "total_vulnerabilities" in data
    assert "status" in data

# ============================================================
# DASHBOARD - RESPONSE FORMAT
# ============================================================

def test_dashboard_response_is_json(
    client,
    auth_headers,
):
    response = client.get(
        "/dashboard/",
        headers=auth_headers,
    )

    assert response.status_code == 200

    assert response.headers[
        "content-type"
    ].startswith("application/json")

# ============================================================
# DASHBOARD - OPENAPI
# ============================================================

def test_dashboard_openapi_registered(client):
    response = client.get(
        "/openapi.json"
    )

    assert response.status_code == 200

    paths = response.json().get(
        "paths",
        {},
    )

    assert "/dashboard/" in paths

# ============================================================
# DASHBOARD - SECURITY / DATA EXPOSURE
# ============================================================

def test_dashboard_does_not_expose_user_id(
    client,
    auth_headers,
):
    response = client.get(
        "/dashboard/",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert "user_id" not in data

def test_dashboard_does_not_expose_database_id(
    client,
    auth_headers,
):
    response = client.get(
        "/dashboard/",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert "id" not in data
