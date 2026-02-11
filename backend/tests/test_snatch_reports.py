"""Tests for snatching report endpoints."""


def test_create_snatch_report(client, auth_header, sample_mobile_data):
    """Submit report for registered device → device marked stolen."""
    # Register device first
    client.post("/api/mobiles/register-self", json=sample_mobile_data, headers=auth_header)

    resp = client.post(
        "/api/snatch-reports",
        json={
            "victim_cnic": "12345-6789012-3",
            "device_imei": sample_mobile_data["imei"],
            "incident_description": "Device was snatched at gunpoint near Saddar area",
        },
        headers=auth_header,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "pending"
    assert data["device_imei"] == sample_mobile_data["imei"]
    assert data["mobile_id"] is not None

    # Verify device is now marked stolen
    device_resp = client.get(f"/api/mobiles/by-imei/{sample_mobile_data['imei']}", headers=auth_header)
    assert device_resp.json()["status"] == "stolen"


def test_create_report_unregistered_device(client, auth_header):
    """IMEI not in system → still creates report with mobile_id=null."""
    resp = client.post(
        "/api/snatch-reports",
        json={
            "victim_cnic": "12345-6789012-3",
            "device_imei": "353456789012345",
            "incident_description": "My device was snatched while walking near Burns Garden",
        },
        headers=auth_header,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["mobile_id"] is None
    assert data["status"] == "pending"


def test_list_my_reports(client, auth_header):
    """User sees only their reports."""
    # Create a report
    client.post(
        "/api/snatch-reports",
        json={
            "victim_cnic": "12345-6789012-3",
            "device_imei": "353456789012345",
            "incident_description": "Device snatched near Clifton Bridge at night",
        },
        headers=auth_header,
    )

    resp = client.get("/api/snatch-reports", headers=auth_header)
    assert resp.status_code == 200
    reports = resp.json()
    assert len(reports) == 1


def test_admin_list_snatch_reports(client, auth_header, admin_header):
    """Admin sees all reports."""
    # Create report as citizen
    client.post(
        "/api/snatch-reports",
        json={
            "victim_cnic": "12345-6789012-3",
            "device_imei": "353456789012345",
            "incident_description": "Snatched near Tariq Road while stuck in traffic",
        },
        headers=auth_header,
    )

    resp = client.get("/api/admin/snatch-reports", headers=admin_header)
    assert resp.status_code == 200
    reports = resp.json()
    assert len(reports) >= 1


def test_admin_review_snatch_report(client, auth_header, admin_header):
    """Admin marks report as reviewed → status changes."""
    client.post(
        "/api/snatch-reports",
        json={
            "victim_cnic": "12345-6789012-3",
            "device_imei": "353456789012345",
            "incident_description": "Device was snatched at gunpoint near Saddar area",
        },
        headers=auth_header,
    )

    # Get reports
    resp = client.get("/api/admin/snatch-reports", headers=admin_header)
    report_id = resp.json()[0]["id"]

    # Review
    resp = client.put(f"/api/admin/snatch-reports/{report_id}/review", headers=admin_header)
    assert resp.status_code == 200
    data = resp.json()
    assert data["is_reviewed"] is True
    assert data["status"] == "under_review"
