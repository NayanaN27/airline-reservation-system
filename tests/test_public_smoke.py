def test_home_page_loads(client):
    r = client.get("/")
    assert r.status_code == 200

def test_login_page_loads(client):
    r = client.get("/login")
    assert r.status_code == 200

def test_flight_status_page_loads(client):
    r = client.get("/flight_status")
    assert r.status_code == 200