# tests/test_search_result.py
from app.models.flight import Flight

def test_search_result_returns_seeded_flight(client, app):
    resp = client.get(
        "/search_result",
        query_string={
            "source": "SFO",
            "destination": "LAX",
            "start_date": "2026-02-15",
            "end_date": "2026-02-15",
        },
    )
    assert resp.status_code == 200

    # UI-level assertion (page loads + shows the route)
    body = resp.data.decode("utf-8")
    assert "SFO" in body
    assert "LAX" in body

    # DB-level assertion (proves flight 1001 exists in the seeded DB)
    with app.app_context():
        f = Flight.query.filter_by(airline_name="CSCI Air", flight_num=1001).first()
        assert f is not None
        assert f.departure_airport == "SFO"
        assert f.arrival_airport == "LAX"
        assert f.status == "On Time"