from app.services.flight_query_builder import FlightQueryBuilder

def test_builder_adds_filters_in_order():
    sql, params = (
        FlightQueryBuilder("CSCI Air")
        .with_start_date("2026-02-01")
        .with_end_date("2026-02-28")
        .with_source("SFO")
        .with_destination("LAX")
        .build()
    )

    assert "WHERE f.airline_name = %s" in sql
    assert "f.departure_time >= %s" in sql
    assert "f.departure_time <= %s" in sql
    assert "a1.airport_name LIKE %s" in sql
    assert "a2.airport_name LIKE %s" in sql
    assert params[0] == "CSCI Air"