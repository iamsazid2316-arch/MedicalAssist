from conftest import auth_header


def test_cadet_can_create_and_read_own_case(client, cadet_token):
    created = client.post(
        "/cases",
        headers=auth_header(cadet_token),
        json={"symptoms": "Automated mild headache test"},
    )

    assert created.status_code == 200
    case_id = created.json()["case_id"]
    response = client.get(f"/cases/{case_id}", headers=auth_header(cadet_token))
    assert response.status_code == 200
    assert response.json()["case_id"] == case_id


def test_cadet_cannot_open_doctor_queue(client, cadet_token):
    response = client.get("/doctor/cases", headers=auth_header(cadet_token))

    assert response.status_code == 403


def test_doctor_cannot_create_cadet_case(client, doctor_token):
    response = client.post(
        "/cases",
        headers=auth_header(doctor_token),
        json={"symptoms": "This must be forbidden"},
    )

    assert response.status_code == 403


def test_doctor_can_approve_case(client, cadet_token, doctor_token):
    created = client.post(
        "/cases",
        headers=auth_header(cadet_token),
        json={"symptoms": "Automated approval test"},
    )
    case_id = created.json()["case_id"]

    decision = client.post(
        f"/doctor/cases/{case_id}/decision",
        headers=auth_header(doctor_token),
        json={"decision": "approve", "response": "Automated approval response"},
    )

    assert decision.status_code == 200
    assert decision.json()["status"] == "approved"

    cadet_response = client.get(
        f"/cases/{case_id}/response", headers=auth_header(cadet_token)
    )
    assert cadet_response.status_code == 200
    assert cadet_response.json()["response"] == "Automated approval response"
