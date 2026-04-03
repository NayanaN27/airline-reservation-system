def fetch_flights_for_airline(db, airline_name, filters):
    """
    Fetch flights for an airline with optional filters.
    Extracted from staff.view_flights route.
    filters keys: start_date, end_date, source, destination
    """
    cursor = db.cursor()

    base_query = """
        SELECT f.*, a1.airport_city as departure_city,
               a2.airport_city as arrival_city
        FROM flight f
        JOIN airport a1 ON f.departure_airport = a1.airport_name
        JOIN airport a2 ON f.arrival_airport = a2.airport_name
        WHERE f.airline_name = %s
    """
    params = [airline_name]

    start_date = filters.get("start_date")
    end_date = filters.get("end_date")
    source = filters.get("source")
    destination = filters.get("destination")

    if start_date:
        base_query += " AND f.departure_time >= %s"
        params.append(start_date)
    if end_date:
        base_query += " AND f.departure_time <= %s"
        params.append(end_date)
    if source:
        base_query += " AND (a1.airport_name LIKE %s OR a1.airport_city LIKE %s)"
        search = f"%{source}%"
        params.extend([search, search])
    if destination:
        base_query += " AND (a2.airport_name LIKE %s OR a2.airport_city LIKE %s)"
        search = f"%{destination}%"
        params.extend([search, search])

    base_query += " ORDER BY f.departure_time"

    try:
        cursor.execute(base_query, tuple(params))
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