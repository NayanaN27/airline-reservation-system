import urllib.parse

def login_as_customer(client, email: str):
    with client.session_transaction() as sess:
        sess["user"] = email
        sess["user_type"] = "customer"

def test_customer_purchase_creates_purchase_and_ticket(client, app):
    customer_email = "naruto@example.com"
    login_as_customer(client, customer_email)

    flight_num = 1001
    airline_name = "CSCI Air"
    airline_path = urllib.parse.quote(airline_name)

    resp = client.post(f"/purchase/{flight_num}/{airline_path}", data={}, follow_redirects=False)

    assert resp.status_code == 302
    assert "/my_flights" in (resp.headers.get("Location") or "")

    conn = app.config["GET_DB"]()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT ticket_id FROM purchases WHERE customer_email=%s ORDER BY purchase_date DESC LIMIT 1",
                (customer_email,),
            )
            purchase = cur.fetchone()
            assert purchase is not None
            ticket_id = purchase["ticket_id"]

            cur.execute(
                "SELECT airline_name, flight_num FROM ticket WHERE ticket_id=%s",
                (ticket_id,),
            )
            ticket = cur.fetchone()
            assert ticket is not None
            assert ticket["airline_name"] == airline_name
            assert int(ticket["flight_num"]) == flight_num
    finally:
        conn.close()