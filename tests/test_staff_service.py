from flask import current_app
from app.services.staff_service import fetch_flights_for_airline

def test_fetch_flights_for_airline_returns_list(app):
    with app.app_context():
        db = current_app.config["GET_DB"]()
        try:
            flights = fetch_flights_for_airline(
                db,
                "CSCI Air",
                {"start_date": None, "end_date": None, "source": None, "destination": None},
            )
            assert flights is not None
            assert isinstance(flights, list)
        finally:
            db.close()