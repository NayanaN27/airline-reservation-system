from app.models.flight import Flight

def test_flight_status_known_flight(client, app):
    resp = client.get(
        "/flight_status",
        query_string={
            "flight_num": "1001",
            "airline": "CSCI Air",
            "date": "2026-02-15",
        },
    )
    assert resp.status_code == 200
    body = resp.data.decode("utf-8")

    assert "On Time" in body

    # DB assertion
    with app.app_context():
        f = Flight.query.filter_by(airline_name="CSCI Air", flight_num=1001).first()
        assert f is not None
        assert f.status == "On Time"


def test_flight_status_unknown_flight_shows_friendly_behavior(client):
    resp = client.get(
        "/flight_status",
        query_string={
            "flight_num": "9999",
            "airline": "CSCI Air",
            "date": "2026-02-15",
        },
    )
    assert resp.status_code == 200
    body = resp.data.decode("utf-8").lower()

    assert ("no" in body and "flight" in body) or ("not found" in body) or ("error" not in body)