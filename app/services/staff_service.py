from app.services.flight_query_builder import FlightQueryBuilder

def fetch_flights_for_airline(db, airline_name, filters):
    """
    Fetch flights for an airline with optional filters.
    Extracted from staff.view_flights route.
    filters keys: start_date, end_date, source, destination
    """
    cursor = db.cursor()

    start_date = filters.get("start_date")
    end_date = filters.get("end_date")
    source = filters.get("source")
    destination = filters.get("destination")

    builder = (
        FlightQueryBuilder(airline_name)
        .with_start_date(start_date)
        .with_end_date(end_date)
        .with_source(source)
        .with_destination(destination)
    )
    query, params = builder.build()
    query += " ORDER BY f.departure_time"

    try:
        cursor.execute(query, tuple(params))
        return cursor.fetchall()
    finally:
        cursor.close()

def fetch_airplanes_for_airline(db, airline_name):
    """
    Fetch airplanes for an airline. Extracted from staff.view_airplanes route.
    """
    cursor = db.cursor()
    try:
        query = """
            SELECT airplane_id, seats
            FROM airplane
            WHERE airline_name = %s
            ORDER BY airplane_id
        """
        cursor.execute(query, (airline_name,))
        return cursor.fetchall()
    finally:
        cursor.close()